#!/usr/bin/env python3

class ctruncate:
    ''' Pointless Wrapper '''

    def __init__(self,mtzin,mtzout, showcommand=False, log=None, verbose=False):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.verbose = verbose
        self.mtzin = mtzin
        self.mtzout = mtzout
        self.log = log

        if (self.mtzout == None): self.mtzout = f"{timestamp}-ctruncate.mtz"
        if (self.log == None): self.log = f"{timestamp}-ctruncate.log"



        if (self.verbose): print("Running cTruncate..")

        # Start the log file
        import sys
        log = open(self.log, "w")
        log.write("ctruncate run through python wrapper using command:\n\n")
        log.write("truncatewrap.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()
        if (self.verbose): print("Log file at: "+self.log)



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

        # Run the command
        s = subprocess.check_output(cmd, shell=True)
        self.result = s.decode('ascii')



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


parser.add_argument("--showcommand", help="Show AIMLESS command", action="store_true")

optional.add_argument("-v","--verbose", help="Verbose", action="store_true")

parser._action_groups.append(optional)


# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = ctruncate(mtzin=args.mtz, mtzout=args.mtzout, verbose=args.verbose, showcommand=args.showcommand, log=args.logout)

    # Run the main class
    program.run()
