from checks import checkout

folder_in = '/home/user/tst'
folder_out = '/home/user/out'
folder_ext = '/home/user/folder1'


def test_addArchive():  # a создали архив
    assert checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok"), "test1 FAIL"


def test_step2():  # e извлекли из архива в заданную папку и ответили на все вопросы "да" -o задали директорию
    assert checkout(f'cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y', "Everything is Ok"), 'test2 FAIL'


def test_totality():  # t проверка целостности архива
    assert checkout(f'cd {folder_out}; 7z t arx2.7z', "Everything is Ok"), 'test3 FAIL'


def test_delete():  # d удаление из архива
    assert checkout(f'cd {folder_out}; 7z d arx2.7z', "Everything is Ok"), 'test3 FAIL'


def test_update():  # u - обновление архива
    assert checkout(f'cd {folder_in}; 7z u {folder_out}/arx2.7z', "Everything is Ok"), 'test3 FAIL'


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
