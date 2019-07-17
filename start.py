import PingTop
import argparse

parser = argparse.ArgumentParser(description='show a PING graph for a specified host. '
                                             '8.8.8.8 is default if none is specified.')

parser.add_argument('--host',
                    type=str,
                    dest='host',
                    default='8.8.8.8',
                    help='specify the HOST to ping, name or IP')

args = parser.parse_args()

pt = PingTop.PingTop(args.host)
pt.run()