from pathlib import Path

from locust.contrib.fasthttp import FastHttpSession


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
