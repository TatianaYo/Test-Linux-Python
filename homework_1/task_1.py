"""
Доработать тест на питоне из предыдущего задания таким образом,
чтобы вывод сохранялся построчно в список и в тесте проверялось, что в этом списке есть строки
VERSION="22.04.1 LTS (Jammy Jellyfish)" и VERSION_CODENAME=jammy.
Проверка должна выполняться только если код возврата равен 0.
"""
import subprocess


if __name__ == '__main__':
    result = subprocess.run('cat /etc/os-release', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        res_list = out.split('\n')
        print(res_list)
        if 'VERSION="22.04.1 LTS (Jammy Jellyfish)"' in res_list and 'VERSION_CODENAME=jammy' in res_list:
            print('SUCCESS')
        else:
            print('FAIL')
    else:
        print('Process finished with exit code != 0')
