from aws_cdk import cloud_assembly_schema, core as cdk
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .webservice_stage import WebServiceStage

class PiplineStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'Pipeline',
            cloud_assembly_artifact = cloud_assembly_artifact,
            pipeline_name='CDKPipeline',

            source_action=cpactions.GitHubSourceAction(
                action_name='GitHub',
                output=source_artifact,
                oauth_token=cdk.SecretValue.secrets_manager('mz-github-token'),
                owner='yueming-zhang',
                repo='cdkpipeline',
                trigger=cpactions.GitHubTrigger.POLL),

            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                build_command='pytest unittests',
                synth_command='cdk synth')

            )

        pre_prod_app = WebServiceStage(self, 'Pre-Prod',env={
                'account': '804197954628',#'334146477851'
                'region': 'us-east-1',
            })

        pre_prod_stage = pipeline.add_application_stage(pre_prod_app)

        # add integration test action
        pre_prod_stage.add_actions(pipelines.ShellScriptAction(
            action_name='IntegrationTest',
            run_order=pre_prod_stage.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=[
                'pip install -r requirements.txt',
                'pytest integtests',
            ],
            use_outputs={'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)}
        ))

        pipeline.add_application_stage(
            WebServiceStage(self, 'Prod',env={
                'account': '804197954628',#'334146477851'
                'region': 'us-east-1',
            })
        )        