from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines
)
# from cdk_workshop.pipeline_stage import WorkshopPipelineStage

class WorkshopPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id,**kwargs)

        #Creates a CodeCommit repository called 'WorkshopRepo'
        repo =  codecommit.Repository(
            self, 'WorkshopRepo',
            repository_name="WorkshopRepo"
        )
        pipeline = pipelines.CodePipeline(
            self,
            "WorkshopPipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo,"master"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "npx cdk synth",
                ]
            )
        )
