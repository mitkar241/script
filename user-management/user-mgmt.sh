#!/bin/bash

Help()
{
   # Display Help
   echo "Added description of the script functions here."
   echo
   echo "Syntax: scriptTemplate [-a|-d|-h|-t]"
   echo "options:"
   echo "-h | --help           Prints help needed."
   echo "-t | --test 'string'  Prints <string>."
   echo "-a | --add            Add User."
   echo "-d | --del            Del User."
   echo
}

Test()
{
   echo "Testing Arguments $1"
}

mutually_exclusive_group_action=false

Die() {
    echo "ERROR: $*. Aborting." >&2
    exit 1
}

user_add()
{
	read -p "Enter username : " username
	read -s -p "Enter password : " password
	egrep "^$username" /etc/passwd >/dev/null
	if [ $? -eq 0 ]; then
		echo "$username exists!"
		exit 1
	else
		pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
		useradd -m -p "$pass" "$username"
		[ $? -eq 0 ] && echo "User has been added to system!" || echo "Failed to add a user!"
	fi
}

user_del()
{
	read -p "Enter username : " username
	sudo killall -u $username
	sudo userdel --remove --force $username
}

##########
# Process the input options. Add options as needed.
##########

# Am i Root user?
if [ $(id -u) -eq 0 ]; then
    while [[ "$#" -gt 0 ]]; do
	   case $1 in
	      -h|--help) # display Help
		 Help
		 exit;;
	      -t|--test) # display Test
	         value="$2"
	         shift
		 Test "$value"
		 exit;;
	      -a|--add) # User Add
		 user_add
		 exit;;
	      -d|--del) # User Del
		 user_del
		 exit;;
	      \?) # Invalid option or use *
		 echo "Error: Invalid option"
		 exit;;
	   esac
	   shift
    done
else
	echo "Only root may add a user to the system."
	exit 2
fi
