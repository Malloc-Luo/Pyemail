# -*- coding: utf-8
# !/usr/bin/python

#from colorama import init, Fore, Back, Style


def printWarning(s, q=' '):
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    assert s
    print(Fore.YELLOW + Style.DIM + '-[%s] %s' % (s, q))


def printError(s, q=' '):
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    assert s
    print(Fore.RED + '-[%s] %s' % (s, q))


def printSuccess(s, q=' '):
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    assert s
    print(Fore.GREEN + Style.DIM + '+[%s] %s' % (s, q))


def check_server_connect(server, port):
    """
    测试网络连接与服务器连接
    :param server: str, server host
    :param port: int, server port
    :return: True, normal connect; False, error connect
    """
    networkerror = True
    s = __import__('socket').socket()
    s.settimeout(3)

    try:
        if s.connect_ex((server, port)) == 0:
            networkerror = True
        else:
            networkerror = False

    except:
        networkerror = False

    finally:
        s.close()
        return networkerror


def check_json_Setting(fname, key):
    """
    查询json中某个设定项
    """
    try:
        import json
        with open(fname, 'r') as f:
            d = json.load(f)
            return d[key]

    except :
        return 'jsonLoadOrReadError'


def quit_or_continue():

    if str(input('quit ?[y/n]')).lower() in {'y', 'yes'}:
        exit(0)
        