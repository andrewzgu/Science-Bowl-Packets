import csv
import shutil
import os
import re

rounds = open('rounds.csv', newline = '')
rows = list(csv.reader(rounds, delimiter=',', quotechar='"'))
properties = rows.pop(0)


if os.path.exists('splitrounds'):
  shutil.rmtree('splitrounds')
os.mkdir('splitrounds')

def texify(text):
  #Subscripts and superscripts inside math mode
  text = re.sub(r'(\s)([^$\s]*[\^_][^$\s}]*?)([\s?.])', r'\1$\2$\3', text)
  #Use enumerate environments
  for i in range(5, 1, -1):
    t1 = ''.join(str(j) + r'\)([\s\S]*)' for j in range(1, i+1))
    t2 = r'\\begin{enumerate}[label={\\arabic*}), noitemsep]' + \
            ''.join(r'\\item ' + '\\'+ str(j) for j in range(1, i+1)) + \
            r'\\end{enumerate}'
    text = re.sub(t1, t2, text)
  text = re.sub(r'W\)([\s\S]*)X\)([\s\S]*)Y\)([\s\S]*)Z\)([\s\S]*)', r'\\wxyz{\1}{\2}{\3}{\4}', text)
  #Remove all trailing whitespace
  text = re.sub(r'\s+$', r'', text)
  return text

round_numbers = {row[0] for row in rows}
for i in round_numbers:
  if i != 'Unused':
    #Opening as a regular file, so we can surround everything in { } for csvsimple
    def tex_row(row):
      return ','.join('{{{}}}'.format(texify(item)) for item in row) + '\n'
    round_writer = open('splitrounds/round{}.csv'.format(i), 'a')
    round_writer.write(tex_row(properties[1:]))
    for row in rows:
      if row[0] == i:
        round_writer.write(tex_row(row[1:]))
