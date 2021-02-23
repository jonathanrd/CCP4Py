#!/usr/bin/env python3

class phaser:
    ''' Phaser Wrapper '''

    def __init__(self, mtzin, showcommand = False, log = None, verbose = False,
    output = None, identity = 50, pdbin = None, totalmw = None, nmol = 1,
    logview = None, custom = None):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.verbose = verbose
        self.mtzin = mtzin
        self.log = log
        self.output = output
        self.identity=identity
        self.pdbin=pdbin
        self.logview = logview
        self.nmol = nmol
        self.custom = custom

        # Is the molecular weight given by the user?
        if totalmw:
            self.totalmw = totalmw
        else: # No it's not given. Let's calculate it from the PDB.
            import subprocess,re
            s = subprocess.check_output("rwcontents XYZIN " + self.pdbin + "<<EOF\nEnd\nEOF", shell = True)
            for line in s.decode('ascii').split("\n"):
                if (re.match("^ Molecular Weight of protein:.*", line)):
                    self.totalmw = line.split(":")[1].strip()

        if (self.output == None):
            self.output = f"{timestamp}-phaser"

        if (self.log == None):
            self.log = f"{timestamp}-phaser.log"

        # Run mtzinfo to get list of column headers
        import subprocess, re
        s = subprocess.check_output("mtzinfo " + self.mtzin, shell = True)
        for line in s.decode('ascii').split("\n"):
            if re.match("^LABELS.*", line):
                self.labels = line.split()[1:]

        # Set the input MTZ labels
        self.label_fp = "FP=" + [i for i in self.labels if i in ['F', 'FP'] ][0]
        self.label_sigfp = "SIGFP=" + [i for i in self.labels if i in ['SIGF', 'SIGFP'] ][0]




    def run(self):
        ''' Run it! '''
        import subprocess, sys

        # Setup the command options
        cmd = ("phaser "
        f"<< eof >>{self.log}\n"
        f"TITLe MR\n"
        f"MODE MR_AUTO\n"
        f"HKLIn {self.mtzin}\n"
        f"LABIn {self.label_fp} {self.label_sigfp}\n"
        f"ENSEmble model PDB {self.pdbin} IDENtity {self.identity}\n"
        f"COMPosition PROTein MW {self.totalmw} NUM 1\n"
        f"SEARch ENSEmble model NUM {self.nmol}\n"
        f"ROOT {self.output}\n")

        # Any extra custom keywords?
        if self.custom:
            cmd+= str(self.custom) + "\n"

        # End the command entry
        cmd += ("\neof")


        # Print the final command to terminal
        if (self.showcommand == True):
            print(cmd)
            sys.exit()

        # Start the log file
        log = open(self.log, "w")
        log.write("phaser run through python wrapper using command:\n\n")
        log.write("phaserwrap.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()

        if self.verbose:
            print("Running phaser..")
            print("Log file at: "+self.log)
            print("PDB Total MW: "+self.totalmw)


        # Show logview?
        if self.logview:
            subprocess.Popen(["logview", self.log],
            stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

        # Run the command
        s = subprocess.check_output(cmd, shell = True)
        self.result = s.decode('ascii')

        # Output the final refinement stats to the terminal
        if self.verbose:
            import re
            shakes = open(self.log, "r")
            for line in shakes:
                if re.match("\*\* Solution written to PDB file:.*", line):
                    print (line.strip())
                if re.match("\*\* Solution written to MTZ file:.*", line):
                    print (line.strip())



import argparse

parser = argparse.ArgumentParser(prog='phaser.py', usage='%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

required.add_argument("--pdb", metavar="input.pdb",
                    required=True,
                    help="PDB input file")

required.add_argument("--mtz", metavar="input.mtz",
                    required=True,
                    help="MTZ input file")

optional.add_argument("--log", metavar = "",
                    help = "Log filename [YYMMDD-HHMMSS-phaser]")

optional.add_argument("--output", metavar = "",
                    help = "Output suffix [YYMMDD-HHMMSS-phaser]",
                    type = str, default = None)

optional.add_argument("--identity", metavar = "",
                    help = "Model identity [50.0]",
                    type = float, default = 50.0)

optional.add_argument("--totalmw", metavar = "",
                    help = "Composition MW [auto]",
                    type = int, default = None)

optional.add_argument("--nmol", metavar = "",
                    help = "No. of PDB copies in ASU [1]",
                    type = int, default = 1)

optional.add_argument("--logview",
                    help = "Run CCP4 logview while phaser is running.",
                    action = "store_true")

optional.add_argument("--custom",
                    help = "Pass custom keywords to phaser.",
                    type = str, default = None)

optional.add_argument("--showcommand",
                    help="Show phaser command",
                    action="store_true")

optional.add_argument("-v", "--verbose",
                    help = "Verbose",
                    action = "store_true")

parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = phaser(mtzin = args.mtz, verbose = args.verbose, showcommand = args.showcommand, log = args.log, output = args.output, identity = args.identity, pdbin = args.pdb, totalmw = args.totalmw, nmol = args.nmol, logview = args.logview, custom = args.custom)

    # Run the main class
    program.run()
