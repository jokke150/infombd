#!/usr/bin/python

# ----------------------------------------------------------------------------
# Author:      Jasper Robeer (3802337)
# Description: Implementation of the frequent itemset mining experiment,
#              comparing Toivonen's bounds to the d-bound.
#              As part of the Big Data course at Utrecht University (2017).
# ----------------------------------------------------------------------------

from sys import argv
from fim import apriori
from math import log, floor
import time
import csv
import random

# ----------------------------------------------------------------------------

# Parses a .dat dataset into a format useable by fim
# The 'rep' parameter indicates how many times the data set should be replicated
def parse_dat(fname, rep=1):
    result = []
    rep_result = []
    line_count = 0

    with open(fname) as inp:
        for line in inp:
            line_count += 1
            items = line.split()
            if len(items) > 0:
                result.append(map(int, items))
    
    print('[+] parsed {:,} lines'.format(line_count))
    if rep > 1:
        print('[+] blowing up transactions {:,} times'.format(rep))
        for i in xrange(rep):
            rep_result.extend(result)
    else:
        rep_result = result

    print('[+] found {:,} transactions'.format(len(rep_result)))
    return rep_result

# ----------------------------------------------------------------------------

# Computes the Toivonen's bound
def toivonen_bound(epsilon, delta):
    return int((1.0/(2.0 * epsilon * epsilon))*log(2.0/delta))

# Computes the d-bound
def dbound_bound(size, epsilon, delta, d_index, c):
    opt = ((4.0 * c)/(epsilon * epsilon)) * (d_index + log(1.0/delta))
    return int(min(size, opt))

# ----------------------------------------------------------------------------

# Returns a sample of size n of the data set, sampled with replacement
def sample_n(transactions, n):
    sample = []
    for i in xrange(n):
        sample.append(random.choice(transactions))
    return sample

# ----------------------------------------------------------------------------

def experiment(epsilon, delta):
    ts = time.time()
    
    t_bound = toivonen_bound(epsilon, delta)
    d_bound = dbound_bound(transactions_len, epsilon, delta, float(d_index), 1.0)
    print('[+] Performing experiment with (epsilon: {}, delta: {})'.format(epsilon, delta))
    print('    Toivonen\'s bound: {:,}'.format(t_bound))
    print('    d-bound: {:,}'.format(d_bound))
    
    te = time.time()
    print('[/] Experiment duration: {:.4f} ms'.format((te - ts)*1000.0))
    print('')
    return [str(epsilon), str(delta), str(t_bound), str(d_bound)]

# ----------------------------------------------------------------------------

if len(argv) < 3:
    print('usage: mining.py filename d-index [rep]')
    exit()

fname   = argv[1]
d_index = int(argv[2])
epsilon = [0.01, 0.015, 0.02, 0.025]
delta   = [0.01, 0.05, 0.1]
mu      = [1.0]
rep     = 1

if len(argv) > 3:
    rep = int(argv[3])

transactions     = parse_dat(fname, rep)
transactions_len = len(transactions)

print('')

csv_fname = 'result-{}-{}.csv'.format(fname, rep)
csv_data  = [['epsilon', 'delta', 'toivonen', 'd-bound']]

for e in epsilon:
    for d in delta:
        csv_data.append(experiment(e, d))

with open(csv_fname, 'wb') as f:
    writer = csv.writer(f, delimiter=';')
    for line in csv_data:
        writer.writerow(line)

print('[+] Wrote results to {}'.format(csv_fname))
