from checkout import ssh_checkout_poz, getout, checkout_positive
from load_file import upload_files, download_files
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step0():
    res = []
    upload_files(data["ip"], data["user"], data["passwd"], data["pkgname"] + ".deb",
                 "/home/{}/{}.deb".format(data["user"], data["pkgname"]))
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -i"
                                "/home/{}/{}.deb".format(data["passwd"], data["user"], data["pkgname"]),
                                "Настраивается пакет"))
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "echo '{}' | "
                                "sudo -S dpkg -s {}".format(data["passwd"], data["pkgname"]),
                                "Status: install ok installed"))
    assert all(res), "Test0 FAIL"


def test_step1(make_folders, clear_folders, make_files, get_statistic):
    # test1
    res1 = ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".format(data["folder_in"],
                            data["folder_out"]), "Everything is Ok")
    res2 = ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_out"]), "arx2.7z")
    assert res1 and res2, "Test1 FAIL"


def test_step2(clear_folders, make_files, get_statistic):
    # test2
    res = []
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".format(data["folder_in"],
                                data["folder_out"]), "Everything is Ok"))
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z e arx2.7z -o{} -y".format(data["folder_out"],
                                data["folder_ext"]), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext"]), item))
    assert all(res), "Test2 FAIL"


def test_step3(get_statistic):
    # test3
    assert ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z t arx2.7z".format(data["folder_out"]),
                            "Everything is Ok"), "Test3 FAIL"


def test_step4(get_statistic):
    # test4
    assert ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z u arx2.7z".format(data["folder_in"]),
                            "Everything is Ok"), "Test4 FAIL"


def test_step5(clear_folders, make_files, get_statistic):
    # test5
    res = []
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2".format(data["folder_in"],
                                data["folder_out"]), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z l arx2.7z".format(data["folder_out"],
                                    data["folder_ext"]), item))
    assert all(res), "Test5 FAIL"


def test_step6(clear_folders, make_files, make_subfolder, get_statistic):
    # test6
    res = []
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx".format(data["folder_in"],
                                data["folder_out"]), "Everything is Ok"))
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z x arx.7z -o{} -y".format(data["folder_out"],
                                data["folder_ext2"]), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]), item))
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]),
                                make_subfolder[0]))
    res.append(ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "ls {}/{}".format(data["folder_ext2"],
                                make_subfolder[0]), make_subfolder[1]))
    assert all(res), "Test6 FAIL"


def test_step7(get_statistic):
    # test7
    assert ssh_checkout_poz(data["ip"], data["user"], data["passwd"], "cd {}; 7z d arx.7z".format(data["folder_out"]),
                            "Everything is Ok"), "Test7 FAIL"


def test_step8(clear_folders, make_files, get_statistic):
    # test8
    result = []
    for item in make_files:
        result.append(checkout_positive("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
        hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
        result.append(checkout_positive("cd {}; 7z h {}".format(data["folder_in"], item), hash))
    assert all(result), "Test8 FAIL"
