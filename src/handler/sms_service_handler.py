#!/usr/bin/env python
#coding:utf-8

import sys
sys.path.append('../gen-py')
import time

from util.log import logger
from util.timer import timer
from util import http

from config.const import PARAM_ERROR
from config.const import SEND_SMS_URL
from config.const import SUCCESS

class SMSServiceHandler(object):
    def __init__(self, account, password):
        self.account = account
        self.password = password

    def __build_param(self, request):
        data = {}
        data['action'] = 'send'
        data['account'] = self.account
        data['password'] = self.password
        data['mobile'] = request.mobile
        data['content'] = request.content
        data['sendTime'] = ''
        if hasattr(request, 'send_time') and request.send_time != 0:
            t = request.send_time
            try:
                x = time.localtime(t)
                data['sendTime'] = time.strftime("%Y-%m-%d %H:%M:%S", x)
            except Exception, e:
                logger.warning('time trans exception, t[%s], e[%s]' % (t, e))

        return data



    def send_sms(self, request):
        if request.mobile == '' or request.content == '':
            logger.warning('param error request[%s]' % request)
            return PARAM_ERROR

        param = self.__build_param(request)
        result = http.request(SEND_SMS_URL, param, 'GET', 10)

        logger.info('result:%s' % result)

        return SUCCESS



    def heart_beat(self):
        return True
