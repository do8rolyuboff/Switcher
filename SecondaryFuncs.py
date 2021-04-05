from pynput import keyboard
from pyinputlanguage import macSwitchInputLanguage


layout_ru = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
							  'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
					 "йцукенгшщзхъфывапролджэячсмитьбю.ё"
					 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

layout_en = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
							  'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
					 "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
					 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))


class SecondaryFuncs:
	@staticmethod
	def binary_search(list, item, low=0, high=None):
		"""
		Бинарный поиск по словорю.
		:param list: словарь
		:param item: хешированное, искомое, сочетание символов
		:param low:
		:param high:
					low и high отвечают за границы той части list,
					 в которой выполняется поиск.
		:return: Место искомого в list.
				 Если искомое не найдено вернет False.
		"""
		if high is None:
			high = len(list) - 1
		while low < high:
			mid = (low + high) // 2
			midval = list[mid]
			if midval < item:
				low = mid + 1
			elif midval > item:
				high = mid
			else:
				return mid
		return False

	@staticmethod
	def match(text, alphabet=None):
		"""
		Определение на какую раскладку нужно менять.
		"""
		if alphabet is None:
			alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
		return not alphabet.isdisjoint(text.lower())

	@staticmethod
	def switchToRussian(text, check_flag):
		"""
		Смена на Русскую раскладку.
		"""
		macSwitchInputLanguage("com.apple.keylayout.Russian")
		SecondaryFuncs.transliteration(text, layout_ru, check_flag)

	@staticmethod
	def switchToABC(text, check_flag):
		"""
		Смена на ABC раскладку.
		"""
		macSwitchInputLanguage("com.apple.keylayout.ABC")
		SecondaryFuncs.transliteration(text, layout_en, check_flag)

	@staticmethod
	def transliteration(text, layout, check_flag):
		"""
		Транслитерация напечатанных символов

		:param layout: ru-en / en-ru
		:param check_flag: был ли нажат space или enter
		"""
		keyboard_controller = keyboard.Controller()
		for i in range(len(text) + int(check_flag)):
			keyboard_controller.press(keyboard.Key.backspace)
		for i in text:
			keyboard_controller.press(i.translate(layout))
		if check_flag:
			keyboard_controller.press(keyboard.Key.space)

	@staticmethod
	def switcher(text, dict_in):
		"""
		Функция проверяет совпадения по словарю dict_in.
		"""
		if SecondaryFuncs.binary_search(dict_in, hash(text)):
			space_check = False
			SecondaryFuncs.switchToABC(text, space_check) \
				if SecondaryFuncs.match(text) \
				else SecondaryFuncs.switchToRussian(text, space_check)
