#!/usr/bin/python

from .udp_server import PBPacketReceiver
from . import messages_robocup_ssl_wrapper_pb2 as ssl_wrapper


class Vision(PBPacketReceiver):

    def __init__(self, host="224.5.23.2", port=10020):
        super(Vision, self).__init__(host, port, ssl_wrapper.SSL_WrapperPacket)
