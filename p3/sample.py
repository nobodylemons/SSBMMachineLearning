import p3.actions
'''
Created on Sep 7, 2017

@author: Robert
'''

class sample(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        function_names = [func for func in dir(p3.actions.Actions) if callable(getattr(p3.actions.Actions, func)) and not func.startswith('_')]
        self.rewards = []
        for _ in function_names:
            self.rewards.append(0)
            
    def set_reward(self, action_num, reward):
        self.rewards[action_num] = reward