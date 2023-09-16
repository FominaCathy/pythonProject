from checks import ssh_checkout, upload_files
import yaml


def deploy():
    with open('test/config_ssh.yaml') as fy:
        data = yaml.safe_load(fy)

    res = list()
    upload_files(data["ip_user"], data["user"], data["pass"],
                 data["local_path"], data["remote_path"])
    res.append(ssh_checkout(data["ip_user"], data["user"], data["pass"],
                            f"echo '{data['pass']}' | sudo -S dpkg -i {data['remote_path']}",
                            "Настраивается пакет")) #"

    res.append(ssh_checkout(data["ip_user"], data["user"], data["pass"],
                            f"echo '{data['pass']}' | sudo -S dpkg -s {data['package']}",
                            "Status: install ok installed"))

    return all(res)


if __name__ == "__main__":

    if deploy():
        print("OK")
    else:
        print("error")
