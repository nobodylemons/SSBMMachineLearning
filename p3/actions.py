import enum
import p3.pad
from argparse import Action

class Actions(object):
#     def __init__(self):
#         print()

#     @enum.unique
#     class Action(enum.Enum):
#         LEFT_1 = 0
#         LEFT_2 = 1
#         LEFT_3 = 2
#         RIGHT_1 = 3
#         RIGHT_2 = 4
#         RIGHT_3 = 5
#         UP_1 = 6
#         UP_2 = 7
#         UP_3 = 8
#         DOWN_1 = 9
#         DOWN_2 = 10
#         DOWN_3 = 11
#         UP_LEFT = 12
#         UP_RIGHT = 13
#         DOWN_LEFT = 14
#         DOWN_RIGHT = 15
# 
#         SHIELD_DROP = 16

    def left_1(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.067, 0.25]))
        return action_list
    

    def left_2(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
        return action_list
    

    def left_3(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.067, 0.75]))
        return action_list
        

    def right_1(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.933, 0.75]))
        return action_list
    
    def right_2(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
        return action_list
    
    def right_3(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .933, 0.25]))
        return action_list
        
    def up_1(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .25, 0.933]))
        return action_list
    
    def up_2(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 1.0]))
        return action_list
    
    def up_3(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .75, 0.933]))
        return action_list
    
    def down_1(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .75, 0.067]))
        return action_list
    
    def down_2(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 0.0]))
        return action_list
    
    def down_3(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .25, 0.067]))
        return action_list
    
    def up_left(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .1464, 0.8535]))
        return action_list
    
    def up_right(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.8535, 0.8535]))
        return action_list
    
    def down_left(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, .1464, .1464]))
        return action_list
    
    def down_right(self, pad, action_list):
        action_list.append((1, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.8535, .1464]))
        return action_list
    
#         B_LEFT = 17
#         B_RIGHT = 18
#         B_UP = 19
#         B_DOWN = 20
#         B_NEUTRAL = 21
    def b_left(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.B]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        return action_list
    
    def b_right(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.B]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        return action_list
    
    def b_up(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.B]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 1.0]))
        action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        return action_list
    
    def b_down(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.B]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 0.0]))
        action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        return action_list
    
    def b_neutral(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.B]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.B]))
        return action_list
    
#         A_LEFT = 22
#         A_RIGHT = 23
#         A_UP = 24
#         A_DOWN = 25
#         A_NEUTRAL = 26
#         A_UP_LEFT = 27
#         A_UP_RIGHT = 28
#         A_DOWN_LEFT = 29
#         A_DOWN_RIGHT = 30

    def a_left(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_right(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_up(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 1.0]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_down(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 0.0]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_neutral(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_up_left(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .1464, 0.8535]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_up_right(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.8535, 0.8535]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_down_left(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .1464, .1464]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
    def a_down_right(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.A]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.8535, .1464]))
        action_list.append((1, pad.release_button, [p3.pad.Button.A]))
        return action_list
    
#         DODGE_LEFT_1 = 31
#         DODGE_LEFT_2 = 32
#         DODGE_LEFT_3 = 33
#         DODGE_RIGHT_1 = 34
#         DODGE_RIGHT_2 = 35
#         DODGE_RIGHT_3 = 36
#         DODGE_UP_1 = 37
#         DODGE_UP_2 = 38
#         DODGE_UP_3 = 39
#         DODGE_DOWN_1 = 40
#         DODGE_DOWN_2 = 41
#         DODGE_DOWN_3 = 42
#         DODGE_UP_LEFT = 43
#         DODGE_UP_RIGHT = 44
#         DODGE_DOWN_LEFT = 45
#         DODGE_DOWN_RIGHT = 46
#         DODGE_NEUTRAL = 47
    
    def dodge_left_1(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.067, 0.25]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    

    def dodge_left_2(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.0, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list

    def dodge_left_3(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.067, 0.75]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
        

    def dodge_right_1(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.933, 0.75]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_right_2(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 1.0, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_right_3(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .933, 0.25]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
        
    def dodge_up_1(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .25, 0.933]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_up_2(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 1.0]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_up_3(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .75, 0.933]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_down_1(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .75, 0.067]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_down_2(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .5, 0.0]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_down_3(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .25, 0.067]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_up_left(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .1464, 0.8535]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_up_right(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.8535, 0.8535]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_down_left(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, .1464, .1464]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_down_right(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.8535, .1464]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list
    
    def dodge_neutral(self, pad, action_list):
        action_list.append((0, pad.press_button, [p3.pad.Button.L]))
        action_list.append((0, pad.tilt_stick, [p3.pad.Stick.MAIN, 0.5, 0.5]))
        action_list.append((1, pad.release_button, [p3.pad.Button.L]))
        return action_list