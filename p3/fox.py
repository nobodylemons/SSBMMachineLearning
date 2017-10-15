from __future__ import generators
import p3.actions
import p3.sample
import random
import math
import p3.location_structure
from numpy.lib.type_check import _getmaxmin
from numpy.ma.core import getmask

class Fox:
    def __init__(self):
        self.actions_so_far = []
        self.action_list = []
        self.last_action = 0
        self.locations = p3.location_structure.LocationStruct()
        self.action_of_last_state = 0
        self.first_round = True
        self.opponent_percent, self.player_percent  = 0,0
        self.op_x, self.op_y, self.pl_x, self.pl_y = 0,0,0,0
        self.op_facing, self.pl_facing  = 0,0
        self.pl_action_state, self.op_action_state = 0, 0
        self.op_vel_x, self.op_vel_y = 0,0
        self.sd = 0
        self.total_sds = 0
        self.reward = 0
        location_str_arr = self.get_location_str_arr(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, self.op_facing, self.opponent_percent, self.op_action_state, self.pl_action_state, self.op_vel_x, self.op_vel_y)
        self.locations.add(location_str_arr, p3.sample.sample())
#         self.locations_len = self.locations.__len__()
        self.count = 1
        function_names = [func for func in dir(p3.actions.Actions) if callable(getattr(p3.actions.Actions, func)) and not func.startswith('_')]
        self.a = []
        for name in function_names:
            action = p3.actions.Actions()
            self.a.append(getattr(action, name))

    def getAngle360(self, distance_x, distance_y, angle):
        if distance_x <= 0 and distance_y >= 0:
            return 180+angle
        if distance_x <= 0 and distance_y <= 0:
            return 180+angle 
        if distance_x >= 0 and distance_y <= 0:
            return 360+angle
        return angle

    def get_location_str_arr(self, op_x, op_y, pl_x, pl_y, pl_facing, op_facing, op_percent, op_action_state, pl_action_state, op_vel_x, op_vel_y):
        distance_x = op_x - pl_x
        distance_y = op_y - pl_y
        if distance_x == 0:
            distance_x = .01
        angle = math.atan(distance_y/distance_x)*180/math.pi
        angle = self.getAngle360(distance_x, distance_y, angle)
        standard_distance_x = math.log10(450/(abs(distance_x)+.1))
        standard_distance_y = math.log10(450/(abs(distance_y)+.1))
        radial_distance = int(math.sqrt(standard_distance_x*standard_distance_x+standard_distance_y*standard_distance_y))
        if distance_x<0:
            standard_distance_x = standard_distance_x*-1
        if distance_y<0:
            standard_distance_y = standard_distance_y*-1

        ret_str_arr = []
        ret_str_arr.extend([
        '%(pl_x)s' % {"pl_x": int(pl_x/20)}, \
        '%(pl_y)s' % {"pl_y": int(pl_y/20)}, \
        '%(pl_facing)s' % {"pl_facing": pl_facing}, \
#         '%(pl_action_state)x' % {"pl_action_state": int(str(pl_action_state))}, \
        '%(rad_distance)s' % {"rad_distance": radial_distance}, \
#         '%(op_action_state)x' % {"op_action_state": int(str(op_action_state))}, \
        '%(op_percent)s' % {"op_percent": int(op_percent/10)}, \
        '%(op_facing)s' % {"op_facing": op_facing}, \
        '%(angle)s' % {"angle": int(angle/45)*45}])
        return ret_str_arr

    def determine_reward(self, state, player_num, opponent_num):
        reward = 0
        if state.players[player_num].sd > self.sd:
            self.total_sds = self.total_sds + 1
            reward = -2
            self.reward = self.reward + -1
        elif state.players[opponent_num].action_state is p3.state.ActionState.DeadDown and self.op_action_state is not p3.state.ActionState.DeadDown:
            reward = 1.5
            self.reward = self.reward + 1
        elif state.players[player_num].action_state is p3.state.ActionState.DeadDown and self.pl_action_state is not p3.state.ActionState.DeadDown:
            reward = -1
            self.reward = self.reward + -1
        else:
            opponent_damage_given = state.players[opponent_num].percent - self.opponent_percent
            player_damage_taken = state.players[player_num].percent - self.player_percent
            reward = (1.5*opponent_damage_given - player_damage_taken)/150
            if reward == 0:
                reward = -.01
            self.reward = self.reward + reward
        return reward


    def update_data(self, state, player_num, opponent_num):
        #update new locations
        self.op_x = state.players[opponent_num].pos_x
        self.op_y = state.players[opponent_num].pos_y
        self.pl_x = state.players[player_num].pos_x
        self.pl_y = state.players[player_num].pos_y
        self.op_facing = state.players[opponent_num].facing
        self.pl_facing = state.players[player_num].facing
        self.opponent_percent = state.players[opponent_num].percent
        self.player_percent = state.players[player_num].percent
        self.pl_action_state = state.players[player_num].action_state
        self.op_action_state = state.players[opponent_num].action_state
        self.op_vel_x = state.players[opponent_num].self_air_vel_x
        self.op_vel_y = state.players[opponent_num].self_air_vel_y
        self.sd = state.players[player_num].sd

    def advance(self, state, pad, player_num, opponent_num, locations):
        if not locations == {} and not locations is None:
            self.locations = locations
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
                old_location_str_arr = self.get_location_str_arr(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, self.op_facing, self.opponent_percent, self.op_action_state, self.pl_action_state, self.op_vel_x, self.op_vel_y)
                old_sample = self.locations.get(old_location_str_arr)
        
                instantaneous_reward = self.determine_reward(state, player_num, opponent_num)
                
