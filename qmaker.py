import sys
import random

f = open('questions.csv', 'a+')

def fake_question():
  values = []
  values.append(['Toss up', 'Bonus'][random.randint(0, 1)])

  categories = ['Energy', 'Chemistry', 'Biology', 'Math', 'Physics', 'Earth and Space']
  values.append(categories[random.randint(0, len(categories)-1)])
  values.append(['Short Answer', 'Multiple Choice'][random.randint(0, 1)])
  values.append('This is a random question. Here is a random number: {}'.format(random.randint(0, 10**10)))
  values.append(str(random.randint(0, 10**10)))
  values.append('')
  values.append('')
  values.append(str(random.uniform(1, 7)))
  values.append('Random Question Generator')
  for i in range(4):
    values.append('')
  
  return ','.join(values)

for i in range(500):
  f.write(fake_question() + "\n")
