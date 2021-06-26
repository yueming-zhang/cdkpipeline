#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from cdk_pipeline.pipline_stack import PiplineStack


app = cdk.App()
PiplineStack(app, 'PipelineStack', env={
    'account':'334146477851',#'804197954628'
    'region': 'us-east-1'
})

app.synth()
