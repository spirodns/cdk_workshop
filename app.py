#!/usr/bin/env python3

import aws_cdk as cdk

# from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack


# app = cdk.App()
# CdkWorkshopStack(app, "cdk-workshop")
from cdk_workshop.pipeline_stack import WorkshopPipelineStack


# app = cdk.App()
# CdkWorkshopStack(app, "cdk-workshop")
app = cdk.App()
WorkshopPipelineStack(app, "WorkshopPipelineStackBySpiroDanousis")

app.synth()
