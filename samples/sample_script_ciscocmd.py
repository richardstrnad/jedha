from __future__ import print_function

from jedha.cdp import *
import sys

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    print('Please provide an input file as argument\n\npython sample_script_ciscocmd.py sample_input_ciscocmd.txt')
    sys.exit(2)

with open(input_file) as input_f:
    cdp_file = input_f.read()

cdp_devs = ciscocmd_input(cdp_file)

for dev in cdp_devs:
    d = '-' * 80
    print('{}\n{}\n{}'.format(d, dev.hostname, d))
    for cdp_entry in dev.cdp_entries:
        print(cdp_entry.create_interface_description(), '\n')