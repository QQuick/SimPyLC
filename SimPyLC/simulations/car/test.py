import tty, sys

tty.setraw (sys.stdin.fileno ())

while 1:
    ch = sys.stdin.read (1)
    if ch == 'a':
        print ('Wohoo\r')
        
