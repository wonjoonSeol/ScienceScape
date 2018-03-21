#!/bin/sh
python_v="python3"
echo $1 "+" $2

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
