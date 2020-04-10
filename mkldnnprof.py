#! /usr/bin/env python
import os, sys
import subprocess

os.environ['MKLDNN_VERBOSE'] = '1'

def run_workload(outfile='mkldnn_log.csv'):
    print('Executing:', sys.argv[1:])
    output = subprocess.getoutput(' '.join(sys.argv[1:]))

    #print('Output:', output)

    with open(outfile, 'w') as f:
        for l in output.split('\n'):
            if 'mkldnn' in l and 'exec' in l:
                print(l)
                f.write(l + '\n')

def parse_log(logfile='mkldnn_log.csv'):
    import pandas as pd
    data = pd.read_csv(logfile, names=['mkl', 'exec', 'type', 'jit', 'pass', 'fmt', 'opt', 'shape', 'time'])
    print(data)

    print('Total MKLDNN time:', data['time'].sum())

    print()
    print('JIT type breakdown:')
    print(data.groupby('jit')['time'].sum().sort_values().head(10))

    print()
    print('Op type breakdown:')
    print(data.groupby('type')['time'].sum().sort_values().head(10))

    print()
    print('Shape breakdown:')
    print(data.groupby('shape')['time'].sum().sort_values().head(5))

if __name__ == '__main__':
    if len(sys.argv) > 1 and '.csv' in sys.argv[1]:
        parse_log(sys.argv[1])
    else:
        run_workload()
        parse_log()