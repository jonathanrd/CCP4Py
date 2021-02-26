#!/usr/bin/env python3

class aimless:
    ''' Aimless Wrapper '''

    def __init__(self, mtzin, mtzout = None, reshigh = None, verbose = False, showcommand = False, log = None, unmerged = False, logview = None):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.reshigh = reshigh
        self.verbose = verbose
        self.mtzin = mtzin
        self.mtzout = mtzout
        self.log = log
        self.logview = logview

        if unmerged:
            self.unmerged = "UNMERGED"
        else:
            self.unmerged = ""

        # If custom mtz output not given, set as timestamp
        if (self.mtzout == None):
            self.mtzout = f"{timestamp}-aimless.mtz"

        # If custom log output not given, set as timestamp
        if (self.log == None):
            self.log = f"{timestamp}-aimless.log"




    def run(self):
        ''' Run it! '''
        import subprocess, sys

        # Setup the command options
        cmd = ("aimless "
        f"HKLIN {self.mtzin} "
        f"HKLOUT {self.mtzout} ")

        # log output
        cmd += f"<< eof >>{self.log}\n"

        # mtz output, merged (and unmerged)
        cmd += f"output mtz MERGED {self.unmerged}\n"

        # Set a high resolution limit
        if (self.reshigh):
            cmd += f"resolution high {self.reshigh}\n"

        # End the command entry
        cmd += "\neof"


        # Print the final command to terminal and stop
        if (self.showcommand == True):
            print(cmd)
            sys.exit()


        # Start the log file
        log = open(self.log, "w")
        log.write("Aimless run through python wrapper using command:\n\n")
        log.write("aimless.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()

        if (self.verbose):
            print("\nRunning Aimless..")
            print("Log file at: "+self.log)

        # Show logview?
        if self.logview:
            subprocess.Popen(["logview", self.log],
            stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

        # Run the command
        s = subprocess.check_output(cmd, shell=True)
        self.result = s.decode('ascii')

        # Output the final refinement stats to the terminal
        if (self.verbose):
            import re
            shakes = open(self.log, "r")
            for line in shakes:
                if re.match("           R factor    .+", line):
                    print ("       "+line.strip())


import argparse

parser = argparse.ArgumentParser(prog='aimless.py', usage='%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

required.add_argument("--mtz", metavar="input.mtz",
                    type=ascii,
                    required=True,
                    help="MTZ input file")

optional.add_argument("--mtzout", metavar="output.mtz",
                    type=ascii,
                    help="MTZ output file (Default: YYMMDD-HHMMSS-aimless.mtz)")

optional.add_argument("--logout", metavar="output.log",
                    type=ascii,
                    help="Log filename (Default: YYMMDD-HHMMSS-aimless.log)")

optional.add_argument("--reshigh",
                    help="High resolution limit",
                    type=float, default=None)

optional.add_argument("--nomerge",
                    help="Also save unmerged reflections",
                    action="store_true")

optional.add_argument("--showcommand", help="Show AIMLESS command", action="store_true")

optional.add_argument("--logview",
                    help = "Run CCP4 logview while pointless is running.",
                    action = "store_true")

optional.add_argument("-v","--verbose", help="Verbose", action="store_true")

parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = aimless(mtzin=args.mtz, mtzout=args.mtzout, verbose=args.verbose, showcommand=args.showcommand, reshigh=args.reshigh, log=args.logout, unmerged = args.nomerge, logview = args.logview)

    # Run the main class
    program.run()
