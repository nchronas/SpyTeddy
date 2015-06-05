#!/bin/bash

# remove all DNAT rules
echo -e '\t* removing all DNAT rules'
for i in $(iptables -t nat -L -n  --line-numbers | grep ^[1-9].*DNAT | awk '{ print $1 }' | tac); do echo $i; iptables -t nat -D PREROUTING $i; done

if [ $1 == "ADD" ]
	then
		# forward all 80 to local tether
		tether_ip=$(ifconfig tether | awk '/inet addr/{print substr($2,6)}')

		run="iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination $tether_ip:$2"

		echo -e "\t* running: $run"

		`$run`
fi

