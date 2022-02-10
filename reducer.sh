#!/bin/bash

# Usage : bash reducer.sh employeelist.txt 1 10

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
