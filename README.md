# Icom 706 prog

This is a simple script that talks to rigctld to load in memories to an Icom 706 transceiver.

## Setup

- Install hamlib and then run the rigctld like:

```
rigctld -m 3009 -r /dev/ttyUSB0 -s 9600 --set-conf=poll_interval=0,cache_timeout=0
```

- Install or make sure you have Python 3.8 or later.

- Install icom-706-prog:

```
git clone git@github.com:alangarf/icom-706-prog.git
cd icom-706-prog
python -m venv venv
source venv/bin/activate

pip install -e .
```

You should be now ready.

## Usage

Create a CSV file like the example file: wia_2m.csv

Run the script:
```
✦6 [21:39:29] ❯ icom --csv ./wia_2m.csv 
Setting up radio mode
Confirm tone is turned on for VFOA! [y/N]: y
Confirm tone is turned on for VFOB! [y/N]: y
Setting memory 5
Confirm tone 88.5 [y/N]: y
Setting memory 1
Confirm tone 91.5 [y/N]: y
Setting memory 3
Setting memory 2
Setting memory 8
[SNIP]
Confirm tone 94.8 [y/N]: y
Setting memory 21
Confirm tone 103.5 [y/N]: y
Setting memory 47
Confirm tone 118.8 [y/N]: y
Setting memory 45
Confirm tone 123.0 [y/N]: y
Setting memory 25
Setting memory 29
Setting memory 18
[SNIP]
Finished setting 56 memories
```

The script will try any minimize the manual changes needed to set the tone values by sorting the memories in the CSV files to put all the like tones together. This greatly reduces the work required to manually set the tones on these radios.

This script should be easily extendable to support other radios that hamlib supports (not just Icom 706's). It's simply feeding rigctl commands to do the work. I have added comments and such to make it easy to understand. For radios that support setting duplex and CTCSS tones etc via the control port of the radio, you won't need the manual steps to set these up.


Good luck!

VK2LAG
