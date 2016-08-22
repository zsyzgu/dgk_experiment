import os

def merge_files(file_class):
	files = os.listdir('.')
	oup = file('total.' + file_class, 'w')

	first_file = True
	for file_name in files:
		if file_name[0 : 5] != 'total' and file_name[-len(file_class) : ] == file_class:
			inp = file(file_name, 'r')
			lines = inp.readlines()
			inp.close()
			os.remove(file_name)
			if first_file and len(lines) > 0:
				oup.write(lines[0])
			for i in range(1, len(lines)):
				oup.write(lines[i])
	
	oup.close()

files = os.listdir('.')

for file_name in files:
	tags = file_name.split('.')
	if len(tags) > 0 and tags[len(tags) - 1] == 'txt':
		print file_name
		os.system('python parser.py ' + '.'.join(tags[0 : len(tags) - 1]))

merge_files('rst')
