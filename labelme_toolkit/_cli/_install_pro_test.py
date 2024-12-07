import subprocess


def test_install_pro_list_versions():
    subprocess.check_call(["labelmetk", "install-pro", "--list-versions"])
