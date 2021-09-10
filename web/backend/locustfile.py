import time
import random

from locust import HttpUser, task, tag, events

from app.models import RecommendRoutesTaskStatus
from example_requests import requests


class SynthesisAppUser(HttpUser):
    """
    locust -H http://localhost -f locustfile.py -u 1 -r 1 --autostart

    # sync only
    locust --tag sync -H http://localhost -f locustfile.py -u 1 -r 1 --autostart

    # async only
    locust --tag async -H http://localhost -f locustfile.py -u 1 -r 1 --autostart
    """

    @tag('sync')
    @task
    def sync_run(self):
        request_dict = random.choice(list(requests.values()))

        start_time = time.time() * 1000
        self.client.post('/api/recommend_routes', json=request_dict)
        end_time = time.time() * 1000

        events.request_success.fire(
            request_type="task",
            name=f'{request_dict["target_entry_id"]} sync_run',
            response_time=end_time - start_time,
            response_length=0,
        )

    @tag('async')
    @task
    def async_run(self):
        request_dict = random.choice(list(requests.values()))

        start_time = time.time() * 1000
        resp = self.client.post('/api/recommend_routes_task', json=request_dict)
        query = f'/api/recommend_routes_task/{resp.json()["task_id"]}'

        status = RecommendRoutesTaskStatus.INVALID
        while status != RecommendRoutesTaskStatus.SUCCESS:
            resp = self.client.get(query, name="/api/recommend_routes_task/[task_id]")
            status = resp.json()['status']
            time.sleep(1)
        end_time = time.time() * 1000

        events.request_success.fire(
            request_type="task",
            name=f'{request_dict["target_entry_id"]} async_run',
            response_time=end_time - start_time,
            response_length=0,
        )
