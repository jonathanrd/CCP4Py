#!/usr/bin/env python3

class pointless:
    ''' Pointless Wrapper '''

    def __init__(self,mtzin,mtzout=None,spacegroup=None, verbose=False, showcommand=False, log=None, custom = None):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.spacegroup = spacegroup
        self.verbose = verbose
        self.mtzin = mtzin
        self.mtzout = mtzout
        self.log = log
        self.custom = custom

        if (self.mtzout == None): self.mtzout = f"{timestamp}-pointless.mtz"
        if (self.log == None):    self.log = f"{timestamp}-pointless.log"


        if (self.verbose): print("Running Pointess..")

        # Start the log file
        import sys
        log = open(self.log, "w")
        log.write("Pointless run through python wrapper using command:\n\n")
        log.write("pointlesswrap.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()
        if (self.verbose): print("Log file at: "+self.log)



    def run(self):
        ''' Run it! '''
        import subprocess

        # Setup the command options
        cmd = ("pointless "
        "HKLIN "+self.mtzin+" "
        "HKLOUT "+self.mtzout+" ")

        cmd += (f"<< eof >>{self.log}\n")

        # Set a high resolution limit
        if (self.spacegroup):
            cmd += f"spacegroup {self.spacegroup}\n"

        # Any extra custom keywords?
        if self.custom:
            cmd+= str(self.custom) + "\n"

        # End the command entry
        cmd += ("\n"
        "eof")



        # Print the final command to terminal
        if (self.showcommand == True): print(cmd)

        # Run the command
        s = subprocess.check_output(cmd, shell=True)
        self.result = s.decode('ascii')

        # Output the info to the terminal
        if (self.verbose):
            import re
            shakes = open(self.log, "r")
            for line in shakes:
                if re.match(".*Space group =.+", line):
                    print (" "+line.strip())



import argparse

parser = argparse.ArgumentParser(prog='pointless.py', usage='%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

required.add_argument("--mtz", metavar="input.mtz",
                    type=ascii,
                    required=True,
                    help="MTZ input file")

optional.add_argument("--mtzout", metavar="output.mtz",
                    type=ascii,
                    help="MTZ output file (Default: YYMMDD-HHMMSS-pointless.mtz)")

optional.add_argument("--logout", metavar="output.log",
                    type=ascii,
                    help="Log filename (Default: YYMMDD-HHMMSS-pointless.log)")

optional.add_argument("--spacegroup", metavar="P1",
                    help="Input a known spacegroup",
                    type=str, default=None)

optional.add_argument("--showcommand", help="Show AIMLESS command", action="store_true")

optional.add_argument("--custom",
                    help = "Pass custom keywords to pointless.",
                    type = str, default = None)


optional.add_argument("-v","--verbose", help="Verbose", action="store_true")

parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = pointless(mtzin=args.mtz, mtzout=args.mtzout, verbose=args.verbose, showcommand=args.showcommand, spacegroup=args.spacegroup, log=args.logout, custom=args.custom)

    # Run the main class
    program.run()
