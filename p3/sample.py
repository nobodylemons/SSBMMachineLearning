import p3.actions
'''
Created on Sep 7, 2017

@author: Robert
'''
from tensorflow.contrib.keras.python.keras.backend import function

class sample(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        function_names = [func for func in dir(p3.actions.Actions) if callable(getattr(p3.actions.Actions, func)) and not func.startswith('_')]
        #Every action will have some resulting states
        #Each resulting state associated with an action will have a counter
#         self.states_I_point_to = []
#         self.states_that_point_to_me = []
        self.q_arr = []
        for _ in function_names:
            self.q_arr.append(0)
#         for _ in function_names:
#             self.states_I_point_to.append(0)
#             self.states_that_point_to_me.append(0)
            
#     def increment_action_taken(self, action_num, state_location):
#         self.states_I_point_to = self.increment(action_num, state_location, self.states_I_point_to)
#                 
#     def increment_old_action(self, action_num, state_location):
#         self.states_that_point_to_me = self.increment(action_num, state_location, self.states_that_point_to_me)
#         
#     def increment(self, action_num, state_location, states):
#         loc_str = ''
#         for my_str in state_location:
#             loc_str = loc_str +',' +my_str
#         loc_str = loc_str[1:loc_str.__len__()]
#         if states[action_num] == 0:
#             locations = {}
#             locations[loc_str] = 1
#             states[action_num] = locations
#         else:
#             locations = states[action_num]
#             if locations.__contains__(loc_str):
#                 locations[loc_str] = locations[loc_str] + 1
#             else:
#                 locations[loc_str] = 1
#         return states
