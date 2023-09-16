import string

import yaml
from random import random, choices
from archive_7zip.checks import checkout, check_hash_crc32
import pytest


class TestPositive:
    with open('config_user.yaml') as fy:
        data = yaml.safe_load(fy)

    def test_add_archive(self, make_folder, clear_folder, make_files):
        """
        проверка создания архива "arx2.7z" в папке "folder_out"
        """
        res = list()

        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        res.append(checkout(f'ls {self.data["folder_out"]}', f'arx2.{self.data["ta"]}'))
        assert all(res)

    def test_check_e_extract(self, clear_folder, make_files):  #
        """
        проверка распаковки содержимого архива "arx2.7z" в папку "folder_ext"
        """
        res = list()
        res.append(
            checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                     "Everything is Ok"))
        res.append(
            checkout(f'cd {self.data["folder_out"]}; 7z e arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                     "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {self.data["folder_ext"]}', item))

        assert all(res)

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        """
        проверка распаковки содержимого архива "arx2.7z" (файлов и папок) в папку "folder_ext" без сохранения путей
        """
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        res.append(checkout(f'cd {self.data["folder_out"]}; 7z e arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                            "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {self.data["folder_ext"]}', item))
        for item in make_subfolder:
            res.append(checkout(f'ls {self.data["folder_ext"]}', item))

        assert all(res)

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        """
        проверка распаковки содержимого архива "arx2.7z" (файлов и папок) в папку "folder_ext" с сохранением путей
        """
        # files, subflder and files in subfolder
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        res.append(checkout(f'cd {self.data["folder_out"]}; 7z x arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                            "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {self.data["folder_ext"]}', item))

        res.append(checkout(f'ls {self.data["folder_ext"]}', make_subfolder[0]))
        res.append(checkout(f'ls {self.data["folder_ext"]}/{make_subfolder[0]}', make_subfolder[1]))

        assert all(res)

    def test_check_x_files(self, clear_folder, make_files):  # only files
        """
        проверка распаковки содержимого архива "arx2.7z" (файлов) в папку "folder_ext" в режиме сохранения путей
        """
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        res.append(checkout(f'cd {self.data["folder_out"]}; 7z x arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                            "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {self.data["folder_ext"]}', item))
        assert all(res)

    def test_totality(self, clear_folder, make_files):
        """
        проверка целостности архива
        """
        res = list()
        res.append(
            checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                     "Everything is Ok"))
        res.append(checkout(f'cd {self.data["folder_out"]}; 7z t arx2.{self.data["ta"]}', "Everything is Ok"))

        assert all(res)

    def test_delete(self, clear_folder, make_files, make_subfolder):
        """
        удаление из архива
        """
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        res.append(checkout(f'cd {self.data["folder_out"]}; 7z d arx2.{self.data["ta"]}',
                            "Everything is Ok"))

        assert all(res)

    def test_update(self, make_folder, clear_folder, make_files):
        """
        проверка обновления архива
        """
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        # добавление файла в исходную папку
        file_name = ''.join(choices(string.ascii_lowercase + string.digits, k=5))
        res.append(checkout(
            f'cd {self.data["folder_in"]}; dd if=/dev/urandom of={file_name} bs={self.data["bs"]} count=1 iflag=fullblock',
            ''))
        # обновление архива
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z u {self.data["folder_out"]}/arx2.{self.data["ta"]}',
                            "Everything is Ok"))
        # проверка добавления файла в архив
        res.append(checkout(f'7z l {self.data["folder_out"]}/arx2.{self.data["ta"]}', file_name))
        return all(res)

    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        res.append(checkout(f'cd {self.data["folder_out"]}; 7z l arx2.{self.data["ta"]}',
                            f'{len(make_files)} file'))

    def test_check_hash(self, make_folder, clear_folder, make_files):
        """
        проврека расчета хеша
        """
        res = list()
        res.append(checkout(f'cd {self.data["folder_in"]}; 7z a -t{self.data["ta"]} {self.data["folder_out"]}/arx2',
                            "Everything is Ok"))
        hash_crc32 = check_hash_crc32(f'cd {self.data["folder_out"]}; crc32 arx2.{self.data["ta"]}')
        res_upper = checkout(f'cd {self.data["folder_out"]}; 7z h arx2.{self.data["ta"]}', hash_crc32.upper())
        res_lower = checkout(f'cd {self.data["folder_out"]}; 7z h arx2.{self.data["ta"]}', hash_crc32.lower())
        res.append(res_lower or res_upper)
        assert all(res)


if __name__ == '__main__':
    pytest.main(['-vv'])
