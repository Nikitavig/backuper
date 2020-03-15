from datetime import datetime
import os
import time
import shutil

# Пути откуда бэкапить файлы
LIST_PATH_FROM = [
				'C:/Project/alarm',
				]

# Пути куда бэкапить файлы
LIST_PATH_TO = [
				'C:/Backup',
				'D:/Backup',
				'E:/Backup',
				'F:/Backup',
				'//backup/sda1/backup',
				]

# Тут хранится информация о дате последнего быкапа
PATH_RESOURCES = 'resources'


def check_date():
	"""
	
	Функция для проверки даты
	Если наступил следующий день, то необходимо  сделать бэкап

	"""


	def get_date_fropm_file():
		"""

		Функция для чтения даты из файла
		"""		
		with open(PATH_RESOURCES + '/' + 'date', 'r') as file:
			return datetime.strptime(file.read(), "%Y-%m-%d").date()

	def write_date_now():
		"""

		Функция для записи даты в файл
		"""		
		with open(PATH_RESOURCES + '/' + 'date', 'w') as file:
			file.write(str(datetime.now().date()))

	# Проверка, если текущая дата > чем дата последнего бэкапа,
	if datetime.now().date() > get_date_fropm_file():
		# Записываем текущую дату в файла 
		write_date_now()
		# тогда возвращаем True
		return True
	else:
		# иначе False
		return False


def backup_from_to(path_from, path_to):
	"""
	
	Функция для бэкапа файлов из одной директории в другую
	На вход получаем два параметра
	1) Путь откуда копировать файлы
	2) Путь куда копировать файлы
	"""

	list_folder = []
	list_file = []

	for name in os.listdir(path_from):

		# Проверка на существования пути
		# Если пути не существет, то это папка
		if '.' in name:
			list_file.append(name)
		elif os.path.exists(path_from + '/' + name):
			list_folder.append(name)
		else:	
			list_file.append(name)

	# Создание каталогов
	for dir_ in list_folder:
		if not os.path.exists(path_to + '/' + dir_):
			try:
				os.listdir(path_from + '/' + dir_)
				print(f">>>>>>>>>> {path_to}")
				os.mkdir(path_to + '/' + dir_)
			except Exception as e:
				print(f"Не нужно создавать каталог. Ошибка: {e}")

	# Копирование файлов
	for file in list_file:
		if os.path.exists(path_from):
			try:
				shutil.copyfile(path_from + '/' + file, path_to + '/' + file )
			except Exception as e:
				print(f"Error: {e}")


	# Добавляем к пути вложенные папки, 
	# и рекурсивно вызываем функцию backup_from_to(,) для копирования
	for folder in list_folder:

		new_path_from = path_from + '/' + folder
		new_path_to = path_to + '/' + folder

		try:
			# Если папка существует и можно получить ее содержание, то копируем все что есть в папке
			os.listdir(new_path_from)
			print(f"new_path_from >>> {new_path_from} | os.path >>> {os.listdir(new_path_from)}")
			backup_from_to(new_path_from, new_path_to)
		except Exception as e:
			print(f"Не существует каталога: {new_path_from}. Ошибка: {e}")


def backup():
	"""
	
	Функция для копирования файлов
	"""

	# Перебираем все пути куда надо скопировать файлы
	for path_to in LIST_PATH_TO:
		# Перебираем все пути откуда надо скопировать файлы
		for path_from in LIST_PATH_FROM:
			# Сохраняем в переменную наименование коневой папки
			root_dir = path_from.split('/')[-1]
			
			# Проверяем наличие коневой папки в целевой директории,
			# если ее нет, то согдаем ее
			if not os.path.exists(path_to + '/' + root_dir):
				os.mkdir(path_to + '/' + root_dir)

			# Запускаем функцию копирования файлов из одной директории в другую
			backup_from_to(path_from, path_to + '/' + root_dir)


def main():
	"""
	
	Главная main функция
	"""

	# Проверка нужно ли делать бэкап или нет
	if check_date():
		# Если нужно сделать бэкап, то вызываем функцию backup()
		backup()


if __name__ == '__main__':
	while True:
		main()
		time.sleep(1)