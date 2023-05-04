"""
Написать функцию на Python, которой передаются в качестве параметров команда и текст. Функция должна возвращать True,
если команда успешно выполнена и текст найден в её выводе и False в противном случае.
Передаваться должна только одна строка, разбиение вывода использовать не нужно.
"""
import subprocess


def command(com: str, text: str) -> bool:
    result = subprocess.run(com, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False


if __name__ == '__main__':
    command1 = 'cat /etc/os-release'
    string1 = 'jammy'
    command(command1, string1)
