#!/bin/bash

# Collect static files.
echo "Collecting staticfiles..."
python manage.py collectstatic --noinput 

# Wait for the database to start up.
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations main --noinput 
python manage.py migrate --noinput 


if [ "$SEARCH" = "elasticsearch" ]; then
# Wait for the Elasticsearch server to start up.
    echo "Waiting for elasticsearch..."

    STATUS=$(curl --write-out %{http_code} --silent --output /dev/null http://$SEARCH_HOST:$SEARCH_PORT/_cat/health?h=st)

    while ! [ $STATUS = 200 ]; do
        sleep 0.5
        STATUS=$(curl --write-out %{http_code} --silent --output /dev/null http://$SEARCH_HOST:$SEARCH_PORT/_cat/health?h=st)
        echo $STATUS
    done

    echo "Elasticsearch started"
# Rebuild the elasticsearch index.
    echo "Rebuilding search index..."
    printf 'y\n' | python manage.py search_index --rebuild 
fi

exec "$@"
