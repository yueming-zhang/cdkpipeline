from aws_cdk import core as cdk
from cdk_pipeline.demoapp_stack import DemoAppStack

def test_lambda_handler():
    # GIVEN
    app = cdk.App()

    #WHEN
    DemoAppStack(app, 'Stack')

    # THEN
    template = app.synth().get_stack_by_name('Stack').template
    functions = [resource for resource in template['Resources'].values()
                 if resource['Type'] == 'AWS::Lambda::Function']

    assert len(functions) == 1
    assert functions[0]['Properties']['Handler'] == 'handler.handler'