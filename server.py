#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *
from multiprocessing import Process, Queue
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


HOST = ''
PORT = 40002
BUFSIZ = 1024
ADDR = (HOST, PORT)

# SOCK_DGRAM 是UDP协议，socket初始化默认值：family=AF_INET, type=SOCK_STREAM, proto=0, _sock=None
udpServer = socket(AF_INET, SOCK_DGRAM)
udpServer.bind(ADDR)

queue = Queue()                  # define queue to save udp data


class Email(object):
    def __init__(self, from_addr, password, smtp_server, to_addr):
        self.from_addr = from_addr   # Email地址和口令:
        self.password = password
        self.smtp_server = smtp_server         # SMTP服务器地址:
        self.to_addr = to_addr       # 件人地址
        self.msg = ''
        self.server = ''

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def set_msg(self, content):
        self.msg = MIMEText(content, 'plain', 'utf-8')
        self.msg['From'] = self._format_addr(u'MonitorCentor<%s>' % self.from_addr)
        self.msg['To'] = self._format_addr(u'linux管理员 <%s>' % self.to_addr)
        self.msg['Subject'] = Header(u'资源监控告警', 'utf-8').encode()

    def send(self):
        self.server = smtplib.SMTP(self.smtp_server, 25)               # SMTP协议默认端口是25
        self.server.set_debuglevel(1)
        self.server.login(self.from_addr, self.password)
        self.server.sendmail(self.from_addr, self.to_addr, self.msg.as_string())
        self.server.quit()


def consume():
    while True:
        if not queue.empty():
            content = queue.get()
            print content
            email = Email('send_email', 'passwd', 'smtp.163.com', ['recv_email_1', 'recv_email_2'])
            email.set_msg(content)
            email.send()
        time.sleep(2)


def main():
    handler = Process(target=consume, args=())
    handler.start()

    while True:
        eip_mapping, addr = udpServer.recvfrom(BUFSIZ)
        queue.put(eip_mapping)


if __name__ == "__main__":
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        # 产生子进程，而后父进程退出
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
    # 修改子进程工作目录
    os.chdir("/")

    # 创建新的会话，子进程成为会话的首进程
    os.setsid()

    # 修改工作目录的umask
    os.umask(0)

    try:
        # 创建孙子进程，而后子进程退出
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # 刷新缓冲区先，小心使得万年船
    sys.stdout.flush()
    sys.stderr.flush()

    # 孙子进程的程序内容
    main()
