# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
python 邮件客户端
:module: load
加载用户配置文件及邮件正文文件，邮件正文是一个字典，格式如下：

+-------+-----------------------+
|email  | 发送对象的邮箱          
+-------+-----------------------+
|title  | 邮件标题               
+-------+-----------------------+
|name   | 发送者姓名             
+-------+-----------------------+
|toname | 接收者姓名
+-------+-----------------------+
|type   | 邮件类型
+-------+-----------------------+
|text   | 邮件正文
+-------+-----------------------+
"""
import json
import re
import os
import platform
from colorama import init, Fore, Back, Style

if __name__ != '__main__':
    from src.emailScript.tools import check_server_connect, printError, printSuccess, check_json_Setting
    from src.emailScript.filepath import *

else:
    from tools import check_server_connect, printError, check_json_Setting


init(autoreset=True)

pltform = platform.system()

# json信息，全局变量
eInfo = {}



def _open_file_in_system_edit(fname):
    """
    使用系统默认编辑器打开文件
    Windows 下为 notepad
    Linux 下为 gedit
    """
    assert fname and isinstance(fname, (str, ))

    if pltform == 'Windows':
        os.system('notepad %s' % fname)

    elif pltform == 'Linux':
        os.system('gedit %s' % fname)



def open_file_in_edit(fname, editer=''):
    """
    直接在编辑器中打开文件
    :param: str, filename
    :return: None
    """
    assert fname and isinstance(fname, (str, ))

    if editer != '':

        try:
            os.system(editer + ' ' + fname)
        except :
            _open_file_in_system_edit(fname)
    else:
        _open_file_in_system_edit(fname)



def load_user_info():
    """
    加载用户配置文件 info.json中的用户信息
    :return: user information dict
    """
    info = {'user-email': 'your email address',
            'password': 'your email password',
            'smtp-server': 'smtp server address',
            'port': 25,
            'default-name': 'default name in email',
            'default-editer': '',
            'ssl': False,
            'save_log': True}

    try:
        with open(infofile, 'r', encoding='utf-8') as f:
            info = json.load(f)
            # 检查info.json配置是否缺失
            if {'user-email', 'password', 'smtp-server', 'port', 'default-name', 'default-editer', 'ssl'} > set(info.keys()):
                printError('info json error', 'some information lost, delete info.json and try again')
                exit(0)

            return info

    except FileNotFoundError:

        # 文件夹不存在则创建文件夹
        if not os.path.exists(_path):
            os.mkdir(_path)

        print('Please set up info.json file first')
        print('请先设置 info.json 文件')

        with open(infofile, 'w') as f:

            json.dump(info, f, indent=4)

        open_file_in_edit(infofile)
        exit(0)



def _read_file(fname):
    """
    文本读取迭代器
    """
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()

                if line:
                    yield line
                else:
                    return line
    except FileNotFoundError:
        exit(0)



def _load_email_text_file(fname):
    """
    加载 .email .txt格式的文本
    """
    assert fname and isinstance(fname, (str, ))
    mailText = {}
    text = ''

    for line in _read_file(fname):
        # mail文本命令格式
        if re.match(r'\s*\#[a-zA-Z]+\s+(.+)', line):

            keyword = re.match(r'\s*\#([a-zA-Z]+)\s+', line).group(1).lower()
            value = re.match(r'\s*\#[a-zA-Z]+\s+(.+)', line).group(1)

            mailText[keyword] = value
        else:

            text = text + line

    mailText['text'] = text

    return mailText



def show_email_text(mailtext):
    """
    展示main text dict
    如果要显示邮件正文信息，需在settings.json中加上 show-text项，值为 true
    :param mailtext: mailtext dict
    """
    # 计算字符串占用字节长度
    charlen = lambda s: len(s) + (len(s.encode()) - len(s)) // 2
    length = max([charlen(value) for k, value in mailtext.items() if k != 'text']) + 5
    
    for key in mailtext.keys():

        if key in {'email', 'title', 'name', 'toname'}:

            line = Fore.CYAN + ' %s' % mailtext[key]
            print('+-----------+' + length * '-' + '+')
            print('|' + key + (11 - charlen(key)) * ' ' + '|' + line + Style.RESET_ALL + (length - charlen(line) + 5) * ' ' + '|')

    print('+-----------+' + length * '-' + '+')

    # 是否显示文本
    isShowText = check_json_Setting(settingfile, 'show-text')

    if isShowText != 'jsonLoadOrReadError' and isShowText == True:

        # 将文本一行一行打印输出
        textlines = mailtext['text'].split('\n')
        length = max(list(map(charlen, textlines))) + 3
        print('\n+' + length * '-' + '+')
        print('|text' + (length - 4) * ' ' + '|')

        for line in textlines:
            print('|' + Fore.CYAN + line + (length - charlen(line)) * ' ' + Style.RESET_ALL + '|')

        print('+' + length * '-' + '+')



def load_email_text(fname):
    """
    加载邮件正文文件
    邮件正文可以 .txt .html，抑或专用的 .email 支持特定语法
    """
    assert fname and isinstance(fname, (str, ))

    # 获取文件扩展名
    fileType = re.split(r'\s*\.\s*', fname)[-1]
    # 邮件信息
    mailText = {}

    if fileType in {'email', 'txt'}:
        mailText = _load_email_text_file(fname)
        mailText['type'] = 'plain'

    # 邮件文件加载成功，输出调试
    printSuccess('load successfully')
    #show_email_text(mailText)

    return mailText



def load_command():
    """
    加载启动命令，决定是否进入交互模式
    如果命令长度为 0 则进入交互模式
    """
    cmd = []

    try:
        tempfile = ""

        with open('C:\\Program Files\\pyemail\\target.~', 'r', encoding='utf-8') as f:
            tempfile = f.readline().strip('\n') + '\\temp.~'

        cmd = [c.strip('\n') for c in _read_file(tempfile)]

        try:
            # 删掉临时文件
            if pltform == 'Windows':
                os.system('del ' + tempfile)
            elif pltform == 'Linux':
                os.system('rm ' + tempfile)
        except:
            pass

    except :
        print('交互模式..')

    if len(cmd) == 0:
        print('交互模式..')

    return cmd


# def main():
# 在这里读入用户信息，其它文件import此变量
eInfo = load_user_info()


if __name__ == '__main__':

    load_user_info() 