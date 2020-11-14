# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
先判断网络是否正常；如果网络正常则检查依赖环境是否正常；
若网络连接正常且依赖环境缺失则安装依赖环境
若网络连接不正常且环境缺失则提示用户安装
"""

import os
import socket
import json
from src.emailScript.tools import check_server_connect
from src.emailScript.filepath import *

__all__ = ['load', 'mail']

settings = {}

# 尝试打开settings.json
try:

    if not os.path.exists(settingfilepath):
        os.mkdir(settingfilepath)
        
    with open(settingfile, 'r') as f:
        settings = json.load(f)

except :
    settings['pack-loss'] = True


networkcorrect = False

if settings['pack-loss'] == False:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

networkcorrect = check_server_connect('www.baidu.com', 443)
check_server_connect('smtp.stu.neu.edu.cn', 25)

# 网络连接有问题
if networkcorrect == False:

    if settings['pack-loss'] == False:        
        print(Fore.RED + Style.DIM + '-[network error] please check your network connect')

    else:
        print('-[network error] please check your network connect')

    exit(0)


# 缺失依赖项
if settings['pack-loss'] == True:
    import re
    p = os.popen('pip list')
    needpacklist = {'requests', 'colorama', 'PyEmail', 'emails'}
    packlist = []

    while True:
        s = p.readline()
        if s == '':
            break
        m = re.match(r'([a-zA-Z0-9]+)\s+\d+\.', s)

        if m:
            packlist.append(m.group(1))

    installpacklist = needpacklist - set(packlist)

    if len(installpacklist) == 0:
        settings['pack-loss'] = False

    else:

        print('-[missing dependencies] try to install')
        print('-[missing pack list] ', installpacklist)

        for pack in installpacklist:
            print('+[installing] %s' % pack)
            os.system('pip install ' + pack)
            
        settings['pack-loss'] = False


with open(settingfile, 'w') as f:
    json.dump(settings, f, indent=4)


if __name__ == '__main__':
    pass
