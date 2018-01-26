# -*- encoding: utf-8
import time
import psutil
import socket
import sys
import thread


reload(sys)
sys.setdefaultencoding('utf-8')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

'''
require python-devel.x86_64, psutil
yum install python-devel.x86_64 -y
pip install psutil
'''


def login_check():
    login = psutil.users()
    while True:
        message = ''
        current_login = psutil.users()
        if len(login) < len(current_login):
            new_login = set([x.host for x in current_login]) - set([x.host for x in login])
            message = ", ".join(list(new_login)) + " just login"
            login = psutil.users()
        if len(login) > len(current_login):
            new_login = set([x.host for x in login]) - set([x.host for x in current_login])
            message = (", ".join(list(new_login)) + " logout")
            login = psutil.users()
        if message:
            print message
            s.sendto(message, ('115.238.145.72', 40002))
        time.sleep(0.2)


if __name__ == "__main__":
    send_message = []
    login = psutil.users()
    last_send_time = 0
    thread.start_new_thread(login_check, ())

    while True:
        # cpu info
        cpu_percent = psutil.cpu_percent(4)
        if cpu_percent > 75:
            send_message.append(u"警告: CPU使用率即将过载%s" % cpu_percent)

        # memory
        free = round(psutil.virtual_memory().free/(1024.0*1024.0*1024.0), 2)
        if free < 3:
            send_message.append(u"警告: 内存不足%sG" % free)

        # login
        if ((time.time()-last_send_time) > 600) and send_message:
            content = "\r\n".join(send_message)
            print content
            s.sendto(str(content), ('115.238.145.72', 40002))
            last_send_time = time.time()
        send_message = []
        login = psutil.users()
        time.sleep(3)

