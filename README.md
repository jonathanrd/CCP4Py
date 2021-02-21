# CCP4Py
Python wrappers for CCP4 programs. Each can be run directly from the command line or called from within a python script or pipeline.

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

# Usage

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



## For individual wrapper usage see below

### pointless.py
```
pointless.py --mtz integrated.mtz --mtzout sorted.mtz
```

Currently, pointless.py supports the following options:

```
usage: pointless.py [options]

required arguments:
  --mtz input.mtz      MTZ input file

optional arguments:
  -h, --help           show this help message and exit
  --mtzout output.mtz  MTZ output file (Default: YYMMDD-HHMMSS-pointless.mtz)
  --logout output.log  Log filename (Default: YYMMDD-HHMMSS-pointless.log)
  --spacegroup P1      Input a known spacegroup
  --showcommand        Show AIMLESS command
  -v, --verbose        Verbose
```




### aimless.py
```
aimless.py --mtz sorted.mtz --mtzout aimless.mtz --reshigh 1.8
```

Currently, pointless.py supports the following options:

```
usage: aimless.py [options]

required arguments:
  --mtz input.mtz      MTZ input file

optional arguments:
  -h, --help           show this help message and exit
  --mtzout output.mtz  MTZ output file (Default: YYMMDD-HHMMSS-aimless.mtz)
  --logout output.log  Log filename (Default: YYMMDD-HHMMSS-aimless.log)
  --reshigh RESHIGH    High resolution limit
  --showcommand        Show AIMLESS command
  -v, --verbose        Verbose
```

### ctruncate.py
```
ctruncate.py --mtz aimless.mtz --mtzout truncate.mtz
```

Currently, ctruncate.py supports the following options:

```
usage: ctruncate.py [options]

required arguments:
  --mtz input.mtz      MTZ input file

optional arguments:
  -h, --help           show this help message and exit
  --mtzout output.mtz  MTZ output file (Default: YYMMDD-HHMMSS-ctruncate.mtz)
  --logout output.log  Log filename (Default: YYMMDD-HHMMSS-ctruncate.log)
  --showcommand        Show AIMLESS command
  -v, --verbose        Verbose
```


### phaser.py
```
phaser.py --pdb model.pdb --mtz free.mtz
```

Currently, phaser.py supports the following options:
```
usage: phaser.py [options]

required arguments:
  --pdb input.pdb      PDB input file
  --mtz input.mtz      MTZ input file

optional arguments:
  -h, --help           show this help message and exit
  --log LOG            Log filename
  --output OUTPUT      Output suffix
  --identity IDENTITY  Model identity
  --totalmw TOTALMW    Composition MW
  --nmol NMOL          No. of mol in asu (Default: 1)
  --showcommand        Show phaser command
  -v, --verbose        Verbose
```




### refmac.py
```
refmac.py --pdb model.pdb --mtz data.mtz -v

Running Refmac..
Log file at: 210221-140739-refmac.log
       R factor    0.2524   0.2500
         R free    0.3035   0.3074
 Rms BondLength    0.0090   0.0089
  Rms BondAngle    1.6879   1.6758

coot --pdb 210221-140739-refmac.pdb --auto 210221-140739-refmac.mtz
```

Currently, refmac.py supports the following options:
```
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
