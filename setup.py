import os, ctypes, sys

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except :
        return False


if isAdmin():

    targetpath = 'C:/Program Files/pyemail/'

    # 文件夹不存在则创建文件夹
    if not os.path.exists(targetpath):
        os.mkdir(targetpath)

    pwd = os.getcwd()

    with open(targetpath + 'target.~', 'w') as f:
        f.write(pwd)

    input('set up ok')

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)




