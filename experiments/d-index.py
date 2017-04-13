#!/usr/bin/python

# The following file reads a data set and computes the d-index.
#
# "The d-index of a data set D is the maximum integer d such that D contains
#  at least d transactions of length at least d."
# The implementation below IS NOT CORRECT

from sys import argv
import os.path

# ----------------------------------------------------------------------------

# Given a line, computes the size of the transaction
def transaction_size(line):
    return len(line.split())

# ----------------------------------------------------------------------------
# Main

if len(argv) < 2:
    print('usage: d-index filename')
    exit()

filename = argv[1]
if not os.path.isfile(filename):
    print('[-] failed to open file')
    exit()

transactions = dict()
line_count = 0

with open(filename) as f:
    for line in f:
        line_count += 1
        s = transaction_size(line)
        if s in transactions:
            transactions[s] += 1
        else:
            transactions[s] = 1

d_index = 0
for key, value in transactions.iteritems():
    if value >= key and key > d_index:
        d_index = key

print('[+] parsed {} lines ...'.format(line_count))
print('[+] found {} transactions'.format(len(transactions)))
if len(transactions) > 0:
    print('[+] d-index of "{}": {}'.format(filename, max(transactions, key=transactions.get)))
    print('[+] d-index of "{}": {}'.format(filename, d_index))
