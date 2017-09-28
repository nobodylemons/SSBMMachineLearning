import os.path
import subprocess
import time
import _thread
import traceback

import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager
import p3.stats


def find_dolphin_dir():
    """Attempts to find the dolphin user directory. None on failure."""
    candidates = ['~/.dolphin-emu','~/Library/Application Support/Dolphin']
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
    mm = p3.menu_manager.MenuManager()
    while True:
        last_frame = state.frame
        res = next(mw)
        if res is not None:
            sm.handle(*res)
        if state.frame > last_frame:
            stats.add_frames(state.frame - last_frame)
            start = time.time()
            make_action(state, pads, mm, fox, locations)
            stats.add_thinking_time(time.time() - start)

def make_action(state, pads, mm, fox, locations):
    if state.menu == p3.state.Menu.Game:
        #locations = fox.advance(state, pads[0], 0, 1, locations)
        #locations = fox.advance(state, pads[1], 1, 0, locations)
        locations = fox[0].advance(state=state, pad=pads[0], player_num=2, opponent_num=3, locations=locations)
        locations = fox[1].advance(state=state, pad=pads[1], player_num=3, opponent_num=2, locations=locations)
        locations = fox[2].advance(state=state, pad=pads[2], player_num=1, opponent_num=0, locations=locations)
    elif state.menu == p3.state.Menu.Characters:
        mm.pick_falcon(state=state, pad=pads[0], player_num=2)
        mm.pick_falcon(state=state, pad=pads[1], player_num=3)
        mm.pick_falcon(state=state, pad=pads[2], player_num=0)
    elif state.menu == p3.state.Menu.Stages:
        # Handle this once we know where the cursor position is in memory.
        for pad in pads:
            pad.tilt_stick(p3.pad.Stick.C, 0.5, 0.5)
    elif state.menu == p3.state.Menu.PostGame:
        for pad in pads:
            mm.press_start_lots(state, pad)


def main():
    locations = {}
    run_threads(locations)
#     locations = {}
#     for _ in range(2):
#         try:
#             _thread.start_new_thread(run_threads, (locations,))
#         except:
#             print("Give up")
#     while 1:
#         pass


def run_threads(locations):
    dolphin_dir = find_dolphin_dir()
    if dolphin_dir is None:
        print('Could not find dolphin config dir.')
        return
    state = p3.state.State()
    sm = p3.state_manager.StateManager(state)
    write_locations(dolphin_dir, sm.locations())

    stats = p3.stats.Stats()

    fox = p3.fox.Fox()
    fox2 = p3.fox.Fox()
    fox3 = p3.fox.Fox()
#     os.system('/Applications/Dolphin.app/Contents/MacOS/Dolphin --exec=/Users/Robert/Documents/Dolphin\ Roms/melee/20XX.iso')
    try:
        subprocess.Popen(['/Applications/Dolphin.app/Contents/MacOS/Dolphin','--exec=/Users/Robert/Documents/Dolphin Roms/melee/20XX.iso'])
        mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'
#         pads.append(p3.pad.Pad(dolphin_dir + '/Pipes/p1'))
#         pads.append(p3.pad.Pad(dolphin_dir + '/Pipes/p2'))
#         pads.append(p3.pad.Pad(dolphin_dir + '/Pipes/p4'))
        with p3.pad.Pad(dolphin_dir + '/Pipes/p3') as pad3, p3.pad.Pad(dolphin_dir + '/Pipes/p4') as pad4, p3.pad.Pad(dolphin_dir + '/Pipes/p2') as pad1, p3.memory_watcher.MemoryWatcher(mw_path) as mw:
            run(fox=[fox, fox2, fox3], state=state, sm=sm, mw=mw, pads=[pad3, pad4, pad1], stats=stats, locations=locations)
        
    except KeyboardInterrupt:
        print('Stopped')
        print(stats)

if __name__ == '__main__':
    main()
