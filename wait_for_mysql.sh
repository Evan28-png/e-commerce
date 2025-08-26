#!/bin/sh
while ! nc -z db 3306; do
  echo "Waiting for MySQL to start..."
  sleep 1.4
done
echo "MySQL is up!"
flask db upgrade 
gunicorn app:app --bind 0.0.0.0:5000 --log-level debug --capture-output

#use exec only once pref last command to run
#as it repleacves the shell
