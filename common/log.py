# coding: utf-8

import logging
import logging.config
import os
from logging.handlers import TimedRotatingFileHandler


def gen_logger(_name):
    # logging.config.fileConfig("logger.conf")
    logger = logging.getLogger("bigone")

    level = logging.INFO
    logger.setLevel(level)

    fmt = logging.Formatter('[%(asctime)s] %(filename)s[line:%(lineno)d] [%(levelname)s]: %(message)s')

    fmt_less = logging.Formatter('[%(levelname)s]: %(message)s')

    filename = os.path.join('%s.log' % _name).replace('\\', '/')

    hdlr = TimedRotatingFileHandler(filename, 'midnight', 1, 0,encoding='utf8')
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)

    fhlr = logging.StreamHandler()
    fhlr.setFormatter(fmt_less)
    logger.addHandler(fhlr)
