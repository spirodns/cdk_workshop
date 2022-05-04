from nturl2path import url2pathname
from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from .hitcounter import HitCounter
from cdk_dynamo_table_view import TableViewer


class CdkWorkshopStack(Stack):

    @property
    def hc_endpoint(self):
        return self._hc_endpoint
    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Define and AWS LAmbda resoource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda
        )
        gateway = apigw.LambdaRestApi(
            self,'Endpoint',
            handler=hello_with_counter._handler
        )

        tv = TableViewer(
            self,'ViewHitCounter',
            title='HelloHits',
            table=hello_with_counter.table
        )
        self._hc_endpoint = CfnOutput(
            self,'GatewayUrl',
            value = gateway.url
        )
        self._hc_viewer_url = CfnOutput(
            self, 'TableViewerUrl',
            value=tv.endpoint
        )


