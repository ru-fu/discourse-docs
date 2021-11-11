import sys
import re

output = []

in_table = 0

with open(sys.argv[1], 'r') as md_file:

    for line in md_file:

        if line.startswith("----") or line.startswith("|--"):

            in_table = 1

            table="TABLEHEADER#X#"

            header = output.pop().split("|")
            for one in header:
                if one:
                    table += one.strip()+"#X#"

        elif in_table:

            row = line.split("|")
            if len(row) == 1:
                in_table = 0
                output.append(table+"TABLEEND\n\n")
            else:
                table += "TABLEROW#X#"
                for one in row:
                    if one:
                        table += one.strip()+"#X#"

        else:
            output.append(line)


with open(sys.argv[1], 'w') as out_file:
    for line in output:
        out_file.write(line)
