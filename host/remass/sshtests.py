import paramiko

RM_FILE_DIR = '/home/root/.local/share/remarkable/xochitl'


#paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG) 

host_ = 'nyt'
port_ = 22
username_ = 'root'
password_ = 'NotizenKritzler'
timeout_ = 5
compress_ = True

client = paramiko.SSHClient()
#client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#connect may rise: BadHostKeyException,AuthenticationException,SSHException,socket error
# public-private key auth doesn't work for me
#client.connect(host_, port=port_, key_filename='/home/snototter/.ssh/id_github', timeout=timeout_, compress=True)
client.connect(host_, port=port_, username=username_, password=password_, look_for_keys=False, allow_agent=False, timeout=timeout_, compress=compress_)

print('CONNECTED!!!!')
stdin,stdout,stderr=client.exec_command('ls -la')
print(stdout.readlines())
#stdin, stdout, stderr = client.exec_command('ls -l')
sftp = client.open_sftp()
print('listdir', sftp.listdir())
for i in sftp.listdir():
  lstatout = str(sftp.lstat(i)).split()
  print('lstatout', lstatout)
#print('out', stdout)
#print('err', stderr)

print('CWD:', sftp.getcwd())
stdin,stdout,stderr=client.exec_command(f'ls -la "{RM_FILE_DIR}"')
print('ls rm_file_dir:',  '\n'.join(stdout.readlines()))
sftp.close()


##Downloading a file from remote machine
#ftp_client=ssh_client.open_sftp()
#ftp_client.get(‘remotefileth’,’localfilepath’)
#ftp_client.close()
##Uploading file from local to remote machine
#ftp_client=ssh.open_sftp()
#ftp_client.put(‘localfilepath’,remotefilepath’)
#ftp_client.close()


# TODO docs
# http://docs.paramiko.org/en/stable/api/client.html
# http://docs.paramiko.org/en/stable/api/sftp.html#paramiko.sftp_client.SFTPClient



client.close()
