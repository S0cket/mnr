import os
import sys
import re

class Ip:
	def __init__(self, val = 1):
		self.ip = val

class Parser: # Класс для обработки команд
	def __init__(self):
		self.config = { # Список команд
			"z": self.z,
			"s": self.s,
			"t": self.t,
			"j": self.j,
			"d": self.debug
		}
	# По списку команд передаёт управление нужной функции
	def command(self, string, values, ip):
		f = re.findall(r"[z|Z|s|S|t|T|j|J|d|D]", string)[0].lower() # Буква команды
		args = re.findall(r"\d+", string) # Операнды команды
		try:
			self.config[f](*args, values, ip)
		except:
			print("{0}: неверные операнды".format(string))
			exit(1)
	# Команда обнуления
	def z(self, n, values, ip):
		rn = values.get(n)
		if (rn == None):
			values.update([(n, 0)])
		else:
			values[n] = 0
	# Команда инкремента
	def s(self, n, values, ip):
		rn = values.get(n)
		if (rn == None):
			print("Неинициализированный регистр R{0}".format(n))
			exit(1)
		else:
			values[n] += 1
	# Команда переадресации (замены)
	def t(self, m, n, values, ip):
		rm = values.get(m)
		rn = values.get(n)
		if (rm == None or rn == None):
			if (rm == None):
				print("Неинициализированный регистр R{0}".format(m))
				exit(1)
			if (rn == None):
				values.update([(n, rm)])
		else:
			values[n] = values[m]
	# Команда условного перехода
	def j(self, m, n, q, values, ip):
		rm = values.get(m)
		rn = values.get(n)
		if (rm == None or rn == None):
			if (rm == None):
				print("Неинициализированный регистр R{0}".format(m))
				exit(1)
			if (rn == None):
				print("Неинициализированный регистр R{0}".format(n))
				exit(1)
		else:
			if (rm == rn):
				ip.ip = int(q) - 1
	# Команда вывода регистров на экран
	def debug(self, values, ip):
		out = values.copy()
		out = sorted(out.items(), key = lambda item: int(item[0]))
		print()
		print("ip = {0}".format(ip.ip))
		for elem in out:
			print("R{0} = {1}".format(*elem))

# Функция чтения из файла. Возвращает список команд и словарь значений
def reader(path):
	values = {} # Словарь значений
	commands = [] # Список команд
	reg, prog = "", ""
	with open(path, "r") as f:                 # Чтение и разбиение файла на 2 части:
		reg, prog = f.read().split("proga")    # 1. до "proga", 2. после "proga"
	reg = re.split(r"[\n|;]+", reg)      # Разделение на одельные выражения
	prog = re.split(r"[\n|;]+", prog)    # Разделение на одельные выражения
	while ("" in reg):   #
		reg.remove("")   # Удаление пустых выражений
	while ("" in prog):  #
		prog.remove("")  #
	# Проход по объявлениям регистров
	for elem in reg:
		a = re.findall(r"^\s*\d+\s*=\s*\d+\s*$", elem)
		if (len(a) == 0):
			print("{0}: присвоение не распознано".format(elem))
			exit(1)
		else:
			b = re.findall(r"\d+", a[0])
			values.update([(b[0], int(b[1]))])
	# Проход по командам
	for elem in prog:
		a = re.findall(r"^\s*[z|Z|s|S|t|T|j|J|d|D]\s*\([\w|\s|,]*\)\s*$", elem)
		if (len(a) == 0):
			print("{0}: команда не распознана".format(elem))
			exit(1)
		else:
			commands.append(a[0])
	return commands, values

# Исполнение команды, на которую ссылается ip (начинается с 1)
# Если команда исполнена, то возвращает True, иначе False
def runner(parser, commands, values, ip):
	if (ip.ip == 0 or not (ip.ip - 1) in range(len(commands))):
		return False
	else:
		parser.command(commands[ip.ip - 1], values, ip)
		ip.ip += 1
		return True

ip = Ip()
path = "proga.test"
coms, vals = reader(path)
parser = Parser()
while (runner(parser, coms, vals, ip)):
	pass

out = sorted(vals.items(), key = lambda item: int(item[0]))
print("\nEnd of Program:")
print("ip = {0}".format(ip.ip))
for elem in out:
	print("R{0} = {1}".format(*elem))