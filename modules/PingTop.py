from modules.RenderPing import RenderPing
import socket
import time


class PingTop:
    PING_MODE_SHELL = 1
    PING_MODE_TCP_PING = 2
    PING_MODE_PYTHON = 3

    def __init__(self, ping_host="8.8.8.8"):
        self.time_out = 10
        self.max_history = 75
        self.sleep = 1.0
        self.time_list = []
        self.ping_host = ping_host
        self.active = True
        self.ping_mode = PingTop.PING_MODE_SHELL
        self.tcp_ping_port = 80
        self.renderer = RenderPing(self.ping_host)
        self.total_pings = 0
        self.total_errors = 0
        self.total_time = 0
        self.started = time.time()
        self.save_log_path = ''

    @staticmethod
    def get_ping_modes():
        return {
            PingTop.PING_MODE_PYTHON: 'python module',
            PingTop.PING_MODE_SHELL: 'shell (system ping)',
            PingTop.PING_MODE_TCP_PING: 'TCP PING (needs a host with an open port, default: 80)',
        }

    @staticmethod
    def get_ping_modes_readable(separator="\n"):
        ret = ''
        for _id, _label in PingTop.get_ping_modes().items():
            ret += "{0}: {1}{2}".format(_id, _label, separator)

        return ret

    def ping(self):
        if self.ping_mode == PingTop.PING_MODE_SHELL:
            delay = self._ping_shell()
        elif self.ping_mode == PingTop.PING_MODE_PYTHON:
            delay = self._ping_python()
        elif self.ping_mode == PingTop.PING_MODE_TCP_PING:
            delay = self._ping_tcp_ping()
        else:
            raise Exception('PING method not implemented.')

        self.total_pings += 1

        if delay >= 0:
            self.total_time += delay
            self._log_ping(delay, False)
        else:
            self.total_errors += 1
            self._log_ping(delay, True)

        self.time_list.append(delay)

        if len(self.time_list) > self.max_history:
            del self.time_list[0]

    def _ping_python(self):
        # this does NOT work properly or reliable with a broken connection
        try:
            import ping3
        except ImportError:
            print('TO USE THE PYTHON PING-METHOD YOU HAVE TO INSTALL ping3')
            print('("pip3 install ping3") https://pypi.org/project/ping3/')
            print('Then this program also hast to be run as root (on most systems)')
            print('It also does NOT work properly or reliable with a broken connection')
            import sys
            sys.exit(1)

        delay = -1
        try:
            delay = ping3.ping(self.ping_host, timeout=self.time_out, unit='s')
            # print(delay)
        except socket.error as ex:
            print(ex)

        return delay

    def _ping_shell(self):
        from modules.PingShell import PingShell
        return PingShell.ping(self.ping_host, self.time_out)

    def _ping_tcp_ping(self):
        from modules.TcpPing import TcpPing
        return TcpPing.ping(self.ping_host, self.tcp_ping_port, self.time_out)

    def _log_ping(self, delay, was_error):
        if self.save_log_path:
            import datetime

            log_line = '{0},{1},{2}\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                delay,
                was_error
            )

            file_handle = open(self.save_log_path, 'a+')
            file_handle.write(log_line)
            file_handle.flush()
            file_handle.close()

    def do_render(self):
        self.renderer.render(self.time_list, self.started, self.total_pings, self.total_errors)

    def run(self):
        while self.active:
            self.ping()
            self.do_render()
            if self.sleep > 0:
                time.sleep(self.sleep)


if __name__ == "__main__":
    pt = PingTop()
    pt.ping()
    pt.ping()
    pt.ping()
    pt.ping()
    pt.do_render()
