import enum
import p3.pad
from argparse import Action

class Actions(object):

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