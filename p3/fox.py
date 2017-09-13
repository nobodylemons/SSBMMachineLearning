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
        self.thirty_frames = []
        self.losing_actions = []
        self.last_four_states = [0]*4
        self.locations = {}
        self.opponent_percent,self.cpu_percent  = 0,0
        self.opponent_stocks, self.cpu_stocks = -1, -1
        self.op_x, self.op_y, self.pl_x, self.pl_y = 0,0,0,0
        self.op_facing, self.pl_facing  = 0,0
        function_names = [func for func in dir(p3.actions.Actions) if callable(getattr(p3.actions.Actions, func)) and not func.startswith('_')]
        self.a = []
        for name in function_names:
            action = p3.actions.Actions()
            self.a.append(getattr(action, name))


    def get_location_str(self, op_x, op_y, pl_x, pl_y, pl_facing, op_percent):
        distance_x = abs(op_x - pl_x)
        distance_y = abs(op_y - pl_y)
        standard_distance_x = int(5*math.log10(450/(distance_x+.1)))
        standard_distance_y = int(5*math.log10(450/(distance_y+.1)))
        above_stage = 0
        if pl_x < 68.5 and pl_x > -68.5 and pl_y >= -.2:
            above_stage = 1
        else:
            above_stage = 0
        ret_str = str(standard_distance_x)+','+str(standard_distance_y)+','+str(above_stage)+','+str(pl_facing)+','+str(int(op_percent/10))
        return ret_str
        #divider = 10
        #return str(int(op_x / divider)) + ',' + str(int(op_y / divider)) + ',' + str(int(pl_x / divider)) + ',' + str(int(pl_y / divider))

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
            #self.shinespam(pad)
            
            if self.thirty_frames.__sizeof__()>=200:
                self.losing_actions = []
                #update last 30 frames object with its outcome, and location of next 30 frames
                
                location_str = self.get_location_str(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, self.opponent_percent)
                
                if self.locations.__contains__(location_str):
                    var_list = self.locations[location_str]
                    var = var_list.pop()
                else:
                    #thirty action frames, was success, future key
                    var_list = [p3.sample.sample(0,0,[],0)]
                    var = var_list[0]

                #update success of last frames
                new_op_percent = state.players[1].percent
                new_pl_percent = state.players[2].percent
                if new_op_percent > self.opponent_percent:
                    var.last_actions_were_success = 1
                elif new_pl_percent > self.cpu_percent:
                    var.last_actions_were_success = -1
                else:
                    var.last_actions_were_success = 0
                    
                #update info on stocks
                if self.opponent_stocks == -1 or self.cpu_stocks == -1:
                    self.opponent_stocks = state.players[1].stocks
                    self.cpu_stocks = state.players[2].stocks
                elif state.players[1].stocks < self.opponent_stocks:
                    var.last_actions_were_success = 2
                elif state.players[2].stocks < self.cpu_stocks:
                    print('stock loss')
                    var.last_actions_were_success = -2
                    
                #update new locations
                self.op_x = state.players[1].pos_x
                self.op_y = state.players[1].pos_y
                self.pl_x = state.players[2].pos_x
                self.pl_y = state.players[2].pos_y
                self.op_facing = state.players[1].facing
                self.pl_facing = state.players[2].facing
                
                new_loc_str = self.get_location_str(self.op_x, self.op_y, self.pl_x, self.pl_y, self.pl_facing, new_op_percent)
                
                if self.locations.__contains__(new_loc_str):
                    #Set location of old var within var list
                    old_var_list = self.locations[location_str]
                    old_var_len = old_var_list.__len__()
                    if old_var_len > 0:
                        old_var_list[old_var_len-1].next_sample_loc_num = self.locations[new_loc_str].__len__() - 1
                    self.locations[new_loc_str].append(p3.sample.sample(self.thirty_frames, 0, 0, 0))
                else:
                    
                    self.locations[new_loc_str] = [p3.sample.sample(self.thirty_frames, 0, 0, 0)]
                
                #update pointer of last location
                var.next_sample_loc = new_loc_str
                var.last_thirty_actions = self.thirty_frames
                var_list.append(var)
                self.locations[location_str] = var_list
                self.thirty_frames = []
                self.last_four_states.pop()
                self.last_four_states.append(new_loc_str)
                
                self.opponent_percent = new_op_percent
                self.cpu_percent = new_pl_percent
                
                self.opponent_stocks = state.players[1].stocks
                self.cpu_stocks = state.players[2].stocks
                self.cpu_percent = state.players[2].stocks
                
                result_actions, indicator = self.get_actions()
                if indicator == 1:
                    self.action_list = result_actions
                else:
                    self.randomAction(pad)
                    if indicator == -1:
                        for losing_var in result_actions:
                            for losing_action in losing_var.last_thirty_actions:
                                self.losing_actions.append(losing_action)
                    
            if self.losing_actions.__len__()>0:
                self.randomAction(pad)
