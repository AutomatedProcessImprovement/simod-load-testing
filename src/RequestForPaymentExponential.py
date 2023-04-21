import os
import random
from pathlib import Path

from locust import FastHttpUser, task

import common


class RequestForPaymentExponential(FastHttpUser):
    host = os.environ.get("SIMOD_HTTP_URL")
    endpoint_url = f"{host}/discoveries"
    assets_dir = Path(__file__).parent.parent / "assets"

    def wait_time(self):
        return random.expovariate(1 / 15)

    @task
    def post(self):
        common.make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )

    @task
    def post2(self):
        common.make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )

    @task
    def post3(self):
        common.make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )
