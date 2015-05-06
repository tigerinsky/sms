#coding:utf-8
import sys
sys.path.append('gen-py')
import time

from tis import SmsService
from tis.ttypes import SendSMSRequest

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol



try:
    transport = TSocket.TSocket('localhost', 9898)
    transport = TTransport.TFramedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = SmsService.Client(protocol)

    # Connect!
    transport.open()
    request = SendSMSRequest('18611629534', '亲爱的用户您好，您的验证码为：8857。请于10分钟内完成注册。【翼众文化】')
    #print client.heart_beat()

    print client.send_sms(request)
except Exception, e:
    print '%s' % e
