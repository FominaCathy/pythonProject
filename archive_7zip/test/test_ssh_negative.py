import pytest

from archive_7zip.checks import checkout_negativ, ssh_checkout
import yaml

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestSSHNegative:
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):
        assert ssh_checkout(data["ip_user"], data["user"], data["pass"],
                            f'cd {data["folder_bad"]}; 7z e arx2.{data["ta"]} -o{data["folder_ext"]} -y',
                            "ERRORS", negative=True)

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert ssh_checkout(data["ip_user"], data["user"], data["pass"],
                            f'cd {data["folder_bad"]}; 7z t arx2.{data["ta"]}',
                            "Is not", negative=True)


if __name__ == '__main__':
    pytest.main(['-vv'])
