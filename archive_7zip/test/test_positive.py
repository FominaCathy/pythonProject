import random
import string
import yaml


from checks import checkout, check_hash_crc32
import pytest

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


# folder_in = '/home/user/tst'
# folder_out = '/home/user/out'
# folder_ext = '/home/user/folder1'
# folder_ext3 = '/home/user/folder3'

class TestPositive:

    def test_add_archive(self, make_folder, clear_folder, make_files):  # a создали архив
        res_add = checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok")
        res_ls = checkout(f'ls {data["folder_out"]}', "arx2.7z")
        assert res_add and res_ls

    def test_check_e_extract(self, clear_folder, make_files):  #
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z e arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folder_ext"]}', item))

        assert all(res)

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z e arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folder_ext"]}', item))
        for item in make_subfolder:
            res.append(checkout(f'ls {data["folder_ext"]}', item))

        assert all(res)

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        # files, subflder and files in subfolder
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z x arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folder_ext"]}', item))

        res.append(checkout(f'ls {data["folder_ext"]}', make_subfolder[0]))
        res.append(checkout(f'ls {data["folder_ext"]}/{make_subfolder[0]}', make_subfolder[1]))

        assert all(res)

    def test_check_x_files(self, clear_folder, make_files):  # only files
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z x arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folder_ext"]}', item))
        assert all(res)

    def test_totality(self, clear_folder, make_files):  # t проверка целостности архива
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z t arx2.7z', "Everything is Ok"))

        assert all(res)

    def test_delete(self, clear_folder, make_files, make_subfolder):  # d удаление из архива
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z d arx2.7z', "Everything is Ok"))

        assert all(res)

    def test_update(self):  # u - обновление архива
        assert checkout(f'cd {data["folder_in"]}; 7z u {data["folder_out"]}/arx2.7z', "Everything is Ok"), 'NO update'

    # def test_check_archive(clear_folder, make_files):  #
    #
    #     result_add = checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok")
    #     result_check = checkout(f'ls {folder_out}', 'arx2.7z')
    #     assert result_check and result_add, 'test_check_archive FAIL'

    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folder_out"]}; 7z l arx2.7z', f'{len(make_files)} files'))

    # def test_check_list_archive(clear_folder, make_files):
    #     res = list()
    #     res.append(checkout(f'cd {folder_in}; 7z a {folder_out}/arx2', "Everything is Ok"))
    #
    #     res.append(checkout(f'cd {folder_out}; 7z l arx2.7z', 'tst1')
    #     res_tst2 = checkout(f'cd {folder_out}; 7z l arx2.7z', 'tst2')
    #     assert res_tst1 and res_tst2, 'test_check_list_archive FAIL'

    def test_check_hash(self):
        hash_crc32 = check_hash_crc32(f'cd {data["folder_out"]}; crc32 arx2.7z')
        res_upper = checkout(f'cd {data["folder_out"]}; 7z h arx2.7z', hash_crc32.upper())
        res_lower = checkout(f'cd {data["folder_out"]}; 7z h arx2.7z', hash_crc32.lower())
        assert res_lower or res_upper, 'NO equal hash'


if __name__ == '__main__':
    pytest.main(['-vv'])
