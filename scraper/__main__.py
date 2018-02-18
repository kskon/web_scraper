import sys

from .scraper import (
    do_healthcheck,
    iata_date_receiver,
    get_request,
    data_parser)


def main():
    do_healthcheck()
    # Input and validate data
    iata_date_receiver()
    response = get_request()
    data_parser(response)


if __name__ == "__main__":
    main()
