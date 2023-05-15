import random
import string
import pytest
from checkout import checkout_positive, getout
import yaml
from datetime import datetime

with open('config.yaml') as f:
   data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout_positive("mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'],
                                                        data['folder_ext'], data['folder_badarx']), "")


@pytest.fixture()
def clear_folders():
    return checkout_positive("rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'],
                                                        data['folder_ext'], data['folder_badarx']), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'], filename),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(['folder_in'], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def get_statistic():
    yield
    stat = getout("cat /proc/loadavg")
    checkout_positive("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                                     data["count"], data["bs"], stat), "")
