import string
import subprocess


def check_command(str_command: str) -> bool:
    command, path, *text = str_command.split()

    text = ' '.join(text)
    result = subprocess.run(f'{command} {path}', encoding='utf-8', shell=True, stdout=subprocess.PIPE)
    if (text in result.stdout) & (result.returncode == 0):
        return True
    else:
        return False


def check_command_extend(str_command: str, work_split=False) -> bool:
    command, path, *text = str_command.split()

    text = ' '.join(text)
    result = subprocess.run(f'{command} {path}', encoding='utf-8', shell=True, stdout=subprocess.PIPE)

    if work_split:
        list_result = result.stdout.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).split()
        if (text in list_result) & (result.returncode == 0):
            return True
        else:
            return False
    else:
        if (text in result.stdout) & (result.returncode == 0):
            return True
        else:
            return False


if __name__ == '__main__':
    example = 'cat /etc/os-release Jammy Jellyfish'
    print(f'result {example} - {check_command(example)}')
    example = 'cat /etc/os-release 24.01.10'
    print(f'result {example} - {check_command(example)}')

    example = 'cat /etc/os-release Jellyfish'
    print(f'result {example} - {check_command_extend(example, work_split=True)}')
    example = 'cat /etc/os-release Jellyfish23'
    print(f'result {example} - {check_command_extend(example, work_split=True)}')