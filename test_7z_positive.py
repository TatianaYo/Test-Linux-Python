from checkout import checkout_positive, getout
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(make_folders, clear_folders, make_files, get_statistic):
    # test1
    res1 = checkout_positive("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                             "Everything is Ok")
    res2 = checkout_positive("ls {}".format(data["folder_out"]), "arx.{}".format(data["type"]))
    assert res1 and res2, "Test1 FAIL"


def test_step2(clear_folders, make_files, get_statistic):
    # test2
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                                 "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z e arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data["folder_ext"]), item))
    assert all(res), "Test2 FAIL"


def test_step3(get_statistic):
    # test3
    assert checkout_positive("cd {}; 7z t arx.{}}".format(data["folder_out"], data["type"]), "Everything is Ok"),\
        "Test3 FAIL"


def test_step4(get_statistic):
    # test4
    assert checkout_positive("cd {}; 7z u arx2.{}".format(data["folder_in"], data["type"]), "Everything is Ok"),\
        "Test4 FAIL"


def test_step5(clear_folders, make_files, get_statistic):
    # test5
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                                 "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("cd {}; 7z l arx.{}".format(data["folder_out"], data["folder_ext"],
                                                                 data["type"]), item))
    assert all(res), "Test5 FAIL"


def test_step6(clear_folders, make_files, make_subfolder, get_statistic):
    # test6
    res = []
    res.append(checkout_positive("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                                 "Everything is Ok"))
    res.append(checkout_positive("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                     data["folder_ext2"]), "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data["folder_ext2"]), item))
    res.append(checkout_positive("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
    res.append(checkout_positive("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
    assert all(res), "Test6 FAIL"


def test_step7(get_statistic):
    # test7
    assert checkout_positive("cd {}; 7z d arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"),\
        "Test7 FAIL"


def test_step8(clear_folders, make_files, get_statistic):
    # test8
    result = []
    for item in make_files:
        result.append(checkout_positive("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
        hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
        result.append(checkout_positive("cd {}; 7z h {}".format(data["folder_in"], item), hash))
    assert all(result), "Test8 FAIL"