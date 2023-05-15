from checkout import checkout_negative
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step_1():
    # test1
    assert checkout_negative("cd {}; 7z e badarx.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                             "Is not archive"), "Test Fail"


def test_step_2():
    # test2
    assert checkout_negative("cd {}; 7z t badarx.7z".format(data['folder_out']), "Is not archive"), "Test Fail"
