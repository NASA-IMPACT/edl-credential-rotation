import os

import boto3
import requests
from aws_lambda_typing import context as context_
from aws_lambda_typing import events


class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = "urs.earthdata.nasa.gov"

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if "Authorization" in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (
                (original_parsed.hostname != redirect_parsed.hostname)
                and redirect_parsed.hostname != self.AUTH_HOST
                and original_parsed.hostname != self.AUTH_HOST
            ):
                del headers["Authorization"]

        return


def handler(
    event: events.CloudWatchEventsMessageEvent, context: context_.Context
) -> None:
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
    LAMBDA = os.environ["LAMBDA"]

    session = SessionWithHeaderRedirection(USERNAME, PASSWORD)
    response = session.get(
        "https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials"
    ).json()
    client = boto3.client("lambda")
    function_config = client.get_function_configuration(FunctionName=LAMBDA)
    function_environment = function_config["Environment"]
    function_environment["Variables"]["SECRET_ACCESS_KEY"] = response["secretAccessKey"]
    function_environment["Variables"]["ACCESS_KEY_ID"] = response["accessKeyId"]
    function_environment["Variables"]["SESSION_TOKEN"] = response["sessionToken"]

    client.update_function_configuration(
        FunctionName=LAMBDA,
        Environment=function_environment,
    )
