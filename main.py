from itertools import combinations_with_replacement

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

from strategy import AlwaysGoodState, TitForTat, TitForTatBad, \
                     GrimTrigger, GrimTriggerForgiveness, AlwaysBadState, \
                     AllRandom, GoodWhenOddPeriod, GoodWhenEvenPeriod, \
                     TitForTatReverse, TitForTatLast10

classes = [AlwaysGoodState,
           TitForTat,
           TitForTatBad,
           GrimTrigger,
           GrimTriggerForgiveness,
           AlwaysBadState,
           AllRandom,
           GoodWhenOddPeriod,
           GoodWhenEvenPeriod,
           TitForTatReverse,
           TitForTatLast10]
valid_actions = ['cooperate', 'defect']

R = 10000
T = 100

def play(player1, player2):
    
    actions_1, actions_2 = [None], [None]
    scores_1, scores_2 = [], []
    for period in range(1, T+1):
        action_1 = player1.decide(period, actions_1, actions_2)
        action_2 = player2.decide(period, actions_2, actions_1)
        assert action_1 in valid_actions and action_2 in valid_actions

        actions_1.append(action_1)
        actions_2.append(action_2)

        score_1, score_2 = None, None
        if action_1 == 'cooperate':
            if action_2 == 'cooperate':
                score_1, score_2 = 50, 50
            else:
                score_1, score_2 = 0, 100
        else:
            if action_2 == 'cooperate':
                score_1, score_2 = 100, 0
            else:
                score_1, score_2 = 0, 0

        scores_1.append(score_1)
        scores_2.append(score_2)
    
    return sum(scores_1), sum(scores_2)

ary = [[None] * len(classes) for i in range(len(classes))]
for (id_1, class_1), (id_2, class_2) in combinations_with_replacement(enumerate(classes), 2):
    
    sum_scores_1, sum_scores_2 = [], []
    for i in range(R):
        sum_score_1, sum_score_2 = play(class_1(), class_2())
        sum_scores_1.append(sum_score_1)
        sum_scores_2.append(sum_score_2)
    
    avg_score_1 = sum(sum_scores_1) / R
    avg_score_2 = sum(sum_scores_2) / R

    if id_1 != id_2:
        ary[id_1][id_2] = avg_score_1
        ary[id_2][id_1] = avg_score_2
    else:
        avg_score = (avg_score_1 + avg_score_2) / 2
        ary[id_1][id_1] = avg_score
    
    print(class_1.name.rjust(30), ':', avg_score_1)
    print(class_2.name.rjust(30), ':', avg_score_2)
    print('---')

df_cm = pd.DataFrame(
    ary,
    index = [c.name for c in classes],
    columns = [c.name for c in classes]
)

plt.figure()
plt.title('Simulation %d Times of %d-round Game' % (R, T))
sn.heatmap(df_cm, annot=True, fmt='g')
plt.show()