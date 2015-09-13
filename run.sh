#!/bin/bash

out=run.log

for target in 12 123 1234 12345 123456 1234567 12345678; do
	i=0
	while [ "$i" != 10 ]; do
		python expr.py -t $target -g 5 -c 11 -l $out
		i=`expr $i + 1`
	done
done

