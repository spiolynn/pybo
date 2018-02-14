from bigone import BigOneDog
from common import gen_logger

import logging
import time
import json

def Get_All_Currency(dog):
    """
    获取bigone中所有的币种信息
    :return: List Currency
    """
    List_Currency=[]
    All_Currency_Infos = r=dog.get_accounts()
    for All_Currency_Info in All_Currency_Infos:
        List_Currency.append(All_Currency_Info['account_type'])
    return List_Currency




