#!/usr/bin/python3
from modules import PingTop
import argparse

parser = argparse.ArgumentParser(description='show a PING graph for a specified host. '
                                             '8.8.8.8 is default if none is specified.',
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--host',
                    type=str,
                    dest='host',
                    default='8.8.8.8',
                    help='specify the HOST to ping, name or IP'
                    )

parser.add_argument('--mode',
                    type=int,
                    dest='ping_mode',
                    default=PingTop.PingTop.PING_MODE_SHELL,
                    help='what ping method to use, available:\n' + PingTop.PingTop.get_ping_modes_readable(),
                    )

parser.add_argument('--port',
                    type=int,
                    dest='tcp_ping_port',
                    default=80,
                    help='the port TCP PING should connect',
                    )

parser.add_argument('--log',
                    type=str,
                    dest='save_log_path',
                    default='',
                    help='the full or relative PATH where the log should be written to\n' +
                         'Examples:\n' +
                         '--log pingtest.csv\n' +
                         '--log /var/logs/pingtest.csv\n',
                    )

args = parser.parse_args()

pt = PingTop.PingTop(args.host)
pt.ping_mode = args.ping_mode
pt.tcp_ping_port = args.tcp_ping_port
pt.save_log_path = args.save_log_path

pt.run()
