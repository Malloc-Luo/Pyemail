# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
pyemail version = 0.2.0
"""

from src.emailScript.load import eInfo, check_server_connect, show_email_text
from src.emailScript.load import load_command, load_email_text, open_file_in_edit
from src.emailScript.tools import printError
from src.emailScript.mail import MailText
from src.emailScript.filepath import *

import re


def _parsing_send_email(cmd):
    """
    解析发送命令
    :return: 解析后生成的email文件
    """
    if len(cmd) == 0:
        # 缺少参数
        printError('command error', 'missing arguments')
        exit(0)

    file = cmd.pop(0)

    # 检测指定文件是否存在
    try:
        f = open(file, 'r')
        f.close()
    except :
        # 未找到文件
        printError('email file error', 'email file \'%s\' not found' % file)
        exit(0)

    # 加载邮件
    mail = load_email_text(file)

    if len(cmd) == 0:
        return mail

    elif len(cmd) != 0:
        # 获取一个命令
        c = cmd.pop(0).lower()

        if c not in {'to', 'add', '-t', '-a'}:
            # 命令错误
            printError('command error', 'command \'%s\' not found' % c)
            exit(0)

        else:
            # 发送到
            if len(cmd) == 0:
                # 缺少命令参数
                printError('command error', 'missing arguments')
                exit(0)

            else:
                e = cmd.pop(0)
                emailaddr = re.split(r'\s*\,\s*', e)

                if c in {'add', '-a'} and 'email' in mail.keys():
                    emailaddr = emailaddr + re.split(r'\s*\,\s*', mail['email'])

                illegalemail = []

                for email in emailaddr:
                    if not re.match(r'^[a-zA-Z0-9\_\-]+@[a-zA-Z0-9\_\-]+(\.[a-zA-Z0-9\_\-]+)+$', email):
                        illegalemail.append(email)

                # 确保每一个邮箱格式都合法
                if len(illegalemail) == 0:
                    sendemail = ','.join(emailaddr)
                    mail['email'] = sendemail

                else:
                    # 打印出这些格式错误的邮箱
                    printError('email format error', 'illegal email address format')
                    for email in illegalemail:
                        printError('email', email)

                    exit(0)

    return mail


def parsing_instruction(cmd):
    """
    解析输入命令并执行
    :param cmd: 命令
    """
    c = cmd.pop(0).lower()

    if c in {'send', '-s'}:

        check_server_connect('www.baidu.com', 443)
        # 检查smtp服务器
        if check_server_connect(eInfo['smtp-server'], int(eInfo['port'])) == False:

            printError('server error', 'smtp server error, check your smtp server')
            exit(0)

        mail = _parsing_send_email(cmd)
        show_email_text(mail)
        MailText(mail, eInfo).send()

    elif c in {'setting', '-st'}:
        open_file_in_edit(settingfile, eInfo['default-editer'])

    elif c in {'info', '-i'}:
        open_file_in_edit(infofile, eInfo['default-editer'])

    elif c in {'version', '-v'}:
        print(__import__('colorama').Fore.BLUE + __doc__)

    else:
        # 不存在的指令
        printError('command error', 'command \'%s\' not found' % c)
        exit(0)


def main():

    # 加载输入命令
    cmd = load_command()
    return cmd

 
if __name__ == '__main__':

    cmd = main()
    parsing_instruction(cmd)
