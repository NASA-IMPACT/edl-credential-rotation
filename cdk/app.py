import os

from aws_cdk import aws_events, aws_events_targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda
from aws_cdk import aws_logs as logs
from aws_cdk import core

# Required env settings
STACKNAME = os.environ["STACKNAME"]
LAMBDA = os.environ["LAMBDA"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


class Stack(core.Stack):
    def __init__(self, scope: core.Construct, stack_name: str, **kwargs) -> None:
        super().__init__(scope, stack_name, **kwargs)

        self.role = iam.Role(
            self,
            "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        self.role.add_to_policy(
            iam.PolicyStatement(
                resources=[LAMBDA],
                actions=[
                    "lambda:GetFunctionConfiguration",
                    "lambda:UpdateFunctionConfiguration",
                ],
            )
        )

        self.function = aws_lambda.Function(
            self,
            f"{stack_name}-raster-lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            role=self.role,
            code=aws_lambda.Code.from_docker_build(
                path=os.path.abspath("../edl_credential_rotation"),
                file="Dockerfile",
                platform="linux/amd64",
            ),
            handler="handler.handler",
            memory_size=5000,
            timeout=core.Duration.minutes(5),
            environment={
                "LAMBDA": LAMBDA,
                "USERNAME": USERNAME,
                "PASSWORD": PASSWORD,
            },
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        self.rule = aws_events.Rule(
            self,
            "Rule",
            schedule=aws_events.Schedule.expression("cron(0/30 * * * ? *)"),
        )
        self.rule.add_target(aws_events_targets.LambdaFunction(self.function))


app = core.App()
Stack(scope=app, stack_name=STACKNAME)

for k, v in {
    "Project": "hls",
    "Stack": STACKNAME,
}.items():
    core.Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
