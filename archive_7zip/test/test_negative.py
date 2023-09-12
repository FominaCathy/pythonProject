import pytest

from checks import checkout_negativ
import yaml

# folder_in = '/home/user/tst'
# folder_out = '/home/user/out'
# folder_ext = '/home/user/folder1'
# folder_bad = '/home/user/folder2'

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestNegative:
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):  # e извлекли из архива

        assert checkout_negativ(f'cd {data["folder_bad"]}; 7z e arx2.7z -o{data["folder_ext"]} -y', "ERRORS")

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert checkout_negativ(f'cd {data["folder_bad"]}; 7z t arx2.7z', "Is not")



if __name__ == '__main__':
    pytest.main(['-vv'])