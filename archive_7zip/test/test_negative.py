from checks import checkout_negativ

folder_in = '/home/user/tst'
folder_out = '/home/user/out'
folder_ext = '/home/user/folder1'
folder_bad = '/home/user/folder2'


def test_negative1():  # e извлекли из архива
    assert checkout_negativ(f'cd {folder_bad}; 7z e arx2.7z -o{folder_ext} -y', "ERRORS"), "test1 FAIL"


def test_negative2():  # t проверка целостности архива
    assert checkout_negativ(f'cd {folder_bad}; 7z t arx2.7z', "ERRORS"), 'test2 FAIL'
