import argparse
import time
from pathlib import Path

import requests


def post_endpoint(event_log_name: str, endpoint_url: str):
    client = make_client()
    assets_dir = Path(__file__).parent.parent / 'assets'

    start = time.time()
    response = make_post(client, assets_dir, endpoint_url, event_log_name)
    end = time.time()

    print(f'Response status code: {response.status_code}')
    print(f'Response content: {response.content.decode("utf-8")}')
    print(f'Elapsed time: {end - start}s')


def make_client() -> requests.Session:
    client = requests.Session()
    return client


def make_post(client: requests.Session, assets_dir: Path, endpoint_url: str, event_log_name: str) -> requests.Response:
    configuration_path = assets_dir / 'sample.yaml'
    event_log_path = assets_dir / event_log_name

    data = {
        'configuration': ('configuration.yaml', configuration_path.open('rb'), 'text/yaml'),
        'event_log': ('event_log.xes', event_log_path.open('rb'), 'application/xml'),
    }

    return client.post(
        endpoint_url,
        files=data,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('log_name', type=str, help='Name of the event log to post (e.g. "PrepaidTravelCost.xes")')
    parser.add_argument('--endpoint', type=str, default='http://localhost:8000/discoveries')
    args = parser.parse_args()

    post_endpoint(args.log_name, args.endpoint)
