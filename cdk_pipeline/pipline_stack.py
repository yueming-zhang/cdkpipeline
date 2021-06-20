from aws_cdk import cloud_assembly_schema, core as cdk
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

class PiplineStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipelines.CdkPipeline(self, 'Pipeline',
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
                synth_command='cdk synth')

            )