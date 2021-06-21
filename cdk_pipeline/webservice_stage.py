from aws_cdk import core as cdk
from constructs import Construct

from .demoapp_stack import DemoAppStack

class WebServiceStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = DemoAppStack(self, 'WebService')
        self.url_output = service.url_output

        
