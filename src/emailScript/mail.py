# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
邮件发送

"""

if __name__ == '__main__':
    from load import eInfo
    from tools import *

else:
    from src.emailScript.load import eInfo
    from src.emailScript.tools import *

from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from colorama import init, Fore, Back, Style
import smtplib
from src.emailScript.filepath import *



class MailText(object):
    """
    """
    
    def __init__(self, mailtext, info):
        """
        :param mailtext: dict, mailText in load modules
        :param info: user info.json dict
        """
        self.fromemail = info['user-email']
        self.smtpserver = info['smtp-server']
        self.smtppport = info['port']
        self.smtppassword = info['password']

        # 判断text项
        if 'text' not in mailtext.keys():
            self.text = ''
            printWarning('email warning', 'email text is empty')

            if check_json_Setting('C:/Program Files/pyemail/settings.json', 'ignore-warnings') == False:
                quit_or_continue()
        else:
            self.text = mailtext['text']

        # 判断title项
        if 'title' not in mailtext.keys():
            self.title = ''
            printWarning('email warning', 'email has no title')

            if check_json_Setting('C:/Program Files/pyemail/settings.json', 'ignore-warnings') == False:
                quit_or_continue()
        else:
            self.title = mailtext['title']

        # name项
        if 'name' not in mailtext.keys():
            if 'default-name' in eInfo.keys() and info['default-name'] != '':
                self.name = info['default-name']
            else:
                self.name = ''
        else:
            self.name = mailtext['name']

        # toname项
        if 'toname' not in mailtext.keys():
            self.toname = ''
        else:
            self.toname = mailtext['toname']

        if 'email' not in mailtext.keys():
            printError('email error', 'no email address to send')
            exit(0)

        self.email = mailtext['email']
        self.type = mailtext['type']
                

    def _format(self, s):
        """
        格式化
        """
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    def toMsg(self):
        """
        将mailtext dict转换成MIMEText格式
        """
        msg = MIMEText(self.text, self.type, 'utf-8')
        msg['From'] = self._format('%s <%s>' % (self.name, self.fromemail))
        msg['To'] = self._format('%s <%s>' % (self.toname, self.email))
        msg['Subject'] = Header(self.title, 'utf-8').encode()

        return msg


    def send(self):
        """
        发送邮件
        """
        # 获取转换后的msg文本
        Msg = self.toMsg()

        try:
            if eInfo['ssl'] == True:
                server = smtplib.SMTP_SSL(self.smtpserver, self.smtppport)
            else:
                server = smtplib.SMTP(self.smtpserver, self.smtppport)
        except :
            printError('send error', 'send error')
            exit(0)

        try:
            server.login(self.fromemail, self.smtppassword)
        except :
            printError('login error', 'Authentication failed')
            exit(0) 

        try:
            server.sendmail(from_addr=self.fromemail, to_addrs=__import__('re').split(r'\s*\,\s*', self.email), msg=Msg.as_string())
            server.quit()
        except :
            printError('send error', 'send error')
            exit(0)

        printSuccess('send successfully')

