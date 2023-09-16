import pytest

from archive_7zip.checks import checkout_negativ
import yaml

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestNegative:
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):

        assert checkout_negativ(f'cd {data["folder_bad"]}; 7z e arx2.{data["ta"]} -o{data["folder_ext"]} -y',
                                "ERRORS")

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert checkout_negativ(f'cd {data["folder_bad"]}; 7z t arx2.{data["ta"]}',
                                "Is not")


if __name__ == '__main__':
    pytest.main(['-vv'])
