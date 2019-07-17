import socket
import time
from datetime import datetime


class PingTop:
    PING_MODE_PYTHON = 1
    PING_MODE_SHELL = 2

    def __init__(self, ping_address="8.8.8.8"):
        self.time_out = 10
        self.max_history = 75
        self.sleep = 1.0
        self.time_list = []
        self.ping_address = ping_address
        self.active = True
        self.ping_method = PingTop.PING_MODE_SHELL
        self.renderer = RenderPing(self.ping_address)
        self.total_pings = 0
        self.total_errors = 0
        self.total_time = 0
        self.started = time.time()

    def ping(self):
        if self.ping_method == PingTop.PING_MODE_SHELL:
            delay = self._ping_shell()
        elif self.ping_method == PingTop.PING_MODE_PYTHON:
            delay = self._ping_python()
        else:
            raise Exception('PING method not implemented.')

        self.total_pings += 1

        if delay >= 0:
            self.total_time += delay
        else:
            self.total_errors += 1

        self.time_list.append(delay)

        if len(self.time_list) > self.max_history:
            del self.time_list[0]

    def _ping_python(self):
        # this does NOT work properly or reliable with a broken connection
        import ping3
        delay = -1
        try:
            delay = ping3.ping(self.ping_address, timeout=self.time_out, unit='s')
            # print(delay)
        except socket.error as ex:
            print(ex)

        return delay

    def _ping_shell(self):
        import subprocess
        import re

        avg_rtt = ''
        ping = subprocess.Popen(["ping", "-c", "1", self.ping_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            [out, err] = ping.communicate(timeout=self.time_out)
            # print(out)
            if ping.returncode == 0:
                re_result = re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out))
                avg_rtt = re_result.group(1)
        except subprocess.TimeoutExpired as ex:
            ping.kill()

        try:
            return float(avg_rtt) / 100
        except ValueError:
            return -1

    def do_render(self):
        self.renderer.render(self.time_list, self.started, self.total_pings, self.total_errors)

    def run(self):
        while self.active:
            self.ping()
            self.do_render()
            if self.sleep > 0:
                time.sleep(self.sleep)


class RenderPing:

    def __init__(self, host_name):
        self.host_name = host_name
        self.renderHeight = 10
        self.renderWidth = 75
        self._output_rows = [' '] * 10

    def render(self, time_list, started, total_pings, total_errors):
        # print(timeList)
        self._output_rows = [' '] * 10
        longest_time = 0
        shortest_time = 0
        all_combined = 0
        all_combined_count = 0
        error_count = 0

        for duration in time_list:
            if duration > longest_time:
                longest_time = duration

            if duration > 0:
                if duration < shortest_time or shortest_time == 0:
                    shortest_time = duration

                all_combined += duration
                all_combined_count += 1
            elif duration == -1:
                error_count += 1

        for duration in time_list:
            printable_val = 0
            if duration > 0:
                percentage_of_max = RenderPing.get_percentage(duration, longest_time)
                printable_val = int(percentage_of_max)
            else:
                printable_val = duration

            self.add_column(printable_val)

        average = 0
        if all_combined_count > 0:
            average = all_combined / all_combined_count

        print('\x1b[2J')
        print("\033[0;0H")

        if self.host_name is not '':
            print(" ## HOST: {0} | started at {1} | runtime  {2}".format(
                self.host_name,
                datetime.fromtimestamp(started).strftime('%Y-%m-%d %H:%M:%S'),
                (datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(started))
            ))

        for row in reversed(self._output_rows):
            print(row)

        print(" Longest:  {: 10.5f}".format(longest_time))
        print(" Shortest: {: 10.5f}".format(shortest_time))
        print(" Average:  {: 10.5f}".format(average))
        print(" ERROR:        {: 6}".format(error_count))
        print(" ERRORS TOTAL: {: 6}".format(total_errors))
        print(" PINGS TOTAL:  {: 6}".format(total_pings))
        print(" ERROR RATE:  {: 6.2f}%".format(RenderPing.get_percentage(total_errors, total_pings)))

    def add_column(self, height):
        bar_char = '#'
        mod_height = 10
        if height < 100.0:
            mod_height = int(height / 10) - 1

        if height == -1:
            bar_char = 'X'
            mod_height = 1
        elif mod_height <= 0:
            mod_height = 1

        for row in range(10):
            if row < mod_height:
                self._output_rows[row] += bar_char
            else:
                self._output_rows[row] += ' '

    @staticmethod
    def get_percentage(_val, _max_val):
        return (_val * 100) / _max_val


if __name__ == "__main__":
    pt = PingTop()
    pt.ping()
    pt.ping()
    pt.ping()
    pt.ping()
    pt.do_render()
