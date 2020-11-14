# -*- coding: utf-8 -*-
# !/usr/bin/python

_username = __import__('getpass').getuser()

# settings.json路径
settingfile = 'C:/Users/%s/AppData/Local/pyemail/settings.json' % _username

# 文件夹路径
settingfilepath = 'C:/Users/%s/AppData/Local/pyemail' % _username

# info.json路径
infofile = 'C:/Users/%s/AppData/Local/pyemail/info.json' % _username

