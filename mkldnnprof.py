#! /usr/bin/env python
import os, sys
import subprocess

os.environ['MKLDNN_VERBOSE'] = '1'

print('Executing:', sys.argv[1:])
output = subprocess.getoutput(' '.join(sys.argv[1:]))

#print('Output:', output)

with open('mkldnn_log.csv', 'w') as f:
    for l in output.split('\n'):
        if 'mkldnn' in l and 'exec' in l:
            print(l)
            f.write(l + '\n')

import pandas as pd
data = pd.read_csv('mkldnn_log.csv', names=['mkl', 'exec', 'type', 'jit', 'pass', 'fmt', 'opt', 'shape', 'time'])
print(data)

print('Total MKLDNN time:', data['time'].sum())

print()
print('Op type breakdown:')
print(data.groupby('type')['time'].sum().sort_values().head(5))

print()
print('Shape breakdown:')
print(data.groupby('shape')['time'].sum().sort_values().head(5))