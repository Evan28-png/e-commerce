#!/bin/sh
while ! nc -z db 3306; do
  echo "Waiting for MySQL to start..."
  sleep 1.4
done
echo "✅ MySQL is up, running migrations..."
flask db upgrade 

echo "✅ Starting application....."
gunicorn app:app -w 2 --bind 0.0.0.0:3000 --log-level debug --capture-output

#use exec only once pref last command to run
#as it replaces the shell
