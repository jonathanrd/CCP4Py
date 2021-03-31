#!/usr/bin/env python3

class ctruncate:
    ''' Pointless Wrapper '''

    def __init__(self,mtzin,mtzout, showcommand=False, log=None, logview=None):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.mtzin = mtzin
        self.mtzout = mtzout
        self.log = log
        self.logview = logview

        if (self.mtzout == None): self.mtzout = f"{timestamp}-ctruncate.mtz"
        if (self.log == None): self.log = f"{timestamp}-ctruncate.log"


    def run(self):
        ''' Run it! '''
        import subprocess

        # Setup the command options
        cmd = ("ctruncate "
        "-mtzin "+self.mtzin+" "
        "-mtzout "+self.mtzout+" "
        "-colin /*/*/[IMEAN,SIGIMEAN] "
        "-colano /*/*/[I\(+\),SIGI\(+\),I\(-\),SIGI\(-\)] ")

        cmd += (f"<< eof >>{self.log}\n")

        # End the command entry
        cmd += ("\n"
        "eof")



        # Print the final command to terminal
        if (self.showcommand == True): print(cmd)

        # Start the log file
        import sys
        log = open(self.log, "w")
        log.write("ctruncate run through python wrapper using command:\n\n")
        log.write("truncatewrap.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()

        # Show logview?
        if self.logview:
            subprocess.Popen(["logview", self.log],
            stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

        # Print to terminal
        bold      = "\033[1m"
        italic    = "\033[3m"
        underline = "\033[4m"
        blink     = "\033[5m"
        clear     = "\033[0m"
        green     = "\033[32m"
        yellow    = "\033[33m"
        red       = "\033[31m"
        purple    = "\033[35m"

        print(f"\n{underline}ctruncate.py{clear} > {purple}{self.log}{clear}\n")

        print(f"Running... ", end='', flush=True)

        # Run the command
        try:
            s = subprocess.check_output(cmd, shell = True, stderr = subprocess.DEVNULL)
            self.result = s.decode('ascii')
        except:
            print(f"{red}Error!{clear}\n")
            sys.exit()

        print(f"{green}Complete!{clear}\n")




import argparse

parser = argparse.ArgumentParser(prog='ctruncate.py', usage='%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')


required.add_argument("--mtz", metavar="input.mtz",
                    type=ascii,
                    required=True,
                    help="MTZ input file")

optional.add_argument("--mtzout", metavar="output.mtz",
                    type=ascii,
                    help="MTZ output file (Default: YYMMDD-HHMMSS-ctruncate.mtz)")

optional.add_argument("--logout", metavar="output.log",
                    type=ascii,
                    help="Log filename (Default: YYMMDD-HHMMSS-ctruncate.log)")

optional.add_argument("--logview",
                    help = "Run CCP4 logview while refmac is running.",
                    action = "store_true")

parser.add_argument("--showcommand", help="Show AIMLESS command", action="store_true")

parser._action_groups.append(optional)


# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = ctruncate(mtzin=args.mtz, mtzout=args.mtzout, showcommand=args.showcommand, log=args.logout, logview=args.logview)

    # Run the main class
    program.run()
