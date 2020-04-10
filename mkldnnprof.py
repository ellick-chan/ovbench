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

def load_log(log):
    import pandas as pd
    data = pd.read_csv(log, names=['mkl', 'exec', 'type', 'jit', 'pass', 'fmt', 'opt', 'shape', 'time'])
    data = data[data['exec'] == 'exec']
    return data

def parse_log(logfile='mkldnn_log.csv'):
    data = load_log(logfile)
    print('Total MKLDNN time:', data['time'].sum())
    print('Total MKLDNN ops:', data['time'].count())

    print()
    print('JIT type breakdown:')
    print(data.groupby('jit')['time'].sum().sort_values().head(10))
    print(data['jit'].value_counts().head(10))

    print()
    print('Op type breakdown:')
    print(data.groupby('type')['time'].sum().sort_values().head(10))
    print(data['type'].value_counts().head(10))

    print()
    print('Shape breakdown:')
    print(data.groupby('shape')['time'].sum().sort_values().head(5))

def stats_comp(name, log1, log2, d1, d2, n=5):
    import pandas as pd
    print(name, 'stats:')
    jitstat = pd.concat((d1[name].value_counts(), d2[name].value_counts()), axis=1)
    jitstat.columns = ('1-' + log1, '2-' + log2)
    jitstat['comparison'] = jitstat.iloc[:, 1] / jitstat.iloc[:, 0]
    print(jitstat.sort_values('1-' + log1, ascending=False).head(n))
    print()
    jitstat = pd.concat((d1.groupby(name)['time'].sum(), d2.groupby(name)['time'].sum()), axis=1)
    jitstat.columns = ('1-' + log1, '2-' + log2)
    jitstat['comparison'] = jitstat.iloc[:, 1] / jitstat.iloc[:, 0]
    print(jitstat.sort_values('1-' + log1, ascending=False).head(n))

def compare(log1, log2):
    print('Comparing:', log1, log2)
    print()

    d1 = load_log(log1)
    d2 = load_log(log2)

    print('Total time %s: %0.2f\t---  %s: %0.2f' % (log1, d1['time'].sum(), log2, d2['time'].sum()))
    print('Total  ops  %s: %d\t\t---  %s: %d'    % (log1, d1['time'].count(), log2, d2['time'].count()))

    print()
    stats_comp('jit', log1, log2, d1, d2)

    print()
    stats_comp('type', log1, log2, d1, d2)

    print()
    stats_comp('shape', log1, log2, d1, d2)

if __name__ == '__main__':
    if len(sys.argv) > 2 and '.csv' in sys.argv[1] and '.csv' in sys.argv[2]:
        compare(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1 and '.csv' in sys.argv[1]:
        parse_log(sys.argv[1])
    else:
        run_workload()
        parse_log()
