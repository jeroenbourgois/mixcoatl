#!/usr/bin/env bash

regionid=`dcm-list-regions | grep us-east-1 | awk '{ print $2; }'`
firewallid=`dcm-list-firewalls | grep -v "Firewall ID" | grep -v "+--" | head -n 1 | awk '{ print $2; }'`
txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
bldgrn=${txtbld}$(tput setaf 2)
txtrst=$(tput sgr0)
STARTTIME=$(date +%s)

for i in `ls bin/dcm-list-*`; do 
	echo -n "Running $i "
	case $i in
		bin/dcm-list-users)
			;;
		bin/dcm-list-datacenters)
			$i -r $regionid > /dev/null 2>&1
			;;
		bin/dcm-list-machine-images)
			$i -r $regionid > /dev/null 2>&1
			;;
		bin/dcm-list-networks)
			$i -r $regionid > /dev/null 2>&1
			;;
		bin/dcm-list-server-products)
			$i -r $regionid > /dev/null 2>&1
			;;
		bin/dcm-list-groups)
			$i -a > /dev/null 2>&1
			;;
		bin/dcm-list-server-terminate)
			$i -a > /dev/null 2>&1
			;;
		bin/dcm-list-firewall-rules)
			$i $firewallid > /dev/null 2>&1
			;;
		bin/dcm-list-servers)
			$i -a > /dev/null 2>&1
			;;
		bin/dcm-list-snapshots)
			$i -r $regionid > /dev/null 2>&1
			;;
		*)
			$i > /dev/null 2>&1
			;;
	esac

	if [ $? != 0 ]; then
		echo "[ ${bldred}Failed${txtrst} ]";
	else
		echo "[ ${bldgrn}OK${txtrst} ]"
	fi
done

ENDTIME=$(date +%s)
echo "It took $(($ENDTIME - $STARTTIME)) seconds to complete this task..."
