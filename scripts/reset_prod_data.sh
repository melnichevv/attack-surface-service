#!/bin/bash
file_path="$1"
_dkc() { docker-compose -f docker-compose.prod.yml --log-level ERROR "$@"; }
_dkc-run() { _dkc run -e LOGGING_LEVEL_CONSOLE=WARNING --rm "$@"; }
_start=$(date +%s)

echo "Re-creating database."
_dkc-run django python3 manage.py flush --noinput

echo "Rebuilding database schema..."
_dkc-run django python3 manage.py migrate

echo "Loading fixtures..."
_dkc-run django python3 manage.py loaddata init

echo "Loading initial data from $file_path..."
_dkc-run django python3 manage.py init_data --file_path=$file_path

_end=$(date +%s)
echo "Database reset complete! (took $((_end-_start))s)"
