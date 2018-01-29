import pandas as pd
from collections import namedtuple, OrderedDict

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("CSV_file", help="Specify CSV file")
parser.add_argument("output_file", help="Specify output file")
args = parser.parse_args()

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def is_in(row, labels):
    for label in labels:
        if row['class'] == label: return 1

    return 0


###MAIN###
examples = pd.read_csv(args.CSV_file)
grouped = split(examples, 'filename')

labels = list()

for group in grouped:
    for index, row in group.object.iterrows():
        if not is_in(row, labels): labels.append(row['class'])

f = open(args.output_file, "w")
x = 1
for label in labels:
    f.write("item {\n")
    f.write("  id: "+str(x)+"\n")
    f.write("  name: '"+label+"'\n")
    f.write("}\n")
    x = x+1

f.close()
