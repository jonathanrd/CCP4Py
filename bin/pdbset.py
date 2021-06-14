#!/usr/bin/env python3

class pdbset:
    ''' PDBSET Wrapper '''

    def __init__(self, pdb, outputfilename = None, showcommand = False, atrenumber = False, custom = None, renumber = None, breset = False, occupancy = False):

        # Generate timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

        # Assign general inputs to class variables
        self.pdb = pdb
        self.atrenumber = atrenumber
        self.custom = custom
        self.showcommand = showcommand
        self.renumber = renumber
        self.breset = breset
        self.occupancy = occupancy

        # Output filename, use timestamp if not set
        if outputfilename:
            self.outputfilename = outputfilename
        else:
            self.outputfilename = timestamp + "-pdbset"


    def run(self):
        ''' Run it! '''
        import subprocess

        # Setup the command options
        cmd = ("pdbset "
        "xyzin "+self.pdb+" "
        "xyzout "+self.outputfilename+".pdb ")

        # Log output
        cmd += f"<< eof >>{self.outputfilename}.log\n"

        # Renumber a Chain?
        if (self.renumber):
            cmd+= f"renumber {self.renumber.split(',')[1]} chain {self.renumber.split(',')[0]}\n"

        # Renumber Atoms?
        if (self.atrenumber):
            cmd+= f"atrenumber\n"

        # Reset B Factors to value
        if (self.breset):
            cmd+= f"BFACTOR ALWAYS {self.breset}\n"

        # Reset all occupancy values to 1
        if (self.occupancy):
            cmd+= f"OCCUPANCY ALWAYS 1\n"

        # Any extra custom keywords?
        if self.custom:
            cmd+= str(self.custom) + "\n"

        # End the command entry
        cmd += "\neof"


        # Print the final command to terminal
        if self.showcommand == True:
            print(cmd)
            import sys
            sys.exit()

        # Start the log file
        import sys
        log = open(self.outputfilename + ".log", "w")
        log.write("PDBSET run through python wrapper using command:\n\n")
        log.write("pdbset.py " + (" ".join(sys.argv[1:])) + "\n\n")
        log.close()

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

        print(f"\n{underline}pdbset.py{clear} > {purple}{self.outputfilename}.log{clear}\n")

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

parser = argparse.ArgumentParser(prog = 'pdbset.py',
                                 usage = '%(prog)s [options]')

optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')

required.add_argument("--pdb", metavar = "input.pdb",
                    type = ascii,
                    required = True,
                    help = "PDB input file")

common = parser.add_argument_group('common arguments')

common.add_argument("--breset", metavar = "30",
                    help = "Reset all B Factors to a given value.",
                    type = float,
                    default = "30")

common.add_argument("--occupancy",
                    help = "Reset all occupancies to 1.",
                    action = "store_true")

common.add_argument("--renumber", metavar = "A,1",
                    help = "e.g. Renumber residues in a chain A starting from number 1.",
                    type = str)

common.add_argument("--atrenumber",
                    help = "Renumber all atoms.",
                    action = "store_true")

optional.add_argument("--output", metavar = "",
                    help = "Outfile filename [YYMMDD-HHMMSS-pdbset]",
                    type = str,
                    default = None)

optional.add_argument("--showcommand",
                    help = "Print the full pdbset command and stop.",
                    action = "store_true")

optional.add_argument("--custom",
                    help = "Pass custom keywords to pdbset.",
                    type = str, default = None)



parser._action_groups.append(optional)

# If running directly (not imported)
if __name__ == "__main__":

    # Get the command line arguments
    args = parser.parse_args()

    # Pass args to the main class
    program = pdbset(pdb = args.pdb, showcommand = args.showcommand,
    outputfilename = args.output,
    custom = args.custom, atrenumber = args.atrenumber, renumber = args.renumber, breset = args.breset, occupancy = args.occupancy)

    # Run the main class
    program.run()
