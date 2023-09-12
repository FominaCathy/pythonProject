import random
import string

import pytest as pytest

from checks import checkout, check_hash_crc32
import pytest

folder_in = '/home/user/tst'
folder_out = '/home/user/out'
folder_ext = '/home/user/folder1'
folder_ext3 = '/home/user/folder3'


@pytest.fixture()
def make_folder():
    return checkout(f'mkdir {folder_in} {folder_out} {folder_ext} {folder_ext3}', "")


@pytest.fixture()
def clear_folder():
    return checkout(f'rm -rf {folder_in}/* {folder_out}/* {folder_ext}/* {folder_ext3}/*', "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(5):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        checkout(f'cd {folder_in}; dd if=/dev/urandom of={file_name} bs=512 count=1 iflag=fullblock', '')
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not checkout(f'cd {folder_in}; mkdir {subfolder_name}', ''):
        return None, None
    if not checkout(f'cd {folder_in}/{subfolder_name}; '
                    f'dd if=/dev/urandom of={subfile_name} bs=512 count=1 iflag=fullblock', ''):
        return subfolder_name, None

    return subfolder_name, subfile_name


def test_add_archive(make_folder, clear_folder, make_files):  # a создали архив
    res_add = checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok")
    res_ls = checkout(f'ls {folder_out}', "arx2.7z")
    assert res_add and res_ls


def test_check_e_extract(clear_folder, make_files):  #
    res = list()
    res.append(checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok"))
    res.append(checkout(f'cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y', "Everything is Ok"))
    for item in make_files:
        res.append(checkout(f'ls {folder_ext}', item))

    assert all(res)


def test_check_e_extract_subfolder(clear_folder, make_files, make_subfolder):
    res = list()
    res.append(checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok"))
    res.append(checkout(f'cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y', "Everything is Ok"))
    for item in make_files:
        res.append(checkout(f'ls {folder_ext}', item))
    for item in make_subfolder:
        res.append(checkout(f'ls {folder_ext}', item))

    assert all(res)


def test_check_x_extract_subfolder(clear_folder, make_files, make_subfolder):
    # files, subflder and files in subfolder
    res = list()
    res.append(checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok"))
    res.append(checkout(f'cd {folder_out}; 7z x arx2.7z -o{folder_ext} -y', "Everything is Ok"))
    for item in make_files:
        res.append(checkout(f'ls {folder_ext}', item))

    res.append(checkout(f'ls {folder_ext}', make_subfolder[0]))
    res.append(checkout(f'ls {folder_ext}/{make_subfolder[0]}', make_subfolder[1]))

    assert all(res)


def test_check_x_files(clear_folder, make_files):  # only files
    res = list()
    res.append(checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok"))
    res.append(checkout(f'cd {folder_out}; 7z x arx2.7z -o{folder_ext} -y', "Everything is Ok"))
    for item in make_files:
        res.append(checkout(f'ls {folder_ext}', item))
    assert all(res)


def test_totality():  # t проверка целостности архива
    assert checkout(f'cd {folder_out}; 7z t arx2.7z', "Everything is Ok"), 'test_totality FAIL'


def test_delete():  # d удаление из архива
    assert checkout(f'cd {folder_out}; 7z d arx2.7z', "Everything is Ok"), 'NO delete'


def test_update():  # u - обновление архива
    assert checkout(f'cd {folder_in}; 7z u {folder_out}/arx2.7z', "Everything is Ok"), 'NO update'


def test_check_archive():  #
    result_add = checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok")
    result_check = checkout(f'ls {folder_out}', 'arx2.7z')
    assert result_check and result_add, 'test_check_archive FAIL'


def test_check_extract():  # e извлекли из архива в заданную папку и ответили на все вопросы "да" -o задали директорию
    result_ex = checkout(f'cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y', "Everything is Ok"), 'test2 FAIL'
    result_check1 = checkout(f'ls {folder_ext}', 'tst1')
    result_check2 = checkout(f'ls {folder_ext}', 'tst2')
    assert result_ex and result_check1 and result_check2, 'test_check_archive FAIL'


def test_nonempty_archive():
    assert checkout(f'cd {folder_out}; 7z l arx2.7z', '2 files'), 'test_check_archive FAIL'


def test_check_list_archive():
    res_tst1 = checkout(f'cd {folder_out}; 7z l arx2.7z', 'tst1')
    res_tst2 = checkout(f'cd {folder_out}; 7z l arx2.7z', 'tst2')
    assert res_tst1 and res_tst2, 'test_check_list_archive FAIL'


def test_check_hash():
    hash_crc32 = check_hash_crc32(f'cd {folder_out}; crc32 arx2.7z')
    res_upper = checkout(f'cd {folder_out}; 7z h arx2.7z', hash_crc32.upper())
    res_lower = checkout(f'cd {folder_out}; 7z h arx2.7z', hash_crc32.lower())
    assert res_lower or res_upper, 'NO equal hash'
