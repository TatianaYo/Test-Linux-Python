from checkout import checkout, get_hash


path_dir = '/home/user/tst'
path_arx = '/home/user/arx1'
path_to_dir = '/home/user'
path_to_dir2 = '/home/user/dir2'
path_to_dir3 = '/home/user/dir3'


def test_step1():
    assert checkout('cd {}; 7z a {}'.format(path_dir, path_arx), 'Everything is Ok'), 'Test FAIL'


def test_step2():
    assert checkout('cd {}; 7z u {}'.format(path_dir, path_arx), 'Everything is Ok'), 'Test FAIL'


def test_step3():
    assert checkout('cd {}; 7z d {}'.format(path_dir, path_arx), 'Everything is Ok'), 'Test FAIL'


def test_step4():
    assert checkout('cd {}; 7z e arx1.7z -o{}'.format(path_to_dir, path_to_dir2), 'Everything is Ok'), 'Test FAIL'


def test_step5():
    result = checkout('cd {}; 7z l arx1.7z'.format(path_to_dir, path_to_dir2), 'test')
    assert result, 'Test FAIL'


def test_step6():
    result_1 = checkout('cd {}; 7z x arx2.7z -o{}'.format(path_to_dir, path_to_dir3), 'Everything is Ok')
    result_2 = checkout('ls {}'.format(path_to_dir3), 'test')
    assert result_1 and result_2, 'Test FAIL'


def test_step7():
    result_1 = checkout('cd {}; 7z h test'.format(path_dir), 'Everything is Ok')
    gethash = get_hash('cd {}; crc32 test'.format(path_dir)).upper()
    result_2 = checkout('cd {}; 7z h test'.format(path_dir), gethash)
    assert result_1 and result_2, 'Test FAIL'
