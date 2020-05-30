#!/bin/bash
# If you are not using `django` docker container - run command with local argument:
# `./scripts/reset_local_data.sh local`

_env=$1
_dkc() { docker-compose --log-level ERROR "$@"; }
_dkc-run() { _dkc run -e LOGGING_LEVEL_CONSOLE=WARNING --rm "$@"; }
_dkc-run-django() {
  if [[ $_env == "local" ]]; then
    "$@"
  else
    _dkc-run django "$@";
  fi
}
_start=$(date +%s)

if [[ $_env == "local" ]]; then
  echo "Using local environment"
else
  echo "Using 'django' docker container"
fi

echo "Recreating blank database 'atss'"
_dkc restart postgres
while ! docker-compose --log-level ERROR run --no-deps postgres psql -h postgres -U postgres -c 'select 1;' > /dev/null 2>&1; do
    echo "Waiting for postgres initialization..."
    sleep 1
done

_dkc exec postgres dropdb --if-exists -h postgres -U postgres atss
echo "Dropped 'atss' database."

_dkc exec postgres createdb -h postgres -U postgres atss
echo "Re-created 'atss' database."

echo "Rebuilding database schema..."
_dkc-run-django python3 manage.py migrate

echo "Loading fixtures..."
_dkc-run-django python3 manage.py loaddata init

_end=$(date +%s)
echo "Database reset complete! (took $((_end-_start))s)"
