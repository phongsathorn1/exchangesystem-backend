#!/bin/bash
if [[ ! -d "./static" ]]
then
    echo "Not found ./static directory. creating..."
    mkdir static
fi

python3 manage.py collectstatic --no-input
python3 manage.py migrate
# python3 manage.py runserver 0.0.0.0:8000
gunicorn exchangesystem.wsgi -b 0.0.0.0:8000
