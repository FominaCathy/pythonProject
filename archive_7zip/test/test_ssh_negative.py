import pytest

from archive_7zip.checks import checkout_negativ, ssh_checkout
import yaml




class TestSSHNegative:
    with open('config.yaml') as fy:
        data = yaml.safe_load(fy)
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):
        assert ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                            f'cd {self.data["folder_bad"]}; 7z e arx2.{self.data["ta"]} -o{self.data["folder_ext"]} -y',
                            "ERRORS", negative=True)

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert ssh_checkout(self.data["ip_user"], self.data["user"], self.data["pass"],
                            f'cd {self.data["folder_bad"]}; 7z t arx2.{self.data["ta"]}',
                            "Is not", negative=True)


if __name__ == '__main__':
    pytest.main(['-vv'])
