#!/bin/bash
getip=`egrep -v "0.0.0.0 | 127." /proc/net/fib_trie | grep -Eohm4 '[1-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | tail -n1`
filename=./hosts
hostname=nexus

#1 find a nexus string in hosts file
if 
 grep -q nexus "$filename"
#2 replace entire line
then 
 sed -i '/nexus/c\'"${getip} ${hostname}" "$filename"
#3 add to last line 
else 
 echo "$getip $hostname" >> "$filename"
fi

