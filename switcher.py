from pynput import keyboard
from SecondaryFuncs import SecondaryFuncs


input_word = ""

"""
Словари хэширую и помещаю в массий, после сортирую.
dict_in содержит в себе сочетания символов,
при которых необходимо моменять раскладку, вне зависимости он дальнейших символов.
"""
dict_in = []
file_in = open("data/dict_in.txt", "r")
for line in file_in:
    line = line.rstrip()
    l = len(line) + 1
    x = hash(line)
    dict_in.append(x)
file_in.close()
dict_in.sort()

"""
Если, после сочетания символов содержащихся в dict_match, идет пробел, необходимо поменять раскладку.
"""
dict_match = []
file_match = open("data/dict_match.txt", "r")
for line in file_match:
    line = line.rstrip()
    l = len(line) + 1
    x = hash(line)
    dict_match.append(x)
file_match.close()
dict_match.sort()


def on_release(key, check_flag=True):
    """
    Основная функция.
    Если мы нажимаем на space или Enter, world сбрасывается, значит началось новое слово.
    Меняет символы в словах которые совпали со словами в dict_match
    При нажатии на Esc программа заканчивает работу.
    :param key: значение нажатой клавиша
    :param check_flag: был ли нажат space или enter
    """
    global input_word
    try:
        if key.char:
            input_word += key.char
            SecondaryFuncs.switcher(input_word, dict_in)
    except AttributeError:
        pass

    if (key == keyboard.Key.space or key == keyboard.Key.enter) and \
            len(input_word) > 0:
        input_word.strip()
        if key == keyboard.Key.space and \
                SecondaryFuncs.binary_search(dict_match, hash(input_word)) and \
                check_flag:
            SecondaryFuncs.switchToABC(input_word, check_flag) \
                if SecondaryFuncs.match(input_word) \
                else SecondaryFuncs.switchToRussian(input_word, check_flag)
        elif key == keyboard.Key.enter and \
                SecondaryFuncs.binary_search(dict_match, hash(input_word)) and \
                check_flag:
            check_flag = False
            SecondaryFuncs.switchToABC(input_word, check_flag) \
                if SecondaryFuncs.match(input_word) \
                else SecondaryFuncs.switchToRussian(input_word, check_flag)
        input_word = ''
    if key == keyboard.Key.backspace:
        input_word = input_word[:-1]
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_release=on_release) as listener:
    listener.join()

if __name__ == '__main__':
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
