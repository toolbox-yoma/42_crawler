#!/bin/bash

cnt=0
state_done=0

while True
do
	hour=$(date +%H);
	if [ $hour -lt 21 ] && [ $hour -gt 8 ]
	then
		state_done=$(ls | grep "result.loop" | wc -l)
		if [ $state_done -gt 0 ]
		then
			break
		fi

		state_macro=$(ps | grep "agenda_hunter.py" | grep -v "grep" | wc -l)
		if [ $state_macro -eq 0 ]
		then
			now=$(date +%T);
			echo -e "\n\033[0;32mTime : $now\033[0m"
			echo -e "\033[0;31mdown : $cnt\033[0m"
			echo -e "\033[0;36mset  : intra_macro execute\033[0m\n"
			python3 agenda_hunter.py
			cnt=$((cnt + 1))
		fi
	else
		now=$(date +%T);
		echo -e "\n\033[0;32mTime : $now\033[0m"
		echo -e "\033[0;31mWait until morning\033[0m"
		sleep 600
	fi
	sleep 2
done

cnt=$((cnt - 1))
now=$(date +%T);
result=$(cat result.loop)
rm result.loop
echo -e ""
echo -e "\033[0;32mTime : $now\033[0m"
echo -e "\033[0;31mdown : $cnt\033[0m"
echo -e "\033[0;36m\n $result\033[0m\n"
echo -e "\033[0;32mclear event subscribe\033[0m\n"
