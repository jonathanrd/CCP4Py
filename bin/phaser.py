#!/usr/bin/env python3

class phaser:
    ''' Pointless Wrapper '''

    def __init__(self,mtzin,showcommand=False, log=None, verbose=False, output=None, identity=50,pdbin=None,totalmw=None, nmol=1):

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

        # Is the molecular weight given by the user?
        if(totalmw):
            self.totalmw=totalmw
        else: # No it's not given. Let's calculate it from the PDB.
            import subprocess,re
            s = subprocess.check_output("rwcontents XYZIN "+self.pdbin+"<<EOF\nEnd\nEOF", shell=True)
            for line in s.decode('ascii').split("\n"):
                if (re.match("^ Molecular Weight of protein:.*", line)):
                    self.totalmw = line.split(":")[1].strip()

        self.nmol=nmol

        if (self.output == None): self.output = f"{timestamp}-phaser"
        if (self.log == None): self.log = f"{timestamp}-phaser.log"

        # Start the log file
        import sys
        log = open(self.log, "w")
        log.write("phaser run through python wrapper using command:\n\n")
        log.write("phaserwrap.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()

        if (self.verbose):
            print("Running phaser..")
            print("Log file at: "+self.log)
            print("PDB Total MW: "+self.totalmw)



    def run(self):
        ''' Run it! '''
        import subprocess

        # Setup the command options
        cmd = ("phaser "
        f"<< eof >>{self.log}\n"
        f"TITLe MR\n"
        f"MODE MR_AUTO\n"
        f"HKLIn {self.mtzin}\n"
        f"LABIn F=F SIGF=SIGF\n"
        f"ENSEmble model PDB {self.pdbin} IDENtity {self.identity}\n"
        f"COMPosition PROTein MW {self.totalmw} NUM 1\n"
        f"SEARch ENSEmble model NUM {self.nmol}\n"
        f"ROOT {self.output}\n")

        # End the command entry
        cmd += ("\n"
        "eof")



        # Print the final command to terminal
        if (self.showcommand == True): print(cmd)

        # Run the command
        s = subprocess.check_output(cmd, shell=True)
        self.result = s.decode('ascii')

        # Output the final refinement stats to the terminal
        if (self.verbose):
            import re
            shakes = open(self.log, "r")
            for line in shakes:
                if re.match("** Solution written to PDB file:.+", line):
                    print ("       "+line.strip())
                if re.match("** Solution written to MTZ file:.+", line):
                    print ("         "+line.strip())
                if re.match("     Rms BondLength    .+", line):
                    print (" "+line.strip())
                if re.match("      Rms BondAngle    .+", line):
                    print ("  "+line.strip())



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

optional.add_argument("--log", help="Log filename")
optional.add_argument("--output",
                    help="Output suffix",
                    type=str, default="phaser")
optional.add_argument("--identity",
                    help="Model identity",
                    type=float, default=50.0)
optional.add_argument("--totalmw",
                    help="Composition MW",
                    type=int, default=None)
optional.add_argument("--nmol",
                    help="No. of mol in asu (Default: 1)",
                    type=int, default=1)

optional.add_argument("--showcommand", help="Show phaser command", action="store_true")

optional.add_argument("-v","--verbose", help="Verbose", action="store_true")

parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = phaser(mtzin=args.mtz,verbose=args.verbose, showcommand=args.showcommand, log=args.log,output=args.output, identity=args.identity,pdbin=args.pdb,totalmw=args.totalmw, nmol=args.nmol)

    # Run the main class
    program.run()
