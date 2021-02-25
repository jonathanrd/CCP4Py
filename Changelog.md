# Changelog

All notable changes to CCP4Py will be documented in this file.

## 0.4.0 2021-02-25

- refmac.py Added auto NCS option.
- refmac.py Improved error handling for bad MTZ file.
- refmac.py Added extra F, SIGF labels (phaser) to auto detect.
- pointless.py Added logview option.
- aimless.py Added option to save unmerged MTZ file.

## 0.3.0 2021-02-23

- pointless.py Added ability to use custom commands.
- refmac.py Fixed custom commands option.
- phaser.py Fixed broken regex when parsing log file.
- phaser.py Added logview option.
- phaser.py Added auto detection of FP and SIGFP labels from input MTZ.
- phaser.py Added custom commands option.

## 0.2.0 2021-02-23

- refmac.py Added auto detection of FP, SIGFP, and FREER labels from input MTZ.
- refmac.py Added ability to select F+,F- labels or HL coef. using --labels option.
- refmac.py Added logview option.

## 0.1.0 2021-02-21

- Initial version with basic support for pointless, aimless, ctruncate, phaser, and refmac.
