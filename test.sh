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
if [ -z "$1" ]
then
	echo "HOW TO USE:\n
	First parameter is your python alias: python or python3
	Second parameter is what you want to test: frontend, backend or both
	\n
	eg: ./test.sh python3 backend"
fi

if [ ! -z "$1" -a "$1" == "help" ]
then
	echo "HOW TO USE:\n
	First parameter is your python alias: python or python3
	Second parameter is what you want to test: frontend, backend or both
	Third parameter is any flags you want to add.
	\n
	eg: ./test.sh python3 backend --with-coverage"

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
			clear
			echo "\n\n\n ---- Front end test ----- | using $python_v alias \n" "$3"
			"$python_v" manage.py test tests/front_end_tests --settings=mysite.settings.local "$3"
		fi
		if [ "$2" == "backend" ]; then
			clear
			echo "\n\n\n ---- Back end test ----- | using $python_v alias \n" "$3"
			"$python_v" manage.py test tests/bibliotools_tests --settings=mysite.settings.local "$3"
		fi
		if [ "$2" == "both" ]; then
			 clear
			 echo "\n\n\n ---- Front end test ----- | using $python_v alias \n" "$3"
			 "$python_v" manage.py test tests/front_end_tests --settings=mysite.settings.local "$3"
			 echo "\n\n\n ---- Back end test ----- | using $python_v alias \n" "$3"
			 "$python_v" manage.py test tests/bibliotools_tests --settings=mysite.settings.local "$3"
	    fi
	fi
fi
