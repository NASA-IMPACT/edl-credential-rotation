from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    stackname: str = Field(
        default=None,
        description="Name of your stack",
    )
    project: str = Field(
        default=None,
        description="The project name for resource cost tracking",
    )
    lambda_name: str = Field(
        default=None,
        description="The Arn of the Lambda that will receive new S3 Credentials",
    )
    username: str = Field(
        default=None,
        description="A valid Earth Data Login user name",
    )
    password: str = Field(
        default=None,
        description="A valid Earth Data Login password",
    )
    bootstrap_qualifier: Optional[str] = Field(
        default=None,
        description="CDK Bootstrap qualifier",
    )

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
