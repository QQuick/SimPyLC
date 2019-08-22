import argparse as ap
import distutils.dir_util as du
import os
import webbrowser as wb

simulationsSubdirName = 'simulations'
accessoriesSubdirName = 'accessories'
howtoFileName = 'simpylc_howto.html'

class CommandArgs :
    def __init__ (self):
        self.argParser = ap.ArgumentParser ()
        self.argParser.add_argument ('-a', '--acc', help = "Copy accessories to current directory", action = 'store_true')
        self.argParser.add_argument ('-d', '--doc', help = "Show documentation in default browser", action = 'store_true')
        self.argParser.add_argument ('-s', '--sim', help = "Copy example simulations to directory", action = 'store_true')
        self.__dict__.update (self.argParser.parse_args () .__dict__)
    
        
commandArgs = CommandArgs ()

simulatorDir = os.path.dirname (os.path.realpath (__file__))
currentDir = os.getcwd ()

def main ():
    if commandArgs.acc:
        du.copy_tree (simulatorDir + '/' + accessoriesSubdirName, currentDir + '/' + accessoriesSubdirName)
    elif commandArgs.sim:
        du.copy_tree (simulatorDir + '/' + simulationsSubdirName, currentDir + '/' + simulationsSubdirName)
    elif commandArgs.doc:
        wb.open (simulatorDir + '/' + howtoFileName)
    else:
        commandArgs.argParser.print_help ()
        
if __name__ == '__main__':
    main ()
    