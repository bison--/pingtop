import time
import statistics
from datetime import datetime


class RenderPing:

    def __init__(self, host_name):
        self.host_name = host_name
        self.mode_name = ''
        self.mode_id = 0
        self.mode_port = 0

        # you can configure the output chart, maybe with some nice colors
        self.bar_char_value = '#'
        self.bar_char_error = 'X'
        self.bar_char_blank = ' '

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

        # fill bar with empty values
        for _ in range(self.renderWidth - len(time_list)):
            self.add_column(-2)

        times_bigger_zero = []

        for duration in time_list:
            printable_val = 0
            if duration > 0:
                percentage_of_max = RenderPing.get_percentage(duration, longest_time)
                printable_val = int(percentage_of_max)
                times_bigger_zero.append(duration)
            else:
                printable_val = duration

            self.add_column(printable_val)

        average = 0
        if all_combined_count > 0:
            average = all_combined / all_combined_count

        median = 0
        deviation = 0
        if len(times_bigger_zero) >= 2:
            median = statistics.median(times_bigger_zero)
            deviation = statistics.stdev(times_bigger_zero)

        print('\x1b[2J')
        print("\033[0;0H")

        if self.host_name != '':
            port_string = ''
            if self.mode_id == 2:
                port_string = 'port: {0}'.format(self.mode_port)

            print(" ## HOST: {0} | MODE {2}: {1} {3}".format(
                self.host_name,
                self.mode_name,
                self.mode_id,
                port_string
            ))

            print(" ## started at {0} | runtime {1}".format(
                datetime.fromtimestamp(started).strftime('%Y-%m-%d %H:%M:%S'),
                (datetime.fromtimestamp(int(time.time())) - datetime.fromtimestamp(int(started)))
            ))

        for row in reversed(self._output_rows):
            print(row)

        print(" Last PING:   {: 10.5f}".format(time_list[-1]), end=' '*5)
        print(" Average:     {: 10.5f}".format(average))

        print(" Longest:     {: 10.5f}".format(longest_time), end=' '*5)
        print(" Shortest:    {: 10.5f}".format(shortest_time))

        print(" median:      {: 10.5f}".format(median), end=' ' * 5)
        print(" s.deviation: {: 10.5f}".format(deviation))

        print(" ERROR:           {: 6}".format(error_count))
        print(" ERRORS TOTAL:    {: 6}".format(total_errors))
        print(" PINGS TOTAL:     {: 6}".format(total_pings))
        print(" ERROR RATE:     {: 6.2f}%".format(RenderPing.get_percentage(total_errors, total_pings)))

    def add_column(self, height):
        """
        adds a data column to the graph
        :param height: the height of the column
        0 to n: a measured value
        -1: ERROR: any error that has occurred
        -2: NO DATA: used to fill the chart with empty space
        :type height: float
        """
        bar_char = self.bar_char_value
        mod_height = 10
        if height < 100.0:
            mod_height = int(height / 10) - 1

        if height == -1:
            bar_char = self.bar_char_error
            mod_height = 1
        elif height == -2:
            bar_char = self.bar_char_blank
            mod_height = 1
        elif mod_height <= 0:
            mod_height = 1

        for row in range(10):
            if row < mod_height:
                self._output_rows[row] += bar_char
            else:
                self._output_rows[row] += self.bar_char_blank

    @staticmethod
    def get_percentage(_val, _max_val):
        return (_val * 100) / _max_val
