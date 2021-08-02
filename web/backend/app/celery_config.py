broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

# https://medium.com/koko-networks/a-complete-guide-to-production-ready-celery-configuration-5777780b3166
worker_send_task_event = False
task_time_limit = 60 * 15
task_acks_late = True
worker_prefetch_multiplier = 1
