from os import path
from aws_cdk import core as cdk
#from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_cloudwatch as cloudwatch

class DemoAppStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        handler = lmb.Function(self, 'Handler',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')) ,
            #code=lmb.Code.asset('lambda'),
            )

        alias = lmb.Alias(self, 'HandlerAlias',
            alias_name='Current',
            version=handler.current_version
        )

        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service to test CDKPipeline',
            handler=alias)


        #this rollback mechanism has a bug: the API gateway has identical name in PreProd and Prod
        #  hence, the system can't distinguish the real source of the alarm
        failure_alram = cloudwatch.Alarm(self, 'FailureAlarm',
            metric = cloudwatch.Metric(
                metric_name='5XXError',
                namespace='AWS/ApiGateway',
                dimensions={
                    'ApiName': 'Gateway',
                },
                statistic='Sum',
                period=cdk.Duration.minutes(1)),
            threshold=1,
            evaluation_periods=1
        )

        codedeploy.LambdaDeploymentGroup(self, 'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_10_MINUTES,
            alarms=[failure_alram])

        self.url_output = cdk.CfnOutput(self, 'Url', value = gw.url)
