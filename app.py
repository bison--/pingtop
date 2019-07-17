import PingTop
import os


HOST = os.getenv('HOST', '8.8.8.8')

pt = PingTop.PingTop(HOST)
pt.run()
