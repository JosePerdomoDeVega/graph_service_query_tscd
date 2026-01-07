from locust import HttpUser, task, between


class JobSubmitUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def submit_job(self):
        payload = {
            "operation": "min_path",
            "origin_word": "dog",
            "destination_word": "beg",
            "callback_url": "http://localhost:9000/callback"
        }

        headers = {
            "Content-Type": "application/json"
        }

        with self.client.post(
                "/jobs",
                json=payload,
                headers=headers,
                catch_response=True
        ) as response:
            if response.status_code != 200 and response.status_code != 201:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                response.success()
