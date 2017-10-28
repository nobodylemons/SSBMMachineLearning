import time
import csv
import os
import p3.fox
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager
import p3.stats
import p3.dolphin
import pickle
from . import memory_watcher
from .pad import *


def find_dolphin_dir():
    """Attempts to find the dolphin user directory. None on failure."""
    candidates = ['~/.dolphin-emu','~/Library/Application Support/Dolphin','/tmp','/usr/local/share/dolphin-emu/sys']
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

def run(fox, state, sm, mw, pads, stats, sarsa, alpha, highstates, sd):
    mm = []
    for _ in range(4):
        """Menu manager is the object used to select characters and set dual 1v1 fighting mode"""
        mm.append(p3.menu_manager.MenuManager())
    try:
        tree_path = os.path.dirname(os.path.realpath(__file__)) + "/tree"
        locations = p3.location_structure.LocationStruct()
        while True:
            last_frame = state.frame
            messages = mw.get_messages()
            for message in messages:
                sm.handle(*message)
                
            #Every 1000 frames, check for pause directory
            if state.frame % 1000 == 0:
                is_write = os.path.isdir(os.path.dirname(os.path.realpath(__file__))+"/write")
                if state.frame % 1000000 == 0 or is_write:
                    print(tree_path, locations.size)
                    pickle.dump(locations, open(tree_path, 'wb'), pickle.HIGHEST_PROTOCOL)
                    if is_write:
                        os.rmdir(os.path.dirname(os.path.realpath(__file__))+"/write")
                    
            if state.frame > last_frame:
                stats.add_frames(state.frame - last_frame)
                start = time.time()
                locations = make_action(state, pads, mm, fox, locations, sarsa, alpha, highstates, sd)
                stats.add_thinking_time(time.time() - start)
            mw.advance()
                
                
                
    except KeyboardInterrupt:
        print('Stopped')
        print(stats)
#         pads[0].frame_advance_release()

def make_action(state, pads, mm, fox, locations, sarsa, alpha, highstates, sd):
    if state.menu == p3.state.Menu.Game:
#         locations = fox[0].advance(state=state, pad=pads[0], player_num=0, opponent_num=1, locations=locations)
        locations = fox[1].advance(state=state, pad=pads[1], player_num=1, opponent_num=0, locations=locations, sarsa=sarsa, alpha=alpha, highstates=highstates, sd=sd)
#         locations = fox[2].advance(state=state, pad=pads[2], player_num=2, opponent_num=3, locations=locations)
        locations = fox[3].advance(state=state, pad=pads[3], player_num=3, opponent_num=2, locations=locations, sarsa=sarsa, alpha=alpha, highstates=highstates, sd=sd)
        divideby = 10000
        if state.frame % divideby == 0:
            average_reward = []
            for _ in range(4):
                average_reward.append(0)
            distinct_states = 0
            sds = 0
            epsilon = 0
            i = 0
            for singlefox in fox:
                average_reward[i] = average_reward[i] + (singlefox.reward)
                distinct_states = singlefox.locations.size
                sds = sds + singlefox.total_sds
                epsilon = singlefox.count
                singlefox.reward = 0
                singlefox.total_sds = 0
                i = i + 1
            path = os.path.dirname(os.path.realpath(__file__)) + "/stats.csv"
            with open(path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([state.frame]+[distinct_states]+[average_reward[0]/divideby]+[average_reward[1]/divideby]+[average_reward[2]/divideby]+[average_reward[3]/divideby]+[sds]+[epsilon])
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
                if mm[2].changed_cpu == False:
                    mm[2].change_cpu(state, pads[2], 2)
                if mm[1].changed_cpu == False:
                    mm[1].change_cpu(state, pads[1], 1)
                if mm[0].changed_color and mm[1].changed_color and mm[2].changed_cpu and mm[0].pressed_start == False:
                        pads[0].press_button(p3.pad.Button.START)
                        mm[0].pressed_start = True
                elif mm[0].pressed_start:
                    for pad in pads:
                        pad.reset()
#                 elif mm[0].changed_color and mm[1].changed_color and mm[0].pressed_start:
#                     mm[0].global_menu_state = mm[0].global_menu_state + 1
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
    return locations


def main(sarsa=False, alpha = .01, highstates = False, sd = False):
    dolphin = p3.dolphin.Dolphin()
    dolphin_dir = find_dolphin_dir()
    if dolphin_dir is None:
        print('Could not find dolphin config dir.')
        return
    state = p3.state.State()
    sm = p3.state_manager.StateManager(state)
    write_locations(dolphin_dir, sm.locations())
    stats = p3.stats.Stats()

    if os.path.isdir("/Users/Robert/Documents/docker/smash"):
        dolphin.run(iso_path="/Users/Robert/Documents/docker/smash/20XX.iso", render=False, debug=False)
    else:
        dolphin.run(iso_path="/home/root/20XX.iso", user=True)
    mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'
    stats_path = os.path.dirname(os.path.realpath(__file__)) + "/stats.csv"
    mwType = memory_watcher.MemoryWatcherZMQ
    mw = mwType(path=mw_path)
    
    
    with p3.pad.Pad(dolphin.pads[0]) as pad1, \
        p3.pad.Pad(dolphin.pads[1]) as pad2, \
        p3.pad.Pad(dolphin.pads[2]) as pad3, \
        p3.pad.Pad(dolphin.pads[3]) as pad4, \
        open(stats_path, 'w', newline='') as csvfile:
#         pads = get_pads()
        pads = [pad1, pad2, pad3, pad4]
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Frame Number']+['Distinct States']+['Reward 1']+['Reward 2']+['Reward 3']+['Reward 4']+['SDs per 10000 States']+['Epsilon'])
        csvfile.close()
        fox = []
        for _ in range(4):
            fox.append(p3.fox.Fox())
        
        run(fox=fox, state=state, sm=sm, mw=mw, pads=pads, stats=stats, sarsa=sarsa, alpha=alpha, highstates=highstates, sd=sd)

def mergeTwo(tree1, tree2):
    if not tree1:
        return tree2
    if not tree2:
        return tree1
    all_locations_tree1 = tree1.all_locations
    for location1 in all_locations_tree1:
        if tree2.__contains__(location1):
            tree2obj = tree2.get(location1)
            tree1obj = tree2.get(location1)
            for i in range(tree1obj.q_arr.__len__()):
                tree1weight = tree1obj.weight_arr[i]
                tree2weight = tree2obj.weight_arr[i]
                weightTotal = tree1weight + tree2weight
                finalq = 0
                if weightTotal is not 0:
                    finalq = (tree1obj.q_arr[i]*tree1weight + tree2obj.q_arr[i]*tree2weight)/weightTotal
                tree2obj.q_arr[i]=finalq
                tree2obj.weight_arr[i]=weightTotal
        else:
            tree2.add(location1,tree1.get(location1))
    return tree2

if __name__ == '__main__':
#     main.main()
#     main.main(sarsa=True)
#     main.main(alpha=.0001)
#     main.main(alpha=.1)
    main.main(highstates=True)
#     main.main(sd=True)