#                 self.update_nearest_neighbors(old_location_str_arr)
                
                self.update_data(state, player_num, opponent_num)
                
                new_loc_str_arr = self.get_location_str_arr(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing,self.op_facing, self.opponent_percent, self.op_action_state, self.pl_action_state, self.op_vel_x, self.op_vel_y)
                
                #In the old sample, make sure to increment how many times we took an action, and what sample it led to
#                 old_sample.increment_action_taken(self.action_of_last_state, new_loc_str_arr)
                
                if not self.locations.__contains__(new_loc_str_arr):
                    self.locations.add(new_loc_str_arr, p3.sample.sample())
                
                new_sample = self.locations.get(new_loc_str_arr)
                
#                 new_sample.increment_old_action(self.action_of_last_state, old_location_str_arr)
                
#                 alpha = .1
#                 if instantaneous_reward == -2:
#                     self.sd_update_q(old_location_str_arr, alpha)
#                 else:
                self.update_q(old_sample, new_sample, instantaneous_reward, self.action_of_last_state, .001, .9)
                best_action_num = self.find_best_action(new_sample)
                self.performAction(pad, best_action_num)
                self.action_of_last_state = best_action_num
        return self.locations
          
    def sd_update_q(self, loc_str_array, alpha):
        num_ignored_attributes = 5
        pl_loc_array = loc_str_array[0: loc_str_array.__len__()-num_ignored_attributes]
        pl_map_tree = self.locations.get(pl_loc_array)
        self.recurse_me(alpha, pl_map_tree)
        
    def recurse_me(self, alpha, pl_map_tree):
        if type(pl_map_tree) is p3.sample.sample:
            self.update_q(pl_map_tree, -1, [], alpha)
        else:
            for map_tree in pl_map_tree.keys():
                self.recurse_me(alpha, pl_map_tree[map_tree])
        
    def performAction(self, pad, action_num):
        func = self.a[action_num]
        self.action_list = func(pad, self.action_list)
    
    def update_nearest_neighbors(self, old_location_str_arr):
        nearest_neighbors = self.locations.get(old_location_str_arr[0:old_location_str_arr.__len__()-2])  
        if nearest_neighbors.__len__()>1:
            for key in nearest_neighbors.keys():
                for second_key in nearest_neighbors[key].keys():
                    done_key = old_location_str_arr[old_location_str_arr.__len__()-1]
                    if second_key is not done_key:
                        obj = nearest_neighbors[key][second_key]
                        obj.q = .9*obj.q + .1*self.locations.get(old_location_str_arr).q 
                
    
    def update_q(self, old_sample, new_sample, reward, action_num, alpha, gamma):
        old_q = old_sample.q_arr[action_num]
        old_sample.q_arr[action_num] = old_q + alpha*(reward + gamma*self.getMax(new_sample.q_arr)- old_q)
        
    def getMax(self, q_arr):
        max_q = -10000;
        for q in q_arr:
            if q > max_q:
                max_q = q
            if q == max_q:
                if random.randint( 0, 1 ):
                    max_q = q
        if q==-10000:
            return random.randint( 0, q_arr.__len__()-1 )
        return q_arr.index(max_q)

#         for action in range(0,last_sample.states_that_point_to_me.__len__()):
#             locations_map = last_sample.states_that_point_to_me[action]
#             if locations_map is not 0:
#                 for location in locations_map.keys():
#                     if not covered_states.__contains__(location):
#                         covered_states.append(location)
#                         loc_arr = location.split(',')
#                         if not loc_arr[3] is int(str(p3.state.ActionState.DeadDown)) and not loc_arr[5] is int(str(p3.state.ActionState.DeadDown)) and covered_states.__len__()<500:
#                             old_sample = self.locations.get(loc_arr)
#                             old_sample.q = old_sample.q + alpha*(reward+.9*last_sample.q - old_sample.q)
#                             self.update_q(old_sample, reward, covered_states, alpha)
        
    
    def find_best_action(self, sample):
        if self.count > .001:
            self.count = self.count*.99999#99
        #return best action number for sample to take
        if random.random() < self.count:
            return random.randint( 0, self.a.__len__()-1 )
        
#         best_action = 0
#         max_weighted_q = -10000;
        return self.getMax(sample.q_arr)
        #every action has a locations_map with many possible states
#         for action in range(0,sample.states_I_point_to.__len__()):
#             locations_map = sample.states_I_point_to[action]
#             if locations_map is not 0:
#                 total = 0
#                 factor_total = 0
#                 for location in locations_map.keys():
#                     total = total + locations_map[location]
#                     loc_arr = location.split(',')
#                     q = self.locations.get(loc_arr).q
#                     factor_total = factor_total + q*locations_map[location]
#                 
#                 weighted_q = factor_total/total
#                 if weighted_q > max_weighted_q:
#                     max_weighted_q = weighted_q
#                     best_action = action
#         if max_weighted_q == -10000:
#             return random.randint( 0, self.a.__len__()-1 )
#         return best_action
        
        