from random import random as rand

class Strategy(object):

    def __init__(self):
        self.state = None
        self.name = 'Base Strategy'

    def decide(self, period, actions_own, actions_opponent):
        pass

class AlwaysGoodState(Strategy):

    name = 'All Good'

    def decide(self, period, actions_own, actions_opponent):

        if period == 1:
            self.state = "good"
        
        if self.state == "good":
            action = "cooperate"
        else:
            action = "defect"
        
        return action

class TitForTat(Strategy):

    name = 'Tit Tat'

    def decide(self, period, actions_own, actions_opponent):

        if period == 1:
            action = "cooperate"
        
        if period > 1:
            action = actions_opponent[period-1]
        
        return action

class TitForTatBad(Strategy):

    name = 'Tit Tat Bad'

    def decide(self, period, actions_own, actions_opponent):

        if period == 1:
            action = "defect"
        
        if period > 1:
            action = actions_opponent[period-1]
        
        return action

class GrimTrigger(Strategy):

    name = 'Grim Trigger'

    def decide(self, period, actions_own, actions_opponent):
        # set the starting state
        if period == 1:
            self.state = "good"
            action = "cooperate"

        # set state-switching criteria
        if self.state == "good" and period > 1 and actions_opponent[period-1] == "defect":
            self.state = "bad"

        if self.state == "good":
            action = "cooperate"
        else:
            action = "defect"
        
        return action

class GrimTriggerForgiveness(Strategy):

    name = 'Grim Trigger F'

    def decide(self, period, actions_own, actions_opponent):
        # set the starting state
        if period == 1:
            self.state = "good"
            action = "cooperate"
        
        # set state-switching criteria: from good to bad
        if self.state == "good" and period > 1 and actions_opponent[period-1] == "defect":
            self.state = "bad"

        # set state-switching criteria:from bad to good
        # random forgiveness with probability 0.2
        if self.state == "bad" and rand() < 0.2:
            self.state = "good"

        # set action rule
        if self.state == "good":
            action = "cooperate"
        else:
            action = "defect"
        
        return action

class AlwaysBadState(Strategy):

    name = 'All Bad'

    def decide(self, period, actions_own, actions_opponent):

        if period == 1:
            self.state = "bad"
        
        if self.state == "good":
            action = "cooperate"
        else:
            action = "defect"
        
        return action

class AllRandom(Strategy):
    
    name = 'All Random'

    def decide(self, period, actions_own, actions_opponent):

        if rand() > 0.5:
            action = "cooperate"
        else:
            action = "defect"
        
        return action