# coding: utf-8
"""
exception model of ZIEN Models
@Author: chengli
@Date: 2017.02.25
"""
import logging
import logging.config

# ERROR CODE CONSTANTS
# file error
XFS = 'XFS'
# account error
XAC = 'XAC'
# database error
XDB = 'XDB'
# SERVER error
XSR = 'XSR'

logger = logging.getLogger("bigone")


class ZienException(Exception):
    def __init__(self, _err_code, _err_msg, _base_err_msg):
        self.err_code = _err_code
        self.err_msg = _err_msg
        self.base_err_msg = _base_err_msg

    def __str__(self):
        return "[ERROR_CODE]: %s, [ERROR_MSG]: %s, [DETAIL]: %s" \
               % (self.err_code, self.err_msg, self.base_err_msg)

    def log(self, _level):
        o = "[ERROR_CODE]: %s, [ERROR_MSG]: %s, [DETAIL]: %s" \
            % (self.err_code, self.err_msg, self.base_err_msg)
        if _level == 'INFO':
            logger.INFO(o)
        elif _level == 'WARNING':
            logger.warning(o)
        elif _level == 'ERROR':
            logger.error(o)
        else:
            logger.debug(o)
