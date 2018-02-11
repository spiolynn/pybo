# coding: utf-8

from bigone import BigOneDog
from common import gen_logger

import logging
import time
import json


def strategy_eth_big_bnc_eth(dog):
    """
    正向：买BIG/ETH -> 卖BIG/BNC -> 买ETH/BNC
    反向：卖ETH/BNC -> 买BIG/BNC -> 卖BIG/ETH
    :param dog: implemention of BigOneDog
    :return: 正向收益率，反向收益率
    """
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

    # positive transaction
    pos_anc = 0.999*0.999*0.999*\
              ((1 / (float(big_eth_data['bids'][0]['price'])))
              * float(big_bnc_data['asks'][0]['price']) )
    pos_anc = pos_anc / float(eth_bnc_data['bids'][0]['price']) - 1

    # negative transaction
    neg_anc = 0.999 * 0.999 * 0.999 * \
          (float(eth_bnc_data['bids'][0]['price'])
           / float(big_bnc_data['asks'][0]['price'])
           * float(big_eth_data['asks'][0]['price']))
    neg_anc = neg_anc / 1 - 1

    return pos_anc, neg_anc


def strategy_eth_bnc(dog):
    eth_bnc_data = dog.get_order_book('ETH-BNC')
    print('ETH-BNC')
    print('卖一', eth_bnc_data['asks'][0]['price'], eth_bnc_data['asks'][0]['amount'])
    print('买一', eth_bnc_data['bids'][0]['price'], eth_bnc_data['bids'][0]['amount'])
    anc = float(eth_bnc_data['asks'][0]['price']) / float(eth_bnc_data['bids'][0]['price']) - 1
    print(anc)
    if anc > 0.02:
        r = dog.create_order('ETH-BNC', 'BID', str(float(eth_bnc_data['bids'][0]['price'])+0.01), '0.01' )
        bid_order_id = r['order_id']

        r = dog.create_order('ETH-BNC', 'ASK', str(float(eth_bnc_data['asks'][0]['price'])-0.01), '0.01' )
        ask_order_id = r['order_id']

    return anc, anc

if __name__ == '__main__':
    gen_logger('bigonetest')
    logger = logging.getLogger("bigone")

    with open("PRIVATE_KEY.json",'r') as f:
        private_key = json.load(f)["key"]
    dog = BigOneDog(private_key)
    strategy_eth_bnc(dog)
    # dog.get_orders("ETH-BNC",'10')
    # r = dog.get_order("b79ef031-c477-46f9-b452-7e97aa97435d")
    # print(r)
    # r = dog.get_orders('ETH-BNC','10')
    # print(r)

    while False:

        # pos_anc, neg_anc = strategy_eth_big_bnc_eth(dog)
        pos_anc, neg_anc = strategy_eth_bnc(dog)
        if pos_anc < 0.01:
            result = "利润空间小于1%, 放弃本次套利 0"
        else:
            result = "利润空间大于1%, 执行本次套利 1"

        logger.info("预期本次[正向套利:买BIG/ETH -> 卖BIG/BNC -> 买ETH/BNC]利润: {0:.2f}%, {1}".format(pos_anc*100,result))

        if neg_anc < 0.01:
            result = "利润空间小于1%, 放弃本次套利 0"
        else:
            result = "利润空间大于1%, 执行本次套利 1"

        logger.info("预期本次[反向套利:卖ETH/BNC -> 买BIG/BNC -> 卖BIG/ETH]利润: {0:.2f}%, {1}".format(neg_anc*100,result))

        print("休眠10秒")
        print("")
        time.sleep(10)

