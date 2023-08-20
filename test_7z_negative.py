import yaml
from sshcheckers import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)

def test_step1():
    # test1
    assert ssh_checkout(data["host"], data["user"], "11",
                        "cd {}; 7z e badarx.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                        "ERROR"), "Test4 Fail"

def test_step2():
    # test2
    assert ssh_checkout(data["host"], data["user"], "11",
                        "cd {}; 7z t badarx.7z".format(data["folder_out"]), "ERROR"), "Test5 Fail"
