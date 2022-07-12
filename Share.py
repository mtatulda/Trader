import logging

log = logging.getLogger(__name__)

from degiroapi.product import Product
from degiroapi.order import Order


class Share(Product):
    def __init__(self, degiro, productInfo, fee: float, amount: int):
        super().__init__(productInfo)
        self.degiro = degiro

        self.fee = fee  # EUR
        self.lastPrice = 0
        self.amount = amount

    def createStopLossOrder(self, currentPrice: float):
        log.info(f'Creating STOP LOSS order for {self.name}')
        status = self.degiro.sellorder(Order.Type.STOPLIMIT,
                              productId=self.id,
                              timeType=1,  # 1 = one day ony, 3 = all time
                              size=self.amount,  # how much to sell?
                              limit=round(currentPrice * 0.99, 2),
                              stop_loss=round(currentPrice * 0.991, 2))

        return status

    def createSellOrder(self, currentPrice: float):
        log.info(f'Creating SELL order for {self.name}')

    def createBuyOrder(self, currentPrice: float):
        log.info(f'Creating BUY order for {self.name}')
