from __future__ import generators
import p3.pad
import p3.actions
import p3.sample
import random
import math
from p3 import state_manager


class Fox:
    def __init__(self):
        self.action_list = []
        self.last_action = 0
        self.locations = {}
        self.action_of_last_state = 0
        self.first_round = True
        self.opponent_percent  = 0
        self.opponent_stocks, self.cpu_stocks = -1, -1
        self.op_x, self.op_y, self.pl_x, self.pl_y = 0,0,0,0
        self.op_facing, self.pl_facing  = 0,0
        
        location_str = self.get_location_str(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, self.opponent_percent)
        self.locations[location_str] = p3.sample.sample()
        
        function_names = [func for func in dir(p3.actions.Actions) if callable(getattr(p3.actions.Actions, func)) and not func.startswith('_')]
        self.a = []
        for name in function_names:
            action = p3.actions.Actions()
            self.a.append(getattr(action, name))


    def get_location_str(self, op_x, op_y, pl_x, pl_y, pl_facing, op_percent):
        distance_x = op_x - pl_x
        distance_y = op_y - pl_y
        standard_distance_x = int(5*math.log10(450/(abs(distance_x)+.1)))
        standard_distance_y = int(5*math.log10(450/(abs(distance_y)+.1)))
        if distance_x<0:
            standard_distance_x = standard_distance_x*-1
        if distance_y<0:
            standard_distance_y = standard_distance_y*-1

        ret_str = str(standard_distance_x)+','+str(standard_distance_y)+','+str(int(pl_x/20))+','+str(int(op_percent/10))+','+str(pl_facing)
        return ret_str


    def determine_reward(self, state):
        reward = 0
    #update info on stocks
        if self.opponent_stocks == -1 or self.cpu_stocks == -1:
            self.opponent_stocks = state.players[1].stocks
            self.cpu_stocks = state.players[2].stocks
        elif state.players[1].stocks < self.opponent_stocks:
            reward = 1
            print('stock win')
        elif state.players[2].stocks < self.cpu_stocks:
            print('stock loss')
            reward = -1
        return reward


    def update_data(self, state):
        #update new locations
        self.op_x = state.players[1].pos_x
        self.op_y = state.players[1].pos_y
        self.pl_x = state.players[2].pos_x
        self.pl_y = state.players[2].pos_y
        self.op_facing = state.players[1].facing
        self.pl_facing = state.players[2].facing
        self.opponent_percent = state.players[1].percent
        self.opponent_stocks = state.players[1].stocks
        self.cpu_stocks = state.players[2].stocks

    def advance(self, state, pad):
        
        while self.action_list:
            wait, func, args = self.action_list[0]
            if state.frame - self.last_action < wait:
                return
            else:
                self.action_list.pop(0)
                if func is not None:
                    func(*args)
                self.last_action = state.frame
        else:
            if self.first_round:
                self.performAction(pad, self.action_of_last_state)
                self.first_round = False
            else:
                old_location_str = self.get_location_str(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, self.opponent_percent)
                old_sample = self.locations[old_location_str]
                #update success of last frames
                
                reward = self.determine_reward(state)
    
                self.locations[old_location_str] = self.update_reward(old_sample, self.action_of_last_state, reward)
                
                self.update_data(state)
                
                new_loc_str = self.get_location_str(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, self.opponent_percent)
                
                if not self.locations.__contains__(new_loc_str):
                    self.locations[new_loc_str] = p3.sample.sample()
                
                best_action_num = self.find_best_action(self.locations[new_loc_str])
                self.performAction(pad, best_action_num)
                self.action_of_last_state = best_action_num
    
    def randomAction(self, pad):
        randint = random.randint( 0, self.a.__len__()-1 )
        func = self.a[randint]
        self.action_list = func(pad, self.action_list)
        
    def performAction(self, pad, action_num):
        func = self.a[action_num]
        self.action_list = func(pad, self.action_list)
    
    def update_reward(self, sample, action_num, reward):
        #Update reward of old action based on the reward of the last action it took
        past_reward = sample.rewards[action_num]
        return sample
    
    def find_best_action(self, sample):
        #return best action number for sample to take
        
        return random.randint( 0, self.a.__len__()-1 )
        
    def shielddrop(self, pad):
        self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .0, 0.5]))
        self.action_list.append((1, pad.press_button, [p3.pad.Button.L]))
        self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.1625, 0.164]))
        self.action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        
        