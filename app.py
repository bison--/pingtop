from modules import PingTop
import os


HOST = os.getenv('HOST', '8.8.8.8')
PING_MODE = int(os.getenv('PING_MODE', '1'))
TCP_PING_PORT = int(os.getenv('TCP_PING_PORT', '80'))

pt = PingTop.PingTop(HOST)
pt.ping_mode = PING_MODE
pt.tcp_ping_port = TCP_PING_PORT

pt.run()
