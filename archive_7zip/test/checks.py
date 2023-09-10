import subprocess


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
