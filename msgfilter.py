import time
import json
import sys
from collections import defaultdict
import re
import logging
logger = logging.getLogger('filter')
logger.setLevel(logging.DEBUG)

import aflstatsgraph, aflsubgraphs


class MSGFilter:
    def __init__(self):
        self.filters = defaultdict(list)
        

    def process_cmd(self, cmd):
        msg = cmd

        if cmd.startswith('graph:'):
            items = re.findall(r'graph:(.*)', cmd)
            args = items[0].strip().split(' ')
            print args
            style = args[0]
            year = args[1]
            exarg = args[2]
            plotid=''
            fightml=''
            if style=='all' or style=='summary':
                plotid, fightml = aflstatsgraph.request_graph(year, style)
            else:
                plotid, fightml = aflsubgraphs.request_graph(year, style, exarg)
            msg = 'plotid:'+ plotid
            msg += ('fightml:<p> Graph style: ' +style+'</p>\n'+ fightml)
        return msg


    def add_filter(self, symbol, f):
        self.filters[symbol].append(f)
        funcname = sys._getframe().f_code.co_name
        logger.log(logging.DEBUG, funcname + ':' + self.print_filter(symbol))

    def apply_filter(self, quote):

        msg = ''
        funcname = sys._getframe().f_code.co_name

        logger.log(logging.DEBUG, msg)    
        return msg


    def print_filter(self, symbol):
        msg = ''
        return msg

    def print_all_filters(self):
        msg = ''
        for symbol in self.filters:
            msg += self.print_filter(symbol)

        return msg
            

    def delete_filter(self, symbol):
       if symbol in self.filters:
           del self.filters[symbol]

    def delete_all_filters(self):
        for symbol in self.filters:
            self.delete_filter(symbol)
