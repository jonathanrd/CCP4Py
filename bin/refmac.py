#!/usr/bin/env python3

class refmac:
    ''' Refmac5 Wrapper '''

    def __init__(self,pdb, mtz, mode = "HKRF", cycles = 10,bref = "ISOT",weight = None, showcommand=False, outputfilename = "timestamp", coot=False, breset=None, verbose=False, custom=None, libin=None, tlsin=None):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.mode = mode
        self.cycles = cycles
        self.bref = bref
        self.weight = weight
        self.pdb = pdb
        self.mtz = mtz
        self.coot = coot
        self.breset = breset
        self.verbose = verbose
        self.custom = custom
        self.libin = libin
        self.tlsin = tlsin

        # Setup the output file names, use timestamp if not set
        self.outputfilename = outputfilename
        if (self.outputfilename == "timestamp"): self.outputfilename = timestamp+"-refmac"

        if (self.verbose): print("Running Refmac..")

        # Start the log file
        import sys
        log = open(self.outputfilename+".log", "w")
        log.write("Refmac run through python wrapper using command:\n\n")
        log.write("refmacwrapper.py "+(" ".join(sys.argv[1:]))+"\n\n")
        log.close()
        if (self.verbose): print("Log file at: "+self.outputfilename+".log")



    def run(self):
        ''' Run it! '''
        import subprocess

        # Setup the command options
        cmd = ("refmac5 "
        "XYZIN "+self.pdb+" "
        "HKLIN "+self.mtz+" "
        "XYZOUT "+self.outputfilename+".pdb "
        "HKLOUT "+self.outputfilename+".mtz ")

        # Are there TLS definitions?
        if (self.tlsin): cmd+= f"TLSIN {self.tlsin} "

        # Is there an extra dictionary?
        if (self.libin): cmd+= f"LIBIN {self.libin} "

        cmd += (f"<< eof >>{self.outputfilename}.log\n"
        f"ncyc {self.cycles}\n"
        "labin  FP=F SIGFP=SIGF FREE=FreeR_flag\n")

        # Have the B factors been reset?
        if (self.breset != None): cmd+= "BFACTOR SET " + str(self.breset) +"\n"

        # Type of B Factor refinement to run
        if (self.bref != "ISOT"): cmd+= "REFI BREF " + str(self.bref) +"\n"

        # Mode of refinement
        if (self.mode != "HKRF"): cmd+= "MODE " + str(self.mode) +"\n"

        # Adjust the restraints weight
        if (self.weight): cmd+= "WEIGHT MATRIX " + str(self.weight) +"\n"

        # Any extra custom keywords?
        if (self.custom): cmd+= str(self.custom) +"\n"


        # End the command entry
        cmd += ("NOHARVEST\n"
        "END\n"
        "eof")



        # Print the final command to terminal
        if (self.showcommand == True): print(cmd)

        # Run the command
        s = subprocess.check_output(cmd, shell=True)
        self.result = s.decode('ascii')

        # Output the final refinement stats to the terminal
        if (self.verbose):
            import re
            shakes = open(self.outputfilename+".log", "r")
            for line in shakes:
                if re.match("           R factor    .+", line):
                    print ("       "+line.strip())
                if re.match("             R free    .+", line):
                    print ("         "+line.strip())
                if re.match("     Rms BondLength    .+", line):
                    print (" "+line.strip())
                if re.match("      Rms BondAngle    .+", line):
                    print ("  "+line.strip())

            print("coot --pdb "+self.outputfilename+".pdb --auto "+self.outputfilename+".mtz")

        # Open the output files in Coot
        if (self.coot == True):
            import subprocess
            subprocess.check_output("coot --pdb "+self.outputfilename+".pdb --auto "+self.outputfilename+".mtz &>/dev/null", shell=True)



import argparse

parser = argparse.ArgumentParser(prog='refmac.py', usage='%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

required.add_argument("--pdb", metavar="input.pdb",
                    type=ascii,
                    required=True,
                    help="PDB input file")

required.add_argument("--mtz", metavar="input.mtz",
                    type=ascii,
                    required=True,
                    help="MTZ input file")


optional.add_argument("--cycles", metavar="10",
                    help="No. of cycles (Default: 10)",
                    type=int, default=10)

optional.add_argument("--breset", metavar="30",
                    help="Reset B Factor at start to value",
                    type=int, default=None)

optional.add_argument("--bref",  metavar="ISOT",
                    help="B refinement (Default: ISOT. Options: OVER, ISOT, ANIS, MIXED)",
                    type=str,
                    choices=['OVER', 'ISOT', 'ANIS', 'MIXED'],
                    default = 'ISOT')

optional.add_argument("--mode", metavar="HKRF",
                    help="Refinement Mode (Default: HKRF. Options: HKRF, RIGID, TLSR)",
                    type=str,
                    default="HKRF",
                    choices = ['HKRF', 'RIGID', 'TLSR'])

optional.add_argument("--weight", metavar="0.5",
                    help="Weight matrix (Default: Auto)",
                    type=float,
                    default = None) # Leave None for auto

optional.add_argument("--output", metavar="name",
                    help="Outfile file name (Default: YYMMDD-HHMMSS-refmac)",
                    type=str,
                    default = "timestamp")

optional.add_argument("--showcommand",
                    help="Print the full refmac command",
                    action="store_true")

optional.add_argument("--coot",
                    help="Run Coot after refinement",
                    action="store_true")

optional.add_argument("--custom",
                    help="Pass custom keywords to refmac",
                    type=str, default = None)

optional.add_argument("--libin",
                    help="Add a dictionary",
                    type=str, default = None)

optional.add_argument("--tlsin",
                    help="TLS definitions",
                    type=str, default = None)

optional.add_argument("-v","--verbose", help="Verbose", action="store_true")

parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = refmac(pdb = args.pdb, cycles = args.cycles, mtz = args.mtz, bref=args.bref, weight=args.weight, showcommand=args.showcommand, mode=args.mode, outputfilename=args.output, coot=args.coot, breset=args.breset, verbose=args.verbose, libin=args.libin, tlsin=args.tlsin)

    # Run the main class
    program.run()