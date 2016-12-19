from __future__ import print_function

from jedha.cdp import *
import sys

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    print('Please provide an input file as argument\n\npython sample_script.py sample_input.txt')
    sys.exit(2)

with open(input_file) as input_f:
    cdp_file = input_f.read()

dev = Device(cdp_file)

for cdp_entry in dev.cdp_entries:
    print(cdp_entry.create_interface_description(), '\n')