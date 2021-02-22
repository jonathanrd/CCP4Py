<center><img src="CCP4Py.png" alt="CCP4Py Logo" width="800"/></center>

Unofficial python wrappers for CCP4 programs. Designed to make the task of running CCP4 programs from the command line as simple as possible. Not designed to cover every option or use case!

Currently supports: **pointless**, **aimless**, **ctruncate**, **phaser**, and **refmac**.

# Installation
Requires [CCP4](http://www.ccp4.ac.uk/download/)
```
# Clone this repo to your user folder
cd ~/
git clone https://github.com/jonathanrd/CCP4Py.git
```

Add the following to your .bashrc (Linux) or .bash_profile (Mac)
```
export PATH=/Users/YourUserFolder/CCP4Py/bin:$PATH
```

# Basic Usage

```
# Check spacegroup and sort
pointless.py --mtz integrated.mtz --mtzout sorted.mtz

# Scale
aimless.py --mtz sorted.mtz --mtzout scaled.mtz --reshigh 1.8

# Intensities to amplitudes
ctruncate.py --mtz scaled.mtz --mtzout truncate.mtz

# Generate free set
uniqueify -p 0.05 truncate.mtz free.mtz

# Molecular replacement
phaser.py --pdb model.pdb --mtz free.mtz

# Refine the model and open coot
refmac.py --pdb phaser.1.pdb --mtz free.mtz --coot
```


**For all options run the wrapper with the -h flag:**
```
refmac.py -h

usage: refmac.py [options]

required arguments:
  --pdb input.pdb  PDB input file
  --mtz input.mtz  MTZ input file

optional arguments:
  -h, --help       show this help message and exit
  --cycles 10      No. of cycles (Default: 10)
  --breset 30      Reset B Factor at start to value
  --bref ISOT      B refinement (Default: ISOT. Options: OVER, ISOT, ANIS, MIXED)
  --mode HKRF      Refinement Mode (Default: HKRF. Options: HKRF, RIGID, TLSR)
  --weight 0.5     Weight matrix (Default: Auto)
  --output name    Outfile file name (Default: YYMMDD-HHMMSS-refmac)
  --showcommand    Print the full refmac command
  --coot           Run Coot after refinement
  --custom CUSTOM  Pass custom keywords to refmac
  --libin LIBIN    Add a dictionary
  --tlsin TLSIN    TLS definitions
  -v, --verbose    Verbose

```
