import platform


class PingShell:
    OS_NOT_DETECTED = 0
    OS_LIN = 1
    OS_WIN = 2
    OS_MAC = 3

    CURRENT_OS = OS_NOT_DETECTED

    @staticmethod
    def get_os(enforce_detection=False):
        if not enforce_detection and PingShell.CURRENT_OS > PingShell.OS_NOT_DETECTED:
            return PingShell.CURRENT_OS

        system = platform.system()
        if system == 'Windows':
            PingShell.CURRENT_OS = PingShell.OS_WIN
        elif system == 'Darwin':
            PingShell.CURRENT_OS = PingShell.OS_MAC
        else:
            # we assume that everything else might be linux or like enough
            PingShell.CURRENT_OS = PingShell.OS_LIN

        return PingShell.CURRENT_OS

    @staticmethod
    def ping(host, timeout):
        if PingShell.get_os() == PingShell.OS_WIN:
            return PingShell._ping_win(host, timeout)
        else:
            # TODO: check if the Mac-ping works like the Linux ping
            return PingShell._ping_linux(host, timeout)

    @staticmethod
    def _ping_linux(host, timeout):
        import subprocess
        import re

        avg_rtt = ''
        ping = subprocess.Popen(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            [out, _] = ping.communicate(timeout=timeout)
            # print(out)
            if ping.returncode == 0:
                re_result = re.search(r"rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out))
                avg_rtt = re_result.group(1)
        except subprocess.TimeoutExpired:
            ping.kill()

        try:
            return float(avg_rtt) / 1000
        except ValueError:
            return -1

    @staticmethod
    def _ping_win(host, timeout):
        import subprocess
        import re

        avg_rtt = ''
        ping = subprocess.Popen(["ping", "-n", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            [out, _] = ping.communicate(timeout=timeout)
            # print(out)
            if ping.returncode == 0:
                re_result = re.search("=([0-9]*)ms", str(out))

                # none can happen when the ping does something unexpected
                if re_result is None:
                    return -1

                avg_rtt = re_result.group(1)
        except subprocess.TimeoutExpired:
            ping.kill()

        try:
            return float(avg_rtt) / 1000
        except ValueError:
            return -1


if __name__ == "__main__":
    print('Time: {0}'.format(
        PingShell.ping('www.google.com', 1),
    ))
