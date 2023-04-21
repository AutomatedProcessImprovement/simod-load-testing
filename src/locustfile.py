import os
import random
from pathlib import Path

from locust import FastHttpUser, constant, task
from locust.contrib.fasthttp import FastHttpSession


class BaseProfile(FastHttpUser):
    host = os.environ.get("SIMOD_HTTP_URL")
    endpoint_url = f"{host}/discoveries"
    assets_dir = Path(__file__).parent.parent / "assets"
    wait_time = constant(1)


class ExponentialProfile(BaseProfile):
    def wait_time(self):
        return random.expovariate(1 / 15)


class PrepaidTravelCostSingleTask(BaseProfile):
    @task
    def post(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "PrepaidTravelCost.xes"
        )


class PrepaidTravelCostExponential(ExponentialProfile):
    @task
    def post(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "PrepaidTravelCost.xes"
        )

    @task
    def post2(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "PrepaidTravelCost.xes"
        )

    @task
    def post3(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "PrepaidTravelCost.xes"
        )


class RequestForPaymentSingleTask(BaseProfile):
    @task
    def post(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )


class RequestForPaymentExponential(ExponentialProfile):
    @task
    def post(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )

    @task
    def post2(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )

    @task
    def post3(self):
        make_post(
            self.client, self.assets_dir, self.endpoint_url, "RequestForPayment.xes"
        )


def make_post(
    client: FastHttpSession, assets_dir: Path, endpoint_url: str, event_log_name: str
):
    configuration_path = assets_dir / "sample.yaml"
    event_log_path = assets_dir / event_log_name

    data = {
        "configuration": (
            "configuration.yaml",
            configuration_path.open("rb"),
            "text/yaml",
        ),
        "event_log": ("event_log.xes", event_log_path.open("rb"), "application/xml"),
    }

    client.post(
        endpoint_url,
        headers={"Content-Type": "multipart/form-data"},
        files=data,
    )
