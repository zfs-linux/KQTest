# Filename 	: run_tests.sh
# Description 	: tool to test the iotest tool

#!/bin/bash
FILENAME=datafile

sleep 1
for sequence in random seq
	do
	sleep 1
	for sparse_factor in  2 3 4 5 6 7 8 9 10 11 12 13 14 15
		do
		sleep 1
		for num_threads in 2 3 4 5 6 7 8 9 10 11 12 13 14
			do
			sleep 1
			for count  in 456 567 8 256 0512 1024 4096 
				do
				sleep 1
				for iosize in  512 1024 2048 8192 
					do
					sleep 1
					for offset in  512 1536 4096 0 8192 16384 20480
						do
						sleep 1
						for write_method in mmap bufferedio directio
							do
							sleep 1
							for read_method in mmap bufferedio directio
								do
								rm -f $FILENAME
								filename="./logs/test""_offset_""$offset""_iosize_""$iosize""_count_""$count""_write_""$write_method""_read_""$read_method""_seq_""$sequence""_threads_""$num_threads"
								set -x
								./iotest -o $FILENAME -w "offset=$offset,count=$count,iosize=$iosize" -q $sequence -k $write_method -f $read_method -F pattern -s $sparse_factor -t sparse -y $num_threads -V 2>&1 1> $filename 
								set +x
								lines=`grep failed $filename | wc -l`
								if [ $lines -gt 0 ]
								then
									echo "Error occured $filename"
									echo "$filename" >> errors
								else 
									lines=`grep fault $filename | wc -l`
									if [ $lines -gt 0 ]
									then
										echo "Error occured"
										echo "$filename" >> errors
									else
									echo "offset : ""$offset"" iosize : ""$iosize"" count : ""$count"" write : ""$write_method"" read : ""$read_method"" sequence : ""$sequence " sparse :" "$sparse_factor"   " "...done"
									echo "offset : ""$offset"" iosize : ""$iosize"" count : ""$count"" write : ""$write_method"" read : ""$read_method"" sequence : ""$sequence " sparse :" "$sparse_factor"   "threads:"" "$num_threads" " seed" :"$seed ""...done" >> tests_done
									fi
								fi	
							done
						done
					done
				done
			done
		done
	done
done
