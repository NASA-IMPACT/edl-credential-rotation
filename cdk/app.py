import os

from aws_cdk import aws_events, aws_events_targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda
from aws_cdk import aws_logs as logs
from aws_cdk import App, Duration, Stack, Tags
from config import settings

app = App()

if settings.bootstrap_qualifier:
    app.node.set_context(
        "@aws-cdk/core:bootstrapQualifier", settings.bootstrap_qualifier
    )


class Stack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

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
                resources=[settings.lambda_name],
                actions=[
                    "lambda:GetFunctionConfiguration",
                    "lambda:UpdateFunctionConfiguration",
                ],
            )
        )

        self.function = aws_lambda.Function(
            self,
            f"{settings.stackname}-update-lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            role=self.role,
            code=aws_lambda.Code.from_docker_build(
                path=os.path.abspath("./"),
                file="Dockerfile",
                platform="linux/amd64",
            ),
            handler="handler.handler",
            memory_size=5000,
            timeout=Duration.minutes(5),
            environment={
                "LAMBDA": settings.lambda_name,
                "USERNAME": settings.username,
                "PASSWORD": settings.password,
            },
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        self.rule = aws_events.Rule(
            self,
            "Rule",
            schedule=aws_events.Schedule.expression("cron(0/30 * * * ? *)"),
        )
        self.rule.add_target(aws_events_targets.LambdaFunction(self.function))


Stack(app, settings.stackname)

for k, v in {
    "Project": settings.project,
    "Stack": settings.stackname,
}.items():
    Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
