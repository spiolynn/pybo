# -*- coding: utf-8 -*-

from bigone import BigOneDog
from common import gen_logger

import logging
import time

# private key, delete when publish
private_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDk4MTUxMDAsImp0aSI6ImM1MjdhMWUyLTE3ZjMtNDUyNS1hNjkzLTc0OGVjMzZiMmEwZSJ9.OhBEO0bFfAvKPPKfkvCotpmVIKPz2GSWeF8UkU7GwlI:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDk4MTUxMDB9.YuQtu2A4N7WsOBTUacnvzNKWkKvHfBuL-5_AD1cm4lE"


if __name__ == '__main__':
    gen_logger('bigonetest')
    logger = logging.getLogger("bigone")

    dog = BigOneDog(private_key)
    while True:

        big_eth_data = dog.get_order_book('BIG-ETH')
        big_bnc_data = dog.get_order_book('BIG-BNC')
        eth_bnc_data = dog.get_order_book('ETH-BNC')
        print('BIG-ETH')
        print('卖一', big_eth_data['asks'][0]['price'], big_eth_data['asks'][0]['amount'])
        print('买一', big_eth_data['bids'][0]['price'], big_eth_data['bids'][0]['amount'])
        print('BIG-BNC')
        print('卖一', big_bnc_data['asks'][0]['price'], big_bnc_data['asks'][0]['amount'])
        print('买一', big_bnc_data['bids'][0]['price'], big_bnc_data['bids'][0]['amount'])
        print('ETH-BNC')
        print('卖一', eth_bnc_data['asks'][0]['price'], eth_bnc_data['asks'][0]['amount'])
        print('买一', eth_bnc_data['bids'][0]['price'], eth_bnc_data['bids'][0]['amount'])
        anc = 0.999*0.999*0.999*\
              ((1 / (float(big_eth_data['bids'][0]['price'])))
              * float(big_bnc_data['asks'][0]['price']) )

        anc = anc / float(eth_bnc_data['bids'][0]['price']) - 1
        if anc < 0.01:
            result = "利润空间小于1%, 放弃本次套利 0"
        else:
            result = ",利润空间大于1%, 执行本次套利 1"
        # print("预期本次[正向套利]利润%：{0:.2f}%, {1}".format(anc*100,result))
        logger.info("预期本次[正向套利:买BIG/ETH -> 卖BIG/BNC -> 买ETH/BNC]利润%：{0:.2f}%, {1}".format(anc*100,result))

        anc = 0.999*0.999*0.999*\
              (float(eth_bnc_data['bids'][0]['price'])
               /float(big_bnc_data['asks'][0]['price'])
               * float(big_eth_data['asks'][0]['price']))
        anc = anc / 1 - 1


        if anc < 0.01:
            result = "利润空间小于1%, 放弃本次套利 0"
        else:
            result = ",利润空间大于1%, 执行本次套利 1"
        # print("预期本次[反向套利]利润%：{0:.2f}%, {1}".format(anc*100,result))
        logger.info("预期本次[反向套利:卖ETH/BNC -> 买BIG/BNC -> 卖BIG/ETH]利润%：{0:.2f}%, {1}".format(anc*100,result))

        print("休眠10秒")
        print("")
        time.sleep(10)
