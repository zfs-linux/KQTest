#!/bin/ksh
#
#



str=$(cat /proc/mounts | grep tank | tr -s " " " " | cut -d " " -f 2)



set -A str $str

echo "str : ${#str[*]}"


count=${#str[*]}


for (( i=$(($count - 1)) ; i >= 0 ; i-- ))
do
     echo "$i : ${str[$i]} "
#     umount ${str[$i]}  

done
