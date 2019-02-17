import os
import curses

from pyWorldMap import *

LOG = []

def addLog(str):
    global LOG
    LOG.append(str)

def printLog(win):
    global LOG
    start = 30
    count = 0;

    for logRow in LOG:
        win.addstr(start+count, 0, logRow)
        count += 1

def setupColour(win):
    """
        Sets colors to be used in curses
    """
    # Uses default terminal colours
    curses.use_default_colors()
    curses.init_pair(0, 0, -1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    

def print_map(win, mapString):
    # print the ,ap dimensions
    cols, rows = len(mapString.split('\n')[0]), len(mapString.split('\n'))
    count = 0
    for row in mapString.split('\n'):
        win.addstr(count, 0, row)
        count += 1


def print_point(win, lat, lon, char, label=""):
    # get the x, y point 
    x, y = lat_lon_to_X_Y(lat, lon)
    win.addstr(y+1, x+1, char, curses.color_pair(1))
    addLog("{}) {} ({:.1f}, {:.1f}) -> ({:.1f}, {:.1f})".format(char, label, lat, lon, x, y))


def print_test_coords(win, mapString):
    coords = [
        # Lat        Lon       Name
        [51.369208,  0.106923, "London"],
        [39.768173, -434.715499, "New York"],
        [-18.259349, -313.850023, "Madagascar"],
        [-34.520136, -222.565312, "Melbourne"],
        [48.208176, 16.373819, "Vienna"],
        [-43.532055, 172.636230, "CHCH"],
        [35.689487, 139.691711, "Tokyo"],
        [33.929047, -118.441495, "LA"],
        [49.240186, -123.110419, "Vancouver"]
    ]

    win.clear() 
    print_map(win, mapString)

    count = 1
    for coord in coords:
        print_point(win, coord[0], coord[1], str(count), coord[2])
        count += 1


def main(win):
    """
        The main function. sets up the curses menu, variables and holds the main loop for key catches. Also handles most of the updating of state and text input etc.
    """
    curses.curs_set(0)
    setupColour(win)
    win.nodelay(True)

    win.clear() 
    worldMap = get_map_string_with_border()

    print_map(win, worldMap)
    print_test_coords(win, worldMap)
    printLog(win)

    key = ""
    while 1:  
        try:
            key = win.getkey() 

            # Quit
            if key == 'q':
                return

            # Clear the window is always needed
            win.clear() 
            print_map(win, worldMap)
            print_test_coords(win, worldMap)
            printLog(win)


        except Exception as e:
            # No input   
            if str(e) != 'no input':
                win.addstr(35, 0, ' ' * 100)
                win.addstr(35, 0, "ERROR: {0}".format(e))
            pass  

        

# so the excape key doesnt have a noticable delay
os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)