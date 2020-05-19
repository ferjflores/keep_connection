import daemon
import socket
import logging
import lockfile
from time import sleep

REMOTE_SERVER_NAME = "one.one.one.one"
REMOTE_SERVER_IP = "1.1.1.1"
REMOTE_SERVER_ISP = "200.44.32.12"
logging.basicConfig(filename='/tmp/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def is_connected(hostname):
    logging.warning('This will get logged to a file')
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception as error:
        print(error)
    return False

#
# with daemon.DaemonContext(pidfile=lockfile.FileLock('/tmp/check_connection.pid')) as d:
#     print('adsssssssss')
#     d.open()
#     while True:
#         connected = False
#         if is_connected(REMOTE_SERVER_NAME):
#             print("DNS working")
#             logging.info("working")
#             connected = True
#
#         if is_connected(REMOTE_SERVER_IP):
#             print("Working IP")
