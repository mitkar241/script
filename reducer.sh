#!/bin/bash

<<DESC
@ FileName   : reducer.sh
@ Description: Shell script to process large file by processing parts of it in parallel
@ Usage      : bash reducer.sh employeelist.txt 1 10
  - here 'employeelist.txt' is the large file with newline delimiter
  - first script will run for first 10 lines
  - next one would proces next 10 lines in parallel
    - so, bash reducer.sh employeelist.txt 11 20 , and so on.
DESC

srcfile=$1
line_1=$2
line_n=$3

sedexpr="$line_1","$line_n"p
resultfile=result-"$line_1"-"$line_n".txt

list=$(sed -n "$sedexpr" < $srcfile)

IFS='
'

for name in $list ; do
  output=$(python3 authorization.py --name "$name")
  substr='isAdmin: True'
  if [[ "$output" != *"$substr"* ]]; then
    echo "$output" >> "$resultfile"
  fi
done

# COMBINE
#cat result-*.txt > result.txt
#cat result.txt | grep "User : " | cut -d' ' -f3 > adminlist.txt
