# import aws_cdk as core
# import aws_cdk.assertions as assertions
# from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack


# def test_sqs_queue_created():
#     app = core.App()
#     stack = CdkWorkshopStack(app, "cdk-workshop")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })


# def test_sns_topic_created():
#     app = core.App()
#     stack = CdkWorkshopStack(app, "cdk-workshop")
#     template = assertions.Template.from_stack(stack)

#     template.resource_count_is("AWS::SNS::Topic", 1)
from inspect import stack
from re import template
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    assertions
)
from cdk_workshop.hitcounter import HitCounter
import pytest

def test_dynamodb_table_created():
    stack = Stack()
    HitCounter(stack, "HitCounter",
    downstream=_lambda.Function(stack,"TestFunction", 
    runtime=_lambda.Runtime.NODEJS_14_X,
    handler='hello.handler',
    code=_lambda.Code.from_asset('lambda')),
    )
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table",1)

def test_dynamodb_with_encryption():
    stack = Stack()
    HitCounter(stack, "HitCounter",
            downstream=_lambda.Function(stack, "TestFunction",
                runtime=_lambda.Runtime.NODEJS_14_X,
                handler='hello.handler',
                code=_lambda.Code.from_asset('lambda')))

    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::DynamoDB::Table", {
        "SSESpecification": {
            "SSEEnabled": True,
            },
        })



def test_lambda_has_env_vars():
    stack = Stack()
    HitCounter(stack, "HitCounter",
    downstream=_lambda.Function(stack,"TestFunction", 
    runtime=_lambda.Runtime.NODEJS_14_X,
    handler='hello.handler',
    code=_lambda.Code.from_asset('lambda')),
    )
    template = assertions.Template.from_stack(stack)
    envCapture = assertions.Capture()

    template.has_resource_properties("AWS::Lambda::Function",
    {
        "Handler": "hitcount.handler",
        "Environment": envCapture,
    })
    assert envCapture.as_object() == {
            "Variables": {
                "DOWNSTREAM_FUNCTION_NAME": {"Ref": "TestFunction22AD90FC"},
                "HITS_TABLE_NAME": {"Ref": "HitCounterHits079767E5"},
                },
    }