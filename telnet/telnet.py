#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# telnet至Windows机并删除api的jar包文件夹

import telnetlib

''' telnet至Windows机并删除api的jar包文件夹 '''

# 配置选项
Host = '192.168.1.200'     # IP地址
username = 'Administrator' # 登录用户名
password = '1'             # 登录密码
finish = '>'               # 提示符
jarpath = 'E:\sonatype-work\nexus\storage\releases\com\test\api\2.0.2-RELEASE'

# 连接
tn = telnetlib.Telnet(Host)

# 输入登录用户名
#tn.read_until('Welcome to Microsoft Telnet Service\r\n')
tn.read_until('login:')       # Win7 登录
tn.write(username + '\r\n')

# 输入登录密码
tn.read_until('password:')
tn.write(password + '\r\n')

# 登录完毕后，转至文件夹并显示相关文件夹
tn.read_until('Administrator>')
tn.write('E:\del_jarpath.bat\r\n')
tn.read_until('>')
tn.close()