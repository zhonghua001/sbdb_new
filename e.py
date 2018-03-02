# # -*- coding:utf-8 -*-
# import sys
# print sys.path
# import paramiko
#
# pkey_file = '/home/dev/.ssh/id_rsa'  # 指定用来解密的私钥的路径，这个需要手动生成，下面会讲如何生成
# key = paramiko.RSAKey.from_private_key_file(pkey_file)  # 使用私钥解密
#
# # s = paramiko.SSHClient()
# # s.load_system_host_keys()
# # s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# #
# t = paramiko.Transport(('127.0.0.1', 22))
# t.connect(username='root', pkey=key)
# sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
#
# ssh = paramiko.SSHClient()
# ssh._transport = t
# stdin, stdout, stderr = ssh.exec_command('df -h')
# print stdout.read(),stderr.read()
# t.close()


a=[u'next_binlog = /var/log/mysql/binlog/mysql-bin.000212\n', u'start_time = 1518423096\n', u'end_time = 1518423096\n', u'start_pos = 123\n', u'cur_binlog = /var/log/mysql/binlog/mysql-bin.000211\n', u'end_pos = 154\n']
d = {}
for i in  a:
    d[i.replace('\n','').split(' = ')[0]] = i.replace('\n','').split(' = ')[1]
print d['cur_binlog']