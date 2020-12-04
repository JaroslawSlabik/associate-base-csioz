#docker run -it -v /home/jslabik/projects/my/python/django/first_project:/src -w /src/ -p 8111:8000/tcp  django_postgresql:1.8 /bin/bash -c "service postgresql restart && python3 manage.py sqlmigrate associate 0001 && python3 manage.py migrate && python3 manage.py createsuperuser && python3 manage.py runserver 0.0.0.0:8000"

#docker run -it -v /home/jslabik/projects/my/python/django/first_project:/src -w /src/ -p 8111:8000/tcp  django_postgresql:1.8 /bin/bash

docker run -it -v $PWD:/src -w /src/ -p 8111:8000/tcp  django_postgresql:1.8 /bin/bash -c "service postgresql restart && python3 manage.py sqlmigrate associate 0001 && python3 manage.py migrate && python3 manage.py createsuperuser && python3 manage.py runserver 0.0.0.0:8000"
