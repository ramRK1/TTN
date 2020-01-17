#!/bin/sh -ex

set -o errexit
set -o pipefail
set -o nounset


celery -A app.tasks.celery beat -l debug &
celery -A app.tasks.celery worker -l info &
exec "$@";