#!/usr/bin/env python3
"""
inspired by: https://github.com/yantisj/tcpping
TCP Ping Test (defaults to port 80, 10000 packets)
"""

import socket
from timeit import default_timer as timer


class TcpPing:
    ERROR_NONE = 0
    ERROR_OS = 1
    ERROR_TIME_OUT = 2

    last_error = ERROR_NONE
    last_os_error_message = None
    verbose = False

    @staticmethod
    def get_last_error_readable():
        return {
            TcpPing.ERROR_NONE: 'NO ERROR',
            TcpPing.ERROR_OS: 'OS ERROR',
            TcpPing.ERROR_TIME_OUT: 'Connection timed out!',
        }[TcpPing.last_error]

    @staticmethod
    def get_last_os_error_message_readable():
        if TcpPing.last_os_error_message:
            return str(TcpPing.last_os_error_message)

        return ''

    @staticmethod
    def ping(host, port, timeout):
        TcpPing.last_os_error_message = None

        delay = -1

        # New Socket
        s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        # X sec Timeout
        s.settimeout(timeout)

        # Start a timer
        s_start = timer()

        # Try to Connect
        try:
            s.connect((host, port))
            s.shutdown(socket.SHUT_RD)

            TcpPing.last_error = TcpPing.ERROR_NONE

            s_stop = timer()

            delay = s_stop - s_start

        # Connection Timed Out
        except socket.timeout:
            TcpPing.last_error = TcpPing.ERROR_TIME_OUT
        except OSError as e:
            TcpPing.last_error = TcpPing.ERROR_OS
            TcpPing.last_os_error_message = e

        if delay == -1 and TcpPing.verbose:
            print(TcpPing.get_last_error_readable(), TcpPing.get_last_os_error_message_readable())

        return delay


if __name__ == "__main__":

    # test against google
    print('Time: {0} state: {1}'.format(
        TcpPing.ping('www.google.com', 80, 2),
        TcpPing.get_last_error_readable()
    ))
    if TcpPing.last_error:
        print(TcpPing.last_os_error_message)

    # test verbose against broken host name
    TcpPing.verbose = True
    print('Time: {0} state: {1}'.format(
        TcpPing.ping('https://www.google.com', 80, 2),
        TcpPing.get_last_error_readable()
    ))
    if TcpPing.last_error:
        print(TcpPing.last_os_error_message)
