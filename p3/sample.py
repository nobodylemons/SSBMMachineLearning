'''
Created on Sep 7, 2017

@author: Robert
'''

class sample(object):
    '''
    classdocs
    '''
    

    def __init__(self, last_thirty_actions, last_actions_were_success, next_sample_loc, next_sample_loc_num):
        '''
        Constructor
        '''
        self.last_thirty_actions = last_thirty_actions
        self.last_actions_were_success = last_actions_were_success
        self.next_sample_loc = next_sample_loc
        self.next_sample_loc_num = next_sample_loc_num
            