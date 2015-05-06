import sys
sys.path.append('gen-py')
import ConfigParser

from tis import SmsService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.server import TNonblockingServer

from handler.sms_service_handler import SMSServiceHandler
from util.log import logger

def init():
    cfg = {}
    config = ConfigParser.ConfigParser()
    config.read('config/config.ini')
    sections = config.sections()
    for section in sections:
        cfg[section] = {}
        options = config.options(section)
        for option in options:
            try:
                cfg[section][option] = config.get(section, option)
            except Exception, e:
                logger.warning("parse config error, e[%s]" % e)
    logger.info('server cfg[%s]' % cfg)
    return cfg

cfg = init()
account = cfg['passport'].get('account', '')
password = cfg['passport'].get('password', '')
port = int(cfg['server'].get('port', ''))
threads = int(cfg['server'].get('threads', ''))

handler = SMSServiceHandler(account, password)
processor = SmsService.Processor(handler)
#transport = TSocket.TServerSocket(port=9990)
transport = TSocket.TServerSocket(port=port)
#tfactory = TTransport.TFramedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

#server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
server = TNonblockingServer.TNonblockingServer(processor, transport, None, pfactory)
server.setNumThreads(threads)

logger.info('Starting the server...')
server.serve()
logger.info('done.')
