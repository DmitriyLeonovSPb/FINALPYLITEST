import random
import string
import subprocess
import pytest
from datetime import datetime
import yaml
from sshcheckers import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)

# Создаёт директории
@pytest.fixture()
def make_folders():
    return ssh_checkout(data["host"], data["user"], "11",
                        "mkdir {} {} {} {}".format(data["folder_in"],
                                                   data["folder_out"], data["folder_ext"], data["folder_badarx"]), "")


# Очищает директории
@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"],
                        "11", "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"],
                                                                  data["folder_ext"], data["folder_badarx"]), "")

# Генерирует файлы
@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count_file"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(
                data["host"], data["user"], "11",
                "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                       filename, data["size_file"]),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], "11",
                        "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout(
            data["host"], data["user"], "11",
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

@pytest.fixture()
def make_badarx():
    ssh_checkout(data["host"], data["user"], "11",
                 "cd {}; 7z a {}/badarx.7z".format(data["folder_in"], data["folder_badarx"]), "Everything is Ok")
    ssh_checkout(data["host"], data["user"], "11",
                 "truncate -s1{}/badarx.7z".format(data["folder_badarx"]), "Everything is Ok")
    #yield "badarx"
    #checkout_positive("rm -f {}/badarx.7z".format(folder_badarx), "")

@pytest.fixture()
def make_stat():
    f = open("stat.txt", "a")
    current_datetime = datetime.now()
    f.write(str(current_datetime)+"\n")
    file_counter = data["count_file"]
    f.write("Quantity of files: "+str(file_counter)+"\n")
    file_size = data["size_file"]
    f.write("Size of files: "+str(file_size) + "\n")
    o = open("/proc/loadavg")
    statt = o.read()
    f.write(str(statt) + "\n")
    o.close()
    f.close()
    return

@pytest.fixture()
def make_stat2():
    ssh_checkout(data["host"], data["user"], "11",
                 "date >> {}/stat_alt.txt".format(data["stat_alt"]), "Everything is Ok")
    file_counter = data["count_file"]
    file_size = data["size_file"]
    y = open("/home/user/stat_alt/stat_alt.txt", "a")
    y.write("Quantity of files: " + str(file_counter) + "\n")
    y.write("Size of files: " + str(file_size) + "\n")
    y.close()
    ssh_checkout(data["host"], data["user"], "11",
                 "cat /proc/loadavg >> {}/stat_alt.txt".format(data["stat_alt"]), "Everything is Ok")
    return