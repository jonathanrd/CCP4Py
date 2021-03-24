#!/usr/bin/env python3

class refmac:
    ''' Refmac5 Wrapper '''

    def __init__(self, pdb, mtz, mode = "HKRF", cycles = 10, tlscycles = None,
    bref = "ISOT", weight = None, showcommand = False, outputfilename = None,
    coot = False, breset = None, custom = None, libin = None,
    tlsin = None, labeltype = "normal", logview = None, ncs = "none"):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.showcommand = showcommand
        self.mode = mode
        self.cycles = cycles
        self.tlscycles = tlscycles
        self.bref = bref
        self.weight = weight
        self.pdb = pdb
        self.mtz = mtz
        self.coot = coot
        self.breset = breset
        self.custom = custom
        self.libin = libin
        self.tlsin = tlsin
        self.labeltype = labeltype
        self.logview = logview
        self.ncs = ncs

        # Output filename, use timestamp if not set
        if outputfilename:
            self.outputfilename = outputfilename
        else:
            self.outputfilename = timestamp + "-refmac"


        # Run mtzinfo to get list of column headers
        import subprocess,re,sys
        try:
            s = subprocess.check_output("mtzinfo " + self.mtz, shell = True,
            stderr = subprocess.DEVNULL)
        except:
            print("Error: Can't read MTZ file")
            sys.exit()

        for line in s.decode('ascii').split("\n"):
            if re.match("^LABELS.*", line):
                self.labels = line.split()[1:]

        # Using common free r labels, find and set the Free R label
        default_free = ['FREE', 'RFREE', 'FREER', 'FreeR_flag', 'R-free-flags']
        try:
            self.label_free = "FREE=" + [i for i in self.labels if i in default_free][0]
        except:
            return

        # Using common label names, find and set the correct label
        # F-/SIGF-obs-filtered - Phenix
        if (self.labeltype == "normal" or self.labeltype == "hl"):
            try:
                self.label_fp = "FP="+[i for i in self.labels if i in ['F', 'FP', 'F-obs-filtered', 'FOBS'] ][0]
                self.label_sigfp = "SIGFP="+[i for i in self.labels if i in ['SIGF', 'SIGFP', 'SIGF-obs-filtered', 'SIGFOBS'] ][0]
            except:
                print("Error: Could not identify F and/or SIGF columns in MTZ.")
                sys.exit()

        if (self.labeltype == "sad"):
            try:
                self.label_fplus = "F+="+[ i for i in self.labels if i in ['F+', 'F(+)'] ][0]
                self.label_sigfplus = "SIGF+="+[ i for i in self.labels if i in ['SIGF+', 'SIGF(+)'] ][0]
                self.label_fminus = "F-="+[ i for i in self.labels if i in ['F-', 'F(-)'] ][0]
                self.label_sigfminus = "SIGF-="+[ i for i in self.labels if i in ['SIGF-', 'SIGF(-)'] ][0]
            except:
                print("Error: Could not identify F+/F- and/or SIGF+/SIGF+ columns in MTZ.")
                sys.exit()

        if (self.labeltype == "hl"):
            try:
                self.label_hla = "HLA="+[ i for i in self.labels if i in ['HLA'] ][0]
                self.label_hlb = "HLB="+[ i for i in self.labels if i in ['HLB'] ][0]
                self.label_hlc = "HLC="+[ i for i in self.labels if i in ['HLC'] ][0]
                self.label_hld = "HLD="+[ i for i in self.labels if i in ['HLD'] ][0]
            except:
                print("Error: Could not identify HLA/HLB/HLC/HLD columns in MTZ.")
                sys.exit()

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

        # Log output
        cmd += f"<< eof >>{self.outputfilename}.log\n"

        # Number of cycles
        cmd += f"ncyc {self.cycles}\n"

        # Number of TLS cycles
        if self.tlscycles:
            cmd += f"REFI TLSC {self.tlscycles}"

        # Set the input labels
        if self.labeltype == "normal":
            cmd += f"labin  {self.label_fp} {self.label_sigfp} {self.label_free}\n"

        elif self.labeltype == "sad":
            cmd += f"labin  {self.label_fplus} {self.label_sigfplus} {self.label_fminus} {self.label_sigfminus} {self.label_free}\n"

        elif self.labeltype == "hl":
            cmd += f"labin  {self.label_fp} {self.label_sigfp} {self.label_hla} {self.label_hlb} {self.label_hlc} {self.label_hld} {self.label_free}\n"

        # Have the B factors been reset?
        if self.breset != None:
            cmd+= "BFACTOR SET " + str(self.breset) + "\n"

        # Type of B Factor refinement to run
        if self.bref != "ISOT":
            cmd+= "REFI BREF " + str(self.bref) + "\n"

        # Mode of refinement
        if self.mode != "HKRF":
            cmd+= "MODE " + str(self.mode) + "\n"

        # Adjust the restraints weight
        if self.weight:
            cmd+= "WEIGHT MATRIX " + str(self.weight) + "\n"

        # Automatic NCS
        if self.ncs == "global":
            cmd+= "ncsr global\n"
        if self.ncs == "local":
            cmd+= "ncsr local\n"

        # Any extra custom keywords?
        if self.custom:
            cmd+= str(self.custom) + "\n"


        # End the command entry
        cmd += "NOHARVEST\nEND\neof"



        # Print the final command to terminal
        if self.showcommand == True:
            print(cmd)
            import sys
            sys.exit()

        # Start the log file
        import sys
        log = open(self.outputfilename + ".log", "w")
        log.write("Refmac run through python wrapper using command:\n\n")
        log.write("refmac.py " + (" ".join(sys.argv[1:])) + "\n\n")
        log.close()

        # Show logview?
        if self.logview:
            subprocess.Popen(["logview", self.outputfilename + ".log"],
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

        print(f"\n{underline}refmac.py{clear} > {purple}{self.outputfilename}.log{clear}\n")

        if self.label_free == "":
            print(f"{red}Warning:{clear} No free set found.\n")

        print(f"Running... ", end='', flush=True)

        # Run the command
        try:
            s = subprocess.check_output(cmd, shell = True, stderr = subprocess.DEVNULL)
            self.result = s.decode('ascii')
        except:
            print(f"{red}Error!{clear}\n")
            sys.exit()


        print(f"{green}Complete!{clear}\n")

        # Output the final refinement stats to the terminal
        import re

        # Read the log file
        openlog = open(self.outputfilename + ".log", "r")
        logtext = openlog.read()
        openlog.close()

        try:
            # Regex to extract the important refinement values
            rfactor = list(re.findall(r"^\s*R factor\s*([0-9.]+)\s+([0-9.]+)\s*$", logtext, re.MULTILINE)[0])
            rfree = list(re.findall(r"^\s*R free\s*([0-9.]+)\s+([0-9.]+)\s*$", logtext, re.MULTILINE)[0])
            bond_len = list(re.findall(r"^\s*Rms BondLength\s*([0-9.]+)\s+([0-9.]+)\s*$", logtext, re.MULTILINE)[0])
            bond_ang = list(re.findall(r"^\s*Rms BondAngle\s*([0-9.]+)\s+([0-9.]+)\s*$", logtext, re.MULTILINE)[0])

            if rfactor[0] > rfactor[1]:
                rfactor_colour = green
            else:
                rfactor_colour = ""

            if rfree[0] > rfree[1]:
                rfree_colour = green
            else:
                rfree_colour = ""

            # Print a table
            print (f"  {bold}Rwork/Rfree{clear} {rfactor[0]}/{rfree[0]} -> {rfactor_colour}{rfactor[1]}{clear}/{rfree_colour}{rfree[1]}{clear}")
            print (f"{bold}Bond RMSD Å/°{clear} {bond_len[0]}/{bond_ang[0]} -> {bond_len[1]}/{bond_ang[1]}")
        except:
            print ("Error: Could not parse log file.")

        print("\ncoot --pdb", self.outputfilename + ".pdb --auto",
        self.outputfilename+".mtz\n")

        # Open the output files in Coot
        if self.coot:
            import subprocess
            subprocess.check_output("coot --pdb " + self.outputfilename+".pdb --auto " + self.outputfilename+".mtz &>/dev/null", shell=True)



import argparse

parser = argparse.ArgumentParser(prog = 'refmac.py',
                                 usage = '%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

required.add_argument("--pdb", metavar = "input.pdb",
                    type = ascii,
                    required = True,
                    help = "PDB input file")

required.add_argument("--mtz", metavar = "input.mtz",
                    type = ascii,
                    required = True,
                    help = "MTZ input file")

common = parser.add_argument_group('common arguments')

common.add_argument("--cycles", metavar = "10",
                    help = "No. of cycles [10]",
                    type = int, default=10)

common.add_argument("--bref",  metavar = "ISOT",
                    help = "B refinement (OVER, [ISOT], ANIS, MIXED)",
                    type = str,
                    choices = ['OVER', 'ISOT', 'ANIS', 'MIXED'],
                    default = 'ISOT')

common.add_argument("--ncs",  metavar = "none",
                    help = "Auto NCS ([none], local, global)",
                    type = str,
                    choices = ['none', 'local', 'global'],
                    default = 'none')

common.add_argument("--libin",
                    help = "Add a dictionary.",
                    type = str, default = None)

common.add_argument("--logview",
                    help = "Run CCP4 logview while refmac is running.",
                    action = "store_true")

common.add_argument("--coot",
                    help = "Run Coot after refinement.",
                    action = "store_true")

optional.add_argument("--mode", metavar = "HKRF",
                    help = "Refinement Mode ([HKRF], RIGID, TLSR)",
                    type = str,
                    default = "HKRF",
                    choices = ['HKRF', 'RIGID', 'TLSR'])

optional.add_argument("--breset", metavar = "30",
                    help = "Reset B Factor at start to specified value",
                    type = int, default = None)

optional.add_argument("--labels", metavar = "normal",
                    help = "Refine with SAD or exp. data ([normal], sad, hl)",
                    type = str,
                    default = "normal",
                    choices = ['normal', 'sad', 'hl'])

optional.add_argument("--weight", metavar="0.5",
                    help = "Weight matrix [auto]",
                    type = float,
                    default = None) # Leave None for auto

optional.add_argument("--output", metavar = "",
                    help = "Outfile file name [YYMMDD-HHMMSS-refmac]",
                    type = str,
                    default = None)

optional.add_argument("--showcommand",
                    help = "Print the full refmac command and stop.",
                    action = "store_true")

optional.add_argument("--custom",
                    help = "Pass custom keywords to refmac.",
                    type = str, default = None)

optional.add_argument("--tlsin",
                    help = "TLS definitions.",
                    type = str, default = None)

optional.add_argument("--tlscycles",
                    help = "Number of TLS cycles.", metavar = "0",
                    type = int, default=None)


parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = refmac(pdb = args.pdb, cycles = args.cycles, tlscycles = args.tlscycles, mtz = args.mtz,
    bref = args.bref, weight = args.weight, showcommand = args.showcommand,
    mode = args.mode, outputfilename = args.output, coot = args.coot,
    breset = args.breset, libin = args.libin,
    tlsin = args.tlsin, labeltype = args.labels, logview = args.logview,
    custom = args.custom, ncs = args.ncs)

    # Run the main class
    program.run()
