#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python init_data.py
