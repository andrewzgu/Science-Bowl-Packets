#!/usr/bin/env python3
import sys
import csv
import random

round_schema = [[1, 2]]*5 + [
  [1.5, 3],
  [1.5, 3],
  [2, 5],
  [2, 5],
  [3, 6],
  [3, 6],
  [4, 7],
  [4, 7],
]

type_col = 'Toss up/Bonus'
cat_col = 'Category'
diff_col = 'Difficulty'
pair_col = 'PairingID'

with open(sys.argv[1], newline='') as csvfile:
  rows = list(csv.reader(csvfile, delimiter = ',', quotechar='"'))
  properties = rows.pop(0)
  questions = []
  for i, row in enumerate(rows):
    q = dict(zip(properties, row))
    q.update({'id': i})
    q[diff_col] = float(q[diff_col]) if q[diff_col] != '' else 4
    questions.append(q)

categories = list({q[cat_col] for q in questions})
used_question_ids = set()
question_pairs = []

for category in categories:
  category_tossups = sorted([q for q in questions if q[type_col] == 'Toss up' and q[cat_col] == category], key=lambda x: x[diff_col])
  category_bonuses = sorted([q for q in questions if q[type_col] == 'Bonus' and q[cat_col] == category], key=lambda x: x[diff_col])
  for tossup in category_tossups.copy():
    if tossup[pair_col] != '':
      try:
        bonus = next(q for q in category_bonuses if q[pair_col] == tossup[pair_col])
        question_pairs.append([tossup, bonus, (tossup[diff_col]+bonus[diff_col])/2])
        category_tossups.remove(tossup)
        category_bonuses.remove(bonus)
      except:
        print('failed to find paired bonus', tossup)
  category_tossups.sort(key = lambda x: x[diff_col])
  category_bonuses.sort(key = lambda x: x[diff_col])
  while len(category_tossups) > 0 and len(category_bonuses) > 0:
    tossup = category_tossups.pop(0)
    bonus = category_bonuses.pop(0)
    question_pairs.append([tossup, bonus, (tossup[diff_col]+bonus[diff_col])/2])

questions_per_round = 23
recency_factor = [0.4, 0.2, 0.0]

import os
if os.path.exists('rounds.csv'):
  os.remove('rounds.csv')
round_writer = csv.writer(open('rounds.csv', 'w', newline=''), delimiter = ',', quotechar='"')
round_writer.writerow(['Round'] + properties)

used_question_ids = set()

for i, round in enumerate(round_schema):
  category_pools = {}
  category_distribution = {cat: 0 for cat in categories}
  round_length = 0
  recent_categories = [''] * len(recency_factor)
  for category in categories:
    category_pools[category] = [pair for pair in question_pairs if pair[0][cat_col] == category and pair[0]['id'] not in used_question_ids and round[0] <= pair[2] <= round[1]]
  number_of_questions = min(questions_per_round, sum([len(category_pools[category]) for category in categories]))
  while round_length < questions_per_round:
    #The weight factor below will tend to pick categories that have not appeared
    #as often in the given round, and also avoid categories that recently appeared.
    recencies = {cat: 1 for cat in categories}
    recencies[''] = 1
    for index, cat in enumerate(recent_categories):
      recencies[cat] *= recency_factor[index]
    weights = [recencies[category] * min(len(category_pools[category]), 2**(-category_distribution[category])) for category in categories]
    if sum(weights) <= 0:
      break
    category = random.choices(population=categories, weights=weights, k=1)[0]
    if len(category_pools[category]) > 0:
      pair = random.choice(category_pools[category])
      round_writer.writerow([i+1] + rows[pair[0]['id']])
      round_writer.writerow([i+1] + rows[pair[1]['id']])
      category_pools[category].remove(pair)
      used_question_ids.add(pair[0]['id'])
      used_question_ids.add(pair[1]['id'])
      category_distribution[pair[0][cat_col]] += 1
      recent_categories.pop(0)
      recent_categories.append(pair[0][cat_col])
      round_length += 1
for q in questions:
  if q['id'] not in used_question_ids:
    round_writer.writerow(['Unused'] + rows[q['id']])
