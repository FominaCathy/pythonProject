import subprocess
import paramiko


def ssh_checkout(host, user, passw, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passw, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode('utf-8')
    client.close()
    if text in out and exit_code == 0:
        return True
    else:
        return False


def upload_files(host, user, password, local_path, remote_path, port=22):
    print(f"загружаем...")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout_negativ(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8', stderr=subprocess.PIPE)

    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def check_hash_crc32(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


def check_loadavg(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


if __name__ == "__main__":
    pass
