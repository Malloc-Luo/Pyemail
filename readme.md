`pyemail`是一款在终端中使用的邮箱客户端，通过一个简单的命令就可以发送邮件到指定地址，非常简洁高效

## 更新说明：

`version = 0.2.0`

**0.2.0**：目前仅可以发送纯文本邮件，暂不支持发送html，附件等；暂不支持接收邮件

## pyemail 使用说明：

### 1. 配置

1.  `pyemail`运行依赖于`python`环境，在使用之前请配置好你的`python`环境。
2.   将文件中`pyemail.exe`的路径添加到`Windows`[环境变量](https://jingyan.baidu.com/article/47a29f24610740c0142399ea.html)中。设置完成环境变量后可以在终端输入`pyemail -v`或者`pyemail version`进行验证。
3.  `pyemail.exe`同级目录下有两个配置文件，`settings.josn`和`info.json`，分别是用户信息配置和客户端配置；如果没有这两个文件，在`pyemail`第一次启动之后会生成这两个文件，之后分别使用`pyemail setting`和`pyemail info`两个命令打开这两个文件并进行编辑。

### 2. 邮件

当前版本`pyemail`客户端邮件目前仅支持特定格式的文本文件，扩展名为`.email`，当然，使用`.txt`也是支持的，但必须使用`.email`格式。

#### 邮件格式说明：

邮件文本中以`#`开头的一行为格式指令，用来指明一些邮件信息，比如用于设置邮件标题等，大小写不限，目前支持的格式指令：

| 指令      | 格式                         | 是否必须 |
| --------- | ---------------------------- | -------- |
| `#email`  | 目标邮箱，多个邮箱用 `,`隔开 | 是       |
| `#name`   | 发送者姓名                   | 否       |
| `#title`  | 邮件标题                     | 否       |
| `#toname` | 目标邮箱用户姓名             | 否       |
|           |                              |          |

需要说明的是，在一些情况下，`#email`也不是必须的。

以下是一封示例邮件：

```
#email yuqi@email.com
#title 这是一封来自pyemail的邮件
#name pyemail
#toname everyone
您好！
这是一封测试邮件，来自pyemail客户端。
```

### 3.配置文件

配置文件分为`info.json`和`settings.json`，重点是`info.json`文件一些必须的配置项

```javascript
{
    "user-email": "your email", 
    "password": "smtp server password",
    "smtp-server": "smtp server",
    "port": 25,
    "default-name": "",
    "default-editer": "",
    "ssl": false,
}
```

`user-email`为用户的邮箱地址，也就是你发邮件的地址；`smtp-server`为你所用邮箱的`smtp`服务器的地址，具体可以查询你所用邮箱的官网；`port`为`smtp`服务器端口，默认为`25`，当然具体还是要看`smtp`服务器的具体规定；`password`为`smtp`服务器的认证码(密码)，未必是官方邮箱客户端的登录密码，例如[QQ邮箱](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=331)是一个特定的验证码；`default-name`是发信时使用的默认署名；`default-editer`是打开`settings.json`，`info.json`时使用的默认编辑器，填写编辑器启动程序的路径或者命令即可，例如使用`vim`编辑器可以填写`vim`，使用`sublime text`可以填写`subl`

### 4. 使用

`pyemail`客户端只需要你在命令行中打出几个简单的命令就能将邮件发送到指定地址，启动迅速，使用方便。其命令格式为:

```
pyemail <command>
pyemail <command> <param> <opt command> <opt param>
```

需注意的是，命令不区分大小写。全部命令如下：

| `command` | `simple command` | `note`                                            |
| --------- | ---------------- | ------------------------------------------------- |
| `send`    | `-s`             | 发送邮件，`param`为邮件文件`.email`或`.txt`       |
| `version` | `-v`             | 查询`pyemail`版本                                 |
| `setting` | `-st`            | 用默认编辑器打开`settings.json`                   |
| `info`    | `-i`             | 用默认编辑器打开`info.json`                       |
| `to`      | `-t`             | 指定发送邮箱地址，作为`send`命令的`<opt command>` |
| `add`     | `-a`             | 添加发送邮箱地址，作为`send`命令的`<opt command>` |

举例说明：

```
-发送邮件hello.email到邮件内指定地址
pyemail send hello.email
pyemail -s hello.email

-发送邮件hello.email到命令指定地址，覆盖邮件内指定地址
pyemail send hello.email to yuqi@email.com
pyemail -s hello.email -t yuqi@email.com

-发送邮件hello.email到邮件内指定地址，并附加一个地址
pyemail send hello.email add yuqi@email.com
pyemail -s hello.email -a yuqi@email.com
```

## 计划更新：

*   支持发送文件附件
*   支持添加联系人
*   支持发送html
*   支持`pop3`接收邮件
*   适配`Linux`和`Mac os`

