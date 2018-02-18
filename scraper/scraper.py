import logging
import re
import requests
import sys
import traceback
from datetime import datetime
from lxml.html import fromstring

from .settings import (
    service,
    data_request,
    data_second_request,
    headers)


# Determining new call depending on python version.
redefine_input = input


def airports_base():
    """Web-server gives the data away."""

    base_url = (
        '{}en/site/json/suggestAirport.php?'
        'searchfor=departures&searchflightid=0&departures%5B%5D=&'
        'destinations%5B%5D=City%2C+airport'
        '&suggestsource%5B0%5D=activeairports&withcountries=0'
        '&withoutroutings=0&promotion%5Bid%5D=&promotion%5Btype%5D='
        '&get_full_suggest_list=false'
        '&routesource%5B0%5D=airberlin'
        '&routesource%5B1%5D=partner'.format(service)
    )
    respons_from_base = requests.get(base_url)
    respons_from_base.raise_for_status()
    try:
        base = [i.get('code')
                for i in respons_from_base.json().get('suggestList')]
    except (TypeError, ValueError):
        logging.error("Sorry, service can't fetch routes. "
                      "Please address to your technical support.")
        logging.error(traceback.format_exc())
        sys.exit()
    return base


def get_request(session):
    """Makes request to service.
    Request getting secure id for second request.

    """
    url = '{}en/booking/flight/vacancy.php'.format(service)
    first_request = session.get(url, headers=headers, params=data_request)
    tree = fromstring(first_request.text)
    dep_name = tree.xpath('//input[@id="departure"]/@value')[0]
    dst_name = tree.xpath('//input[@id="destination"]/@value')[0]
    data_second_request.update({'_ajax[requestParams][departure]': dep_name,
                                '_ajax[requestParams][destination]': dst_name})
    return first_request.url


def data_parser(tree):
    """Take data from second request and parsing to build fight variant."""

    out_dict = {}
    ret_dict = {}
    fish_lst = []
    pattern = re.compile('\d+\.\d+')
    cmn_templ = '//div[@class="lowest"]/span'
    out_templ = '//div[@class="outbound block"]//div[@class="lowest"]/span'
    ret_templ = '//div[@class="return block"]//div[@class="lowest"]/span'
    crncy = tree.xpath('//th[@id="flight-table-header-price-ECO_PREM"]'
                       '/text()')

    if crncy:
        crncy = crncy[0]
    else:
        crncy = None

    # Checking that server gave valid html and there is data in it.
    if tree.xpath(cmn_templ):
        print('Flight-data:')
        # Output flight heading: Departure - Destination, day, date: dd/mm/yyyy.
        print('\n'.join([i for i in
                         tree.xpath('//div[@class="vacancy_route"]/text()')]))
    else:
        print('Sorry, no data was found.')

    if data_request['oneway'] == '0':
        # Filling dicts for final output.
        # That part contains duplication,
        # but it is more appropriate for understanding.
        for elem in tree.xpath(out_templ):
            out_dict[str(elem.xpath('@title')[0])+str(crncy)] \
                = pattern.search(str(elem.xpath('@title')[0])).group()
        for elem in tree.xpath(ret_templ):
            ret_dict[str(elem.xpath('@title')[0])+str(crncy)] \
                = pattern.search(str(elem.xpath('@title')[0])).group()

        # Alternative option for 2 cycle for its' itertools.product.
        for i in out_dict.items():
            for j in ret_dict.items():
                fish_lst.append([i[0], j[0], (float(i[1]) + float(j[1]))])

        for elem in sorted(fish_lst, key=lambda x: x[2]):
            print('{0}\n{1}\n{2}\n{3}: {4:.2f}{5}'
                  .format('', elem[0], elem[1], 'Total price', elem[2], crncy))
    else:
        for elem in tree.xpath(cmn_templ):
            print('{0}{1}'.format(elem.xpath('@title')[0], crncy))


def do_healthcheck():
    """Before main requests send request on service to check his status."""
    try:
        print("Please wait. Getting response from service...")
        response = requests.get(service)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logging.error("Can't connect to service {0}".format(service))
        logging.error(traceback.format_exc())
        sys.exit()
    print("Service is UP.")


def iata_date_receiver():
    """Compare insert data and IATA-codes from flyniki base."""

    cycle = None
    base = airports_base()
    print('Service is ready to work, please input flight-parameters:')
    for place in ('departure', 'destination'):
        print('Please, insert {0}: '.format(place))
        insert_iata = redefine_input().upper()
        while insert_iata not in base or insert_iata == cycle:
            print('Value is not acceptable or the same as the previous one, '
                  'try again.\nINFO: please insert IATA-code of country or'
                  ' airport: {0}'.format(', '.join(base[:10])))

            insert_iata = redefine_input().upper()
        data_request.update({place: insert_iata})
        cycle = insert_iata

    print('Now, please insert outbound date. Format yyyy-mm-dd:')
    outbound = date_validator(redefine_input(), datetime.today().date())
    data_request.update({'outboundDate': outbound})
    data_second_request.update({'_ajax[requestParams][outboundDate]': outbound})

    print('Please, insert return date. Format yyyy-mm-dd or skip for oneway:')
    ret = redefine_input()
    if ret != '':
        ret = date_validator(ret, datetime.strptime(outbound,
                                                    '%Y-%m-%d').date())
        data_request.update({'returnDate': ret})
        data_second_request.update({'_ajax[requestParams][returnDate]': ret})
    else:
        data_request.update({'oneway': '1'})
        data_second_request.update({
            '_ajax[requestParams][returnDate]': outbound,
            '_ajax[requestParams][oneway]': 'on'})


def date_validator(value, compare_date):
    while True:
        try:
            if datetime.strptime(str(value), '%Y-%m-%d').date() < compare_date:
                print('Sorry, you insert not valid date. '
                      'Try again:\nFormat yyyy-mm-dd')
                value = redefine_input()
            else:
                return value
        except ValueError:
            print('Sorry, you insert not valid date.\n'
                  'Please insert correct date, format yyyy-mm-dd')
            value = redefine_input()
