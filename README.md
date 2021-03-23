<center><img src="CCP4Py.png" alt="CCP4Py Logo" width="800"/></center>

Unofficial python wrappers for CCP4 programs. Designed to make the task of running CCP4 programs from the command line as simple as possible. Not designed to cover every option or use case!

Currently supports: **pointless**, **aimless**, **ctruncate**, **phaser**, and **refmac**.

# Installation
Requires [CCP4](http://www.ccp4.ac.uk/download/) to be installed first.

Clone this Git repo to your user folder:
```
cd ~/
git clone https://github.com/jonathanrd/CCP4Py.git
```

Add the following to your .bashrc (Linux) or .bash_profile (Mac) and restart your terminal.
```
export PATH=/Users/YourUserFolder/CCP4Py/bin:$PATH
```
All script changes are added to Changelog.md, to update in future:
```
cd ~/CCP4Py
git pull
```

# Basic Usage

### Refining a model
```
refmac.py --pdb model.pdb --mtz data.mtz
```
Note: Running refmac.py uses the same default settings as running a refmac job from the CCP4i GUI.


### Going from integrated data to a refined model
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
phaser.py --pdb model.pdb --mtz free.mtz --output phaser

# Refine the model and open coot
refmac.py --pdb phaser.1.pdb --mtz free.mtz --coot

```


### For all options run any wrapper with the -h flag:
```
usage: refmac.py [options]

required arguments:
  --pdb input.pdb  PDB input file
  --mtz input.mtz  MTZ input file

common arguments:
  --cycles 10      No. of cycles [10]
  --bref ISOT      B refinement (OVER, [ISOT], ANIS, MIXED)
  --ncs none       Auto NCS ([none], local, global)
  --libin LIBIN    Add a dictionary.
  --logview        Run CCP4 logview while refmac is running.
  --coot           Run Coot after refinement.

optional arguments:
  -h, --help       show this help message and exit
  --mode HKRF      Refinement Mode ([HKRF], RIGID, TLSR)
  --breset 30      Reset B Factor at start to specified value
  --labels normal  Refine with SAD or exp. data ([normal], sad, hl)
  --weight 0.5     Weight matrix [auto]
  --output         Outfile file name [YYMMDD-HHMMSS-refmac]
  --showcommand    Print the full refmac command and stop.
  --custom CUSTOM  Pass custom keywords to refmac.
  --tlsin TLSIN    TLS definitions.
  --tlscycles 0    Number of TLS cycles.
```
