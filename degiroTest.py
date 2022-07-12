import json
import time
import logging
from datetime import datetime, timedelta

import tinydb
import degiroapi

from Share import Share

degiro = degiroapi.DeGiro()

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO)

sleepTime = 5  # [s]


with open('Config/credentials.json', 'r') as credFile:
    credentials = json.loads(credFile.read())
    degiro.login(credentials['name'], credentials['password'])

    db = tinydb.TinyDB('Data/db.json')

    transactions = db.table('transactions')

    lastOrders = []
    shares = dict()

    # MAIN LOOP
    while True:
        availableFunds = degiro.getdata(degiroapi.Data.Type.CASHFUNDS)

        orders = degiro.orders(datetime.now() - timedelta(days=1), datetime.now(), True)
        orders = [ele for ele in orders if ele['status'] in ('PENDING', )]

        if orders == lastOrders:
            log.info(f'No change...')
        else:
            log.info(f'Orders changed...')

            # print the current portfolio (True to filter Products with size 0, False to show all)
            portfolio = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
            for product in portfolio:
                if product['id'] == '1153605':  # Tesla, testing only
                    try:
                        realPrice = degiro.real_time_price(product['id'], degiroapi.Interval.Type.One_Day)

                        if product['id'] not in shares:
                            shares[product['id']] = Share(degiro,
                                                          degiro.product_info(product['id']),
                                                          fee=2,  # EUR
                                                          amount=product['size'] / 2)

                        selectedProduct = shares[product['id']]

                        if realPrice:
                            value = realPrice[0]['data']['lastPrice']

                            selectedProduct.createStopLossOrder(value)

                    except Exception as e:
                        log.error(f'Something went wrong {e}')

            lastOrders = orders

        time.sleep(sleepTime)


    degiro.logout()