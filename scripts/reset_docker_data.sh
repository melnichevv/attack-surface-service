#!/bin/bash
file_path="$1"
_start=$(date +%s)

echo "Rebuilding database schema..."
python3 manage.py flush --noinput
python3 manage.py migrate

echo "Loading fixtures..."
python3 manage.py loaddata init

echo "Loading initial data from $file_path..."
python3 manage.py init_data --file_path=$file_path

_end=$(date +%s)
echo "Database reset complete! (took $((_end-_start))s)"
