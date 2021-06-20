from os import path
from aws_cdk import core as cdk
#from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw

class DemoAppStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        handler = lmb.Function(self, 'Handler',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')) #TODO: code=_lambda.Code.asset('lambda'),
            )

        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service to test CDKPipeline',
            handler=handler.current_version)

        self.url_output = cdk.CfnOutput(self, 'Url', value = gw.url)
