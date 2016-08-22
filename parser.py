MAXN = 10000
import sys
import msd

file_name = sys.argv[1]
user_name = file_name.split('_')[0]
scene = file_name.split('_')[1]
technique = file_name.split('_')[2]

def get_time(s):
	return (float)(s.split(' ')[0])

def get_cmd(s):
	return s.split(' ')[1]

def get_result(s):
	tags = s.split(' ')
	return ' '.join(tags[2 : len(tags)])

inp = file(file_name + '.txt', 'r')
lines = inp.readlines()
inp.close()

rst = file(file_name + '.rst', 'w')
rst.write('user, scene, technique, session, index, phrase, rate, error, undo\n')

class Word:
	word = ''
	phrase = ''
	session_index = -1
	phrase_index = -1
	phrase_undo = False
	start_time = -1
	enter_time = -1
	select_time = -1
word_cnt = 0
session_index = 0
phrase_index = 0
word_index = 0
words = [Word() for i in range(0, MAXN)]

for i in range(0, len(lines)):
	lines[i] = lines[i].replace('\n', '')

	if get_cmd(lines[i]) == 'session':
		words[word_cnt].session_index = session_index = session_index + 1
		phrase_index = 0
	
	if get_cmd(lines[i]) == 'phrase':
		words[word_cnt].phrase = get_result(lines[i])
		words[word_cnt].session_index = session_index
		words[word_cnt].phrase_index = phrase_index = phrase_index + 1
	
	if get_cmd(lines[i]) == 'start':
		words[word_cnt].start_time = get_time(lines[i])
	
	if get_cmd(lines[i]) == 'click':
		words[word_cnt].word = words[word_cnt].word + '?'
	
	if get_cmd(lines[i]) == 'delete':
		if words[word_cnt].word != '':
			words[word_cnt].word = words[word_cnt][0 : -1]
		elif words[word_cnt].phrase_index == -1:
			word_cnt = word_cnt - 1
			words[word_cnt].word = ''
			if words[word_cnt].phrase_index != -1:
				words[word_cnt].phrase_undo = True

	if get_cmd(lines[i]) == 'enter':
		words[word_cnt].enter_time = get_time(lines[i])
	
	if get_cmd(lines[i]) == 'select':
		words[word_cnt].select_time = get_time(lines[i])
		words[word_cnt].word = get_result(lines[i]).split(' ')[0]
		word_cnt = word_cnt + 1

start_word = -1
letter_cnt = 0
phrase = ''

for i in range(0, word_cnt):
	word = words[i].word
	if phrase == '':
		phrase = word
	else:
		phrase = phrase + ' ' + word
	letter_cnt = letter_cnt + len(word)

	if words[i].phrase_index != -1:
		start_word = i
	
	if i == word_cnt - 1 or words[i + 1].phrase_index != -1:
		std_phrase = words[start_word].phrase
		total_time = words[i].select_time - words[start_word].start_time
		rate = letter_cnt / total_time * 12
		err = msd.msd(phrase, std_phrase)
		is_undo = ('Yes' if words[start_word].phrase_undo == True else 'No')
		rst.write(user_name + ', ' + scene + ', ' + technique + ', ' + str(words[start_word].session_index) + ', ' + phrase + ', ' + str(rate) + ', ' + str(err) + ', ' + is_undo + '\n')
		letter_cnt = 0
		phrase = ''

rst.close()
