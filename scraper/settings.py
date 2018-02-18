# Pleace don't change service address, web scraper working ONLY with address
service = 'https://www.flyniki.com/'

# First request params.
data_request = {
    'openDateOverview': '0',
    'adultCount': '1',
    'childCount': '0',
    'infantCount': '0',
    'oneway': '0'
}

# Data for second request.
data_second_request = {
    '_ajax[templates][]': ['main', 'priceoverview', 'infos', 'flightinfo'],
    '_ajax[requestParams][returnDeparture]': '',
    '_ajax[requestParams][returnDestination]': '',
    '_ajax[requestParams][adultCount]': data_request.get('adultCount'),
    '_ajax[requestParams][childCount]': data_request.get('childCount'),
    '_ajax[requestParams][infantCount]': data_request.get('infantCount'),
    '_ajax[requestParams][openDateOverview]': '',
    '_ajax[requestParams][oneway]': ''
}

# Headers for 1th and 2th requests.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; '
                  'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/javascript, */*'
}
