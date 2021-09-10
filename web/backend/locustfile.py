import time

from locust import HttpUser, task, tag, events

from app.models import RecommendRoutesRequest, RecommendRoutesTaskStatus


class SynthesisAppUser(HttpUser):

    @tag('sync')
    @task
    def sync_run(self):
        request = RecommendRoutesRequest(
            target_entry_id='mp-9029',
            temperature=1600,
            pressure=0.001,
            max_component_precursors=2,
            show_fraction_known_precursors=False,
            show_known_precursors_only=False,
            display_peroxides=True,
            add_pareto=True
        )

        self.client.post('/api/recommend_routes', json=request.dict())

    @tag('async')
    @task
    def async_run(self):
        request = RecommendRoutesRequest(
            target_entry_id='mp-9029',
            temperature=1600,
            pressure=0.001,
            max_component_precursors=2,
            show_fraction_known_precursors=False,
            show_known_precursors_only=False,
            display_peroxides=True,
            add_pareto=True
        )

        start_time = time.time() * 1000
        resp = self.client.post('/api/recommend_routes_task', json=request.dict())
        query = f'/api/recommend_routes_task/{resp.json()["task_id"]}'

        status = RecommendRoutesTaskStatus.INVALID
        while status != RecommendRoutesTaskStatus.SUCCESS:
            resp = self.client.get(query, name="/api/recommend_routes_task/[task_id]")
            status = resp.json()['status']
            time.sleep(1)
        end_time = time.time() * 1000

        events.request_success.fire(
            request_type="task",
            name="async_run",
            response_time=end_time - start_time,
            response_length=0,
        )
