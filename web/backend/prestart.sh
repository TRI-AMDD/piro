# this runs before the /start.sh
# we will start redis, celery workers, celery flower in the background
# then the /start.sh starts the FastAPI app using gunicorn

run_redis_cmd="nohup redis-server"
run_celery_worker_cmd="celery -A app.tasks --broker=redis://localhost:6379/0 --result-backend=redis://localhost:6379/0 worker -l info -c 4 -Ofair --without-gossip --without-mingle"
run_celery_flower_cmd="celery -A app.tasks --broker=redis://localhost:6379/0 --result-backend=redis://localhost:6379/0 flower"

$run_redis_cmd &
$run_celery_worker_cmd &
$run_celery_flower_cmd &