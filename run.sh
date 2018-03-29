#!/bin/sh

#default
python_v="python3"
if [ -z "$1" ]
then
	echo "HOW TO USE:
	First parameter is your python alias: python or python3
	Second parameter is what you want to run: website, scripts or heroku
	\n
	eg: ./run.sh python3 website"
fi

if [ ! -z "$1" -a "$1" == "help" ]
then
	echo "HOW TO USE:
	First parameter is your python alias: python or python3
	Second parameter is what you want to run: website, server or heroku
	\n
	eg: ./run.sh python3 website"

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
		if [ "$2" == "website" ]; then
			clear
			echo "\n\n\n ---- Running website locally. ----- | using $python_v alias \n"
			"$python_v" manage.py migrate --settings=mysite.settings.local;
			"$python_v" manage.py runserver --settings=mysite.settings.local;

		fi
		if [ "$2" == "scripts" ]; then
			clear
			echo "\n\n\n ---- Runnings scripts without website. ----- | using $python_v alias \n"
			"$python_v" bibliotools3/scripts/graph_gen.py
		fi
		if [ "$2" == "heroku" ]; then
			 clear
			 echo "\n\n\n ---- Not a feature yet. ----- | using $python_v alias \n"

		fi
	fi
fi
