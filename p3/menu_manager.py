import math

import p3.pad

class MenuManager:
    def __init__(self):
        self.selected_fox = False
        self.selected_falcon = False
        self.pressed_back = False
        self.pressed_menu_button = False
        self.dual_1v1_ready = False
        self.menu_state = 0
        self.pressed_a = False
        self.changed_color = False
        self.pressed_start = False

    def pick_fox(self, state, pad):
        if self.selected_fox:
            # Release buttons and lazilly rotate the c stick.
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            angle = (state.frame % 240) / 240.0 * 2 * math.pi
            pad.tilt_stick(p3.pad.Stick.C, 0.4 * math.cos(angle) + 0.5, 0.4 * math.sin(angle) + 0.5)
        else:
            # Go to fox and press A
            target_x = -23.5
            target_y = 11.5
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            print(str(state.players[2].cursor_x)+','+str(state.players[2].cursor_y))
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 0.3:
                pad.press_button(p3.pad.Button.A)
                self.selected_fox = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)
    
    def pick_falcon(self, state, pad, player_num):
        self.selected_falcon = self.press_a(state, pad, player_num, self.selected_falcon, 18.3, 19.1)
    
    def press_back_button(self, state, pad, player_num):      
        self.pressed_back = self.press_a(state, pad, player_num, self.pressed_back, 26, 25)
    def press_menu_button(self, state, pad, player_num):
        self.pressed_menu_button = self.press_a(state, pad, player_num, self.pressed_menu_button, 0, 25)
    def change_color(self, state, pad, player_num):
        if player_num == 0:
            #-22.4, -3.4
            self.changed_color = self.press_a(state, pad, player_num, self.changed_color, -22.4, -3.4)
        elif player_num == 1:
            #-10, -3.4
            self.changed_color = self.press_a(state, pad, player_num, self.changed_color, -10, -3.4)
            
#         print(str(state.players[1].cursor_x)+','+str(state.players[1].cursor_y))
            
    def press_a(self, state, pad, player_num, self_bool, target_x, target_y):
        if self_bool:
            # Release buttons and lazilly rotate the c stick.
            pad.release_button(p3.pad.Button.A)
            pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
#             angle = (state.frame % 240) / 240.0 * 2 * math.pi
#             pad.tilt_stick(p3.pad.Stick.C, 0.4 * math.cos(angle) + 0.5, 0.4 * math.sin(angle) + 0.5)
        else:
            dx = target_x - state.players[player_num].cursor_x
            dy = target_y - state.players[player_num].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 2:
                pad.press_button(p3.pad.Button.A)
                return True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)
                return self_bool
                
    def set_dual_1v1(self, state, pad):
        if self.menu_state==0:
            self.pick_falcon(state, pad, 0)
            if self.selected_falcon == True:
                self.menu_state = 1
        elif self.menu_state == 1:
            self.press_back_button(state, pad, 0)
            if state.players[0].cursor_x < .0001: #if we are at the select screen menu
                self.menu_state = 2
                self.frame = state.frame
        elif self.menu_state == 2:
            d_frame = state.frame - self.frame
            if state.frame - self.frame > 70 and state.frame - self.frame < 75:
                pad.release_button(p3.pad.Button.A)
                if d_frame == 71 or d_frame == 73:
                    pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0)
                else:
                    pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            elif state.frame - self.frame >= 74:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
                self.menu_state = 3
                self.frame = state.frame 
            
        elif self.menu_state == 3:
            if state.frame - self.frame > 2  and state.frame - self.frame < 4:
                pad.press_button(p3.pad.Button.A)
            elif state.frame - self.frame >=4:
                pad.release_button(p3.pad.Button.A)
                self.frame = state.frame 
                self.menu_state = 4
        elif self.menu_state == 4:
            if state.frame - self.frame > 10 and state.frame - self.frame < 17:
                pad.release_button(p3.pad.Button.A)
                if state.frame - self.frame  == 11 or state.frame - self.frame  == 13 or state.frame - self.frame  == 15:
                    pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0)
                else:
                    pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            elif state.frame - self.frame >= 16:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
                self.menu_state = 5
                self.frame = state.frame 
        elif self.menu_state == 5:
            if state.frame - self.frame > 2  and state.frame - self.frame < 4:
                pad.press_button(p3.pad.Button.A)
            elif state.frame - self.frame >=4:
                pad.release_button(p3.pad.Button.A)
                self.frame = state.frame 
                self.menu_state = 6
                self.selected_falcon = False
        elif self.menu_state == 6:
            self.pick_falcon(state, pad, 0)
            if self.selected_falcon:
                self.menu_state = 7
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
        elif self.menu_state == 7:
            self.press_menu_button(state, pad, 0)
            if self.pressed_menu_button:
                self.menu_state = 8
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
                pad.release_button(p3.pad.Button.A)
                self.frame = state.frame
        elif self.menu_state == 8:
            if state.frame - self.frame > 5 and state.frame - self.frame < 7:
                pad.press_button(p3.pad.Button.A)
            elif state.frame - self.frame >= 7:
                pad.release_button(p3.pad.Button.A)
                self.frame = state.frame
                self.menu_state = 9
        elif self.menu_state == 9:
            if state.frame - self.frame > 10 and state.frame - self.frame < 13:
                if state.frame - self.frame == 11:
                    pad.tilt_stick(p3.pad.Stick.MAIN, 0, 0.5)
                else:
                    pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
            elif state.frame - self.frame == 15:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
                pad.press_button(p3.pad.Button.B)
            elif state.frame - self.frame > 15:
                pad.release_button(p3.pad.Button.B)
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5, 0.5)
                self.dual_1v1_ready = True
                self.selected_falcon = False   
                self.menu_state = 10
    
    def press_start_lots(self, state, pad):
        if state.frame % 2 == 0:
            pad.press_button(p3.pad.Button.START)
        else:
            pad.release_button(p3.pad.Button.START)
