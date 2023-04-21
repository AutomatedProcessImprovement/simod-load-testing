import os
from pathlib import Path

from locust import FastHttpUser, constant, task

import common


class RequestForPaymentSingleTask(FastHttpUser):
    host = os.environ.get("SIMOD_HTTP_URL")
    endpoint_url = f"{host}/discoveries"
    assets_dir = Path(__file__).parent.parent / "assets"

    wait_time = constant(1)

    @task
    def post(self):
        common.make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )
