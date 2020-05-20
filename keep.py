#!/usr/bin/python3

import logging
import time
from daemon import runner
from library import check_dns_resolution, is_connected, reset

REMOTE_SERVER_NAME = "one.one.one.one"
REMOTE_SERVER_IP = "1.1.1.1"
# DEFAULT_ROUTER_URL = "http://localhost:9080"
DEFAULT_ROUTER_URL = "http://192.168.88.1"
DEFAULT_ADMIN_PW = "admin"


class Runner(runner.DaemonRunner):
    def _open_streams_from_app_stream_paths(self, app):
        self.daemon_context.stdin = open(app.stdin_path, 'rt')
        self.daemon_context.stdout = open(app.stdout_path, 'wb+', buffering=0)
        self.daemon_context.stderr = open(app.stderr_path, 'wb+', buffering=0)


class App:
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/keep_connection.pid'
        self.pidfile_timeout = 5
        self.url = DEFAULT_ROUTER_URL
        self.password = DEFAULT_ADMIN_PW
        self.restart = True

    def run(self):
        i = 0
        while True:
            check_dns, message = check_dns_resolution(REMOTE_SERVER_NAME)
            logger.info(message)
            check_connection, message = is_connected(REMOTE_SERVER_IP)
            logger.info(message)

            if not check_connection and self.restart:
                logger.warning("reset connection")
                message = reset(self.url, self.password)
                logger.info(message)
            else:
                logger.info("Connection working")
            time.sleep(300)


if __name__ == '__main__':
    app = App()
    logger = logging.getLogger("keep_connection")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
    handler = logging.FileHandler("/tmp/keep_connection.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    serv = Runner(app)
    serv.daemon_context.files_preserve = [handler.stream]
    serv.do_action()
