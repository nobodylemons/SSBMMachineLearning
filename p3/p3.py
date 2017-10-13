import time
import csv
import os
import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager
import p3.stats
import p3.dolphin
import subprocess


def find_dolphin_dir():
    """Attempts to find the dolphin user directory. None on failure."""
    candidates = ['~/.dolphin-emu','~/Library/Application Support/Dolphin', '/usr/local/share/dolphin-emu/sys']
    for candidate in candidates:
        path = os.path.expanduser(candidate)
        if os.path.isdir(path):
            return path
    return None

def write_locations(dolphin_dir, locations):
    """Writes out the locations list to the appropriate place under dolphin_dir."""
    path = dolphin_dir + '/MemoryWatcher/Locations.txt'
    with open(path, 'w') as f:
        f.write('\n'.join(locations))

        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not detect dolphin directory.')
            return

def run(fox, state, sm, mw, pads, stats, locations):
    mm = []
    for _ in range(0,4):
        """Menu manager is the object used to select characters and set dual 1v1 fighting mode"""
        mm.append(p3.menu_manager.MenuManager())

    while True:
#         pads[0].frame_advance_press()
        last_frame = state.frame
        res = next(mw)
#         print(state.frame - last_frame)
        if res is not None:
            sm.handle(*res)
        if state.frame > last_frame:
            stats.add_frames(state.frame - last_frame)
            start = time.time()
            make_action(state, pads, mm, fox, locations)
            stats.add_thinking_time(time.time() - start)
#         pads[0].frame_advance_release()

def make_action(state, pads, mm, fox, locations):
    if state.menu == p3.state.Menu.Game:
        #locations = fox.advance(state, pads[0], 0, 1, locations)
        locations = fox[0].advance(state=state, pad=pads[0], player_num=0, opponent_num=1, locations=locations)
        locations = fox[1].advance(state=state, pad=pads[1], player_num=1, opponent_num=0, locations=locations)
        locations = fox[2].advance(state=state, pad=pads[2], player_num=2, opponent_num=3, locations=locations)
        locations = fox[3].advance(state=state, pad=pads[3], player_num=3, opponent_num=2, locations=locations)
        if state.frame % 1000 == 0:
            average_reward = 0
            distinct_states = 0
            sds = 0
            epsilon = 0
            for singlefox in fox:
                average_reward = average_reward + (singlefox.reward/4)
                distinct_states = singlefox.locations.size
                sds = sds + singlefox.total_sds
                epsilon = singlefox.count
                singlefox.reward = 0
                singlefox.total_sds = 0
#           ['Frame Number']+['Distinct States']+['Average Reward']+['SDs per 1000 States']+['Epsilon']
            path = os.path.dirname(os.path.realpath(__file__)) + "/stats.csv"
            with open(path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([state.frame]+[distinct_states]+[average_reward/1000]+[sds]+[epsilon])
                csvfile.close()
    elif state.menu == p3.state.Menu.Characters:
        if mm[0].dual_1v1_ready == False:
            mm[0].set_dual_1v1(state, pads[0])
        else:
            if mm[1].pressed_a and mm[2].pressed_a and mm[3].pressed_a:
                for i in range(1,4):
                    pads[i].reset()
                if mm[0].changed_color == False:
                    mm[0].change_color(state, pads[0], 0)
                if mm[1].changed_color == False:
                    mm[1].change_color(state, pads[1], 1)
                if mm[0].changed_color and mm[1].changed_color and mm[0].pressed_start == False:
                        pads[0].press_button(p3.pad.Button.START)
                        mm[0].pressed_start = True
                elif mm[0].pressed_start:
                    for pad in pads:
                        pad.reset()
                elif mm[0].changed_color and mm[1].changed_color:
                    mm[0].global_menu_state = mm[0].global_menu_state + 1
            else:
                for i in range(1,4):
                    if mm[i].selected_falcon == False:
                        mm[i].pick_falcon(state=state, pad=pads[i], player_num=i)
                    if mm[i].selected_falcon and mm[i].pressed_a==False:
                        pads[i].press_button(p3.pad.Button.A)
                        mm[i].pressed_a=True   
    elif state.menu == p3.state.Menu.Stages:
        # Handle this once we know where the cursor position is in memory.
        for pad in pads:
            pad.tilt_stick(p3.pad.Stick.C, 0.5, 0.5)
    elif state.menu == p3.state.Menu.PostGame:
        for pad in pads:
            for m in mm:
                m.press_start_lots(state, pad)



def main():
    dolphin = p3.dolphin.Dolphin()
    dolphin_dir = find_dolphin_dir()
    if dolphin_dir is None:
        print('Could not find dolphin config dir.')
        return
    state = p3.state.State()
    sm = p3.state_manager.StateManager(state)
    write_locations(dolphin_dir, sm.locations())
    stats = p3.stats.Stats()
    try:
        print("dolphin-emu --exec=/home/20XX.iso")
#         if os.path.isdir("/Users/Robert/Documents/docker/smash"):
#             dolphin.run(iso_path="/Users/Robert/Documents/docker/smash/20XX.iso", render=False, debug=False)
#         else:
#             dolphin.run(iso_path="/home/20XX.iso", render=False, debug=False
        mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'
        path = os.path.dirname(os.path.realpath(__file__)) + "/stats.csv"
        
        with p3.memory_watcher.MemoryWatcher(mw_path) as mw, \
            p3.pad.Pad(dolphin.pads[0]) as pad1, \
            p3.pad.Pad(dolphin.pads[1]) as pad2, \
            p3.pad.Pad(dolphin.pads[2]) as pad3, \
            p3.pad.Pad(dolphin.pads[3]) as pad4, \
            open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Frame Number']+['Distinct States']+['Average Reward']+['SDs per 1000 States']+['Epsilon'])
            csvfile.close()
            fox = []
            for _ in range(0,4):
                fox.append(p3.fox.Fox())
                 
            run(fox=fox, state=state, sm=sm, mw=mw, pads=[pad1, pad2, pad3, pad4], stats=stats, locations={})
        
    except KeyboardInterrupt:
        print('Stopped')
        print(stats)

if __name__ == '__main__':
    main()