#                 match_exists = False
#                 for _ in self.KnuthMorrisPratt(self.losing_actions, self.action_list):
#                     match_exists = True
#                 while match_exists:
#                     self.action_list = []
#                     self.randomAction(pad)
#                     match_exists = False
#                     for _ in self.KnuthMorrisPratt(self.losing_actions, self.action_list):
#                         match_exists = True
            elif self.action_list.__len__()==0:
                self.randomAction(pad)
                for action in self.action_list:
                    self.thirty_frames.append(action)
        
    def get_actions(self):
        most_recent_state = self.last_four_states[3]
        var_list = self.locations[most_recent_state]
        if var_list.__len__() <= 1:
            return [],0
        
        #most recent var is one we just did, so ignore that
        var_list.pop(var_list.__len__()-1)
        
        winning_var_list = []
        losing_var_list = []
        for var in var_list:
            #if next action was success, add to success list
            fewest_steps = 1000
            fewest_steps_loc = []
            #get list of vars that match the location
            if not var.next_sample_loc == 0:
                next_var_list = self.locations[var.next_sample_loc]
                #filter by next sample location num
                next_var = next_var_list[var.next_sample_loc_num]
                _, steps_to_winning_stock = self.steps_to_winning_stock(0, next_var)
                if steps_to_winning_stock > 0:
                    print('stock win path found '+str(steps_to_winning_stock)+' steps in the future')
                    winning_var_list.append([next_var, steps_to_winning_stock])
                    if steps_to_winning_stock < fewest_steps:
                        fewest_steps = steps_to_winning_stock
                        fewest_steps_loc = [winning_var_list.__len__()-1]
                    elif steps_to_winning_stock == fewest_steps:
                        fewest_steps_loc.append(winning_var_list.__len__()-1)
                elif steps_to_winning_stock < -1:
                    print('...stock loss path found '+str(-1*steps_to_winning_stock)+' steps in the future')
                    losing_var_list.append(next_var)
        
        if losing_var_list.__len__()>0:
            return losing_var_list,-1
        if winning_var_list.__len__()==0:
            return [],0
        if fewest_steps == 1000:
            return [],0
        
        winning_var_loc = random.randint(0, fewest_steps_loc.__len__()-1)
        [var, _] = winning_var_list[winning_var_loc]
        #return actions of winning game
        print('executing winning actions')
        return var.last_thirty_actions,1

    def steps_to_winning_stock(self, steps, var):
        if var.last_actions_were_success==2:
            return var, steps
        elif var.last_actions_were_success==-2:
            return var, steps*-1
        elif var.next_sample_loc==0 or steps > 1000:
            return var, -1
        else:
            steps = steps + 1
            next_var_list = self.locations[var.next_sample_loc]
            #filter by next sample location num
            next_var = next_var_list[var.next_sample_loc_num]
            return self.steps_to_winning_stock(steps+1, next_var)
    
    # Knuth-Morris-Pratt string matching
    # David Eppstein, UC Irvine, 1 Mar 2002
    def KnuthMorrisPratt(self, text, pattern):
        # allow indexing into pattern and protect against change during yield
        pattern = list(pattern)
    
        # build table of shift amounts
        shifts = [1] * (len(pattern) + 1)
        shift = 1
        for pos in range(len(pattern)):
            while shift <= pos and pattern[pos] != pattern[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos+1] = shift
    
        # do the actual search
        startPos = 0    
        matchLen = 0
        for c in text:
            while matchLen == len(pattern) or \
                  matchLen >= 0 and pattern[matchLen] != c:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == len(pattern):
                yield startPos
                
    def shinespam(self, pad):
        self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.0])) #Tilt stick down
        self.action_list.append((0, pad.press_button, [p3.pad.Button.B]))           #Press B
        self.action_list.append((1, pad.release_button, [p3.pad.Button.B]))         #Release B
        self.action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5])) #Bring stick to neutral
        self.action_list.append((0, pad.press_button, [p3.pad.Button.X]))           #Press X
        self.action_list.append((1, pad.release_button, [p3.pad.Button.X]))         #Release X
        self.action_list.append((1, None, []))

    def randomAction(self, pad):
        randint = random.randint( 0, self.a.__len__()-1 )
        func = self.a[randint]
        self.action_list = func(pad, self.action_list)
        
    def shielddrop(self, pad):
        self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .0, 0.5]))
        self.action_list.append((1, pad.press_button, [p3.pad.Button.L]))
        self.action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.1625, 0.164]))
        self.action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        
        