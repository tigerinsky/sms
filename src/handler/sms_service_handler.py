#!/usr/bin/env python
#coding:utf-8

import sys
sys.path.append('../gen-py')
import time
import xml
import xml.etree.ElementTree as ET

from util.log import logger
from util.timer import timer
from util import http

from config.const import PARAM_ERROR
from config.const import SEND_SMS_URL
from config.const import SUCCESS
from config.const import SEND_FAILED
from config.const import HTTP_REQUEST_ERROR
from config.const import THIRD_SERVER_ERROR

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

    @timer('send_sms')
    def send_sms(self, request):
        logger.info('send sms, request[%s]' % request)
        if request.mobile == '' or request.content == '':
            logger.warning('param error request[%s]' % request)
            return PARAM_ERROR

        param = self.__build_param(request)
        result = http.request(SEND_SMS_URL, param, 'GET', 10)
        if not result:
            return HTTP_REQUEST_ERROR

        logger.debug('result:%s' % result)
        root = None
        try:
            root = ET.fromstring(result)
            status = root.find('returnstatus').text
            if status != 'Success':
                msg = root.find('message').text
                logger.warning('send failed, msg[%s]' % msg)
                return SEND_FAILED
        except xml.etree.ElementTree.ParseError:
            logger.warning("invalid result[%s] request[%s]" % (result, request))
            return THIRD_SERVER_ERROR
        except Exception, e:
            logger.warning('xml parse exception,ult[%s] request[%s]' % (result, request))

        return SUCCESS

    def heart_beat(self):
        return True
