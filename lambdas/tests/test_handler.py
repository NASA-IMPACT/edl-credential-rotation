import os
from unittest.mock import MagicMock, PropertyMock, patch

from lambdas.handler import handler

s3_credentials = {
    "secretAccessKey": "key",
    "accessKeyId": "key_id",
    "sessionToken": "session_token",
}
username = "username"
password = "password"
lambda_name = "lambda"


@patch("lambdas.handler.boto3")
@patch("lambdas.handler.SessionWithHeaderRedirection")
@patch.dict(
    os.environ,
    {
        "USERNAME": username,
        "PASSWORD": password,
        "LAMBDA": lambda_name,
    },
)
def test_handler(Session, boto3):
    Session.return_value.get.return_value.json.return_value = s3_credentials
    boto3.client.return_value.get_function_configuration.return_value = {
        "Environment": {"Variables": {"SOMESETTING": "something"}}
    }
    handler({}, {})
    Session.assert_called_once_with(username, password)
    combined_variables = {
        "Variables": {
            "SOMESETTING": "something",
            "SECRET_ACCESS_KEY": s3_credentials["secretAccessKey"],
            "ACCESS_KEY_ID": s3_credentials["accessKeyId"],
            "SESSION_TOKEN": s3_credentials["sessionToken"],
        }
    }
    boto3.client.return_value.update_function_configuration.assert_called_once_with(
        FunctionName=lambda_name,
        Environment=combined_variables,
    )
