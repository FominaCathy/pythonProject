import random
import string
import yaml
import pytest as pytest
from archive_7zip.checks import checkout, check_loadavg, ssh_checkout
from datetime import datetime

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


@pytest.fixture()
def make_folder():
    return ssh_checkout(data["ip_user"], data["user"], data["pass"],
                        f'mkdir -p {data["folder_in"]} {data["folder_out"]} {data["folder_ext"]} {data["folder_ext3"]} {data["folder_bad"]}',
                        "")


@pytest.fixture()
def clear_folder():
    return ssh_checkout(data["ip_user"], data["user"], data["pass"],
                        f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* {data["folder_ext"]}/* {data["folder_ext3"]}/* {data["folder_bad"]}/*',
                        "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        ssh_checkout(data["ip_user"], data["user"], data["pass"],
                     f'cd {data["folder_in"]}; dd if=/dev/urandom of={file_name} bs={data["bs"]} count=1 iflag=fullblock',
                     '')
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not ssh_checkout(data["ip_user"], data["user"], data["pass"],
                        f'cd {data["folder_in"]}; mkdir {subfolder_name}', ''):
        return None, None
    if not ssh_checkout(data["ip_user"], data["user"], data["pass"],
                        f'cd {data["folder_in"]}/{subfolder_name}; '
                        f'dd if=/dev/urandom of={subfile_name} bs={data["bs"]} count=1 iflag=fullblock', ''):
        return subfolder_name, None

    return subfolder_name, subfile_name


@pytest.fixture()
def create_bad_archive():
    ssh_checkout(data["ip_user"], data["user"], data["pass"],
                 f'cd {data["folder_in"]}; 7z a -t{data["ta"]} {data["folder_out"]}/arx2',
                 "Everything is Ok")
    ssh_checkout(data["ip_user"], data["user"], data["pass"],
                 f'cp {data["folder_out"]}/arx2.{data["ta"]} {data["folder_bad"]}', '')
    ssh_checkout(data["ip_user"], data["user"], data["pass"],
                 f'truncate -s 1 {data["folder_bad"]}/arx2.{data["ta"]}', '')  # сделали битым


# @pytest.fixture(autouse=True)
# def speed():
#     print(datetime.now().strftime('%H:%M:%S.%f'))
#     yield
#     print(datetime.now().strftime('%H:%M:%S.%f'))


@pytest.fixture(autouse=True)
def statistic():
    res_avg = check_loadavg(f'cat /proc/loadavg')
    text_log = (f'time: {datetime.now().strftime("%H:%M:%S.%f")}; '
                f'count: {data["count"]}; size: {data["bs"]}; loadavg: {res_avg}')

    checkout(f'echo "{text_log}" >> {data["folder_stat"]}', "")
