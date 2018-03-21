#!/bin/sh

#
# HOW TO USE:
#	First parameter is your python alias: python or python3
#	Second parameter is what you want to test: frontend, backend or both
#
#	eg: ./test.sh python3 backend
#

#default
python_v="python3"

if [ ! -z "$1" -a "$1" == "help" ]
then
	echo "HOW TO USE:\n
	First parameter is your python alias: python or python3\n
	Second parameter is what you want to test: frontend, backend or both\n
	\n\n
	eg: ./test.sh python3 backend"

else

	if  [ ! -z "$1"  -a "$1" == "python" ]
	then
		python_v="python"
	fi

	if [ ! -z "$1"  -a "$1" == "python3" ]
	then
		python_v="python3"
	fi

	if ! [ -z "$2" ]; then
		if [ "$2" == "frontend" ]; then
			echo "\n ---- Front end test ----- | using $python_v alias \n"
			"$python_v" manage.py test tests/frontend_tests --settings=mysite.settings.local
		fi
		if [ "$2" == "backend" ]; then
			echo "\n ---- Back end test ----- | using $python_v alias \n"
			"$python_v" manage.py test tests/bibliotools_tests --settings=mysite.settings.local
		fi
		if [ "$2" == "both" ]; then
			 echo "\n ---- Front end test ----- | using $python_v alias \n"
			 "$python_v" manage.py test tests/frontend_tests --settings=mysite.settings.local
			 echo "\n ---- Back end test ----- | using $python_v alias \n"
			 "$python_v" manage.py test tests/bibliotools_tests --settings=mysite.settings.local
	    fi
	fi
fi
