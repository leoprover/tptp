import json
from pathlib import Path
from typing import Dict

import boto3
from botocore.exceptions import ClientError


class LambdaDeploymentException(Exception):
    pass


class LambdaDeletionException(Exception):
    pass


class LambdaInvocationError(Exception):
    pass


def deployLambdaFunctionFromZip(name:str, iamRoleARN:str, handler:str, package:Path, runtime='python3.7') -> str:
    """
    Deploys a lambda function from a zip file.
    :param name: name of the AWS lambda function
    :param iamRoleARN: role in AWS IAM that is allowed to deploy a lambda function
    :param handler: handler of the lambda function, located in the zip file
    :param package: zip file containing all files and code for the lambda function
    :param runtime: the lambda environment (programming language) for executing the lambda function
    :return: The ARN of the lambda function
    """
    packageContent = package.read_bytes()
    client = boto3.client('lambda')
    try:
        response = client.create_function(
            Role = iamRoleARN,
            FunctionName = name,
            Runtime = runtime,
            Handler = handler,
            Code = {
                'ZipFile': packageContent
            }
        )
    except ClientError as e:
        raise LambdaDeploymentException(e)
    if not 'FunctionArn' in response:
        raise LambdaDeploymentException('\"FunctionArn\" is not contained in the response. ', repr(response))
    return response['FunctionArn']


def deployLambdaFunctionFromS3(name:str, iamRoleARN:str, handler:str, bucket:str, object:str, version:str=None, runtime='python3.7') -> str:
    """
    Deploys a lambda function from a zip file.
    :param name: name of the AWS lambda function
    :param iamRoleARN: role in AWS IAM that is allowed to deploy a lambda function
    :param handler: handler of the lambda function, located in the zip file
    :param bucket: S3 bucket where the zip file containing the lambda function is located
    :param object: S3 object pointing at the zip file containing the lambda function
    :param runtime: the lambda environment (programming language) for executing the lambda function
    :return: The ARN of the lambda function
    """
    client = boto3.client('lambda')
    try:
        code = {
            'S3Bucket': bucket,
            'S3Key': object,
        }
        if version:
            code['S3ObjectVersion'] = version
        response = client.create_function(
            Role = iamRoleARN,
            FunctionName = name,
            Runtime = runtime,
            Handler = handler,
            Code = code
        )
    except ClientError as e:
        raise LambdaDeploymentException(e)
    if not 'FunctionArn' in response:
        raise LambdaDeploymentException('\"FunctionArn\" is not contained in the response. ', repr(response))
    return response['FunctionArn']


def deleteLambdaFunction(lambdaArn:str) -> None:
    """
    Deletes an existing lambda function.
    :param lambdaArn: ARN of the lambda function
    :return: None
    """
    client = boto3.client('lambda')
    try:
        client.delete_function(
            FunctionName = lambdaArn
        )
    except ClientError as e:
        raise LambdaDeletionException(e)


def _invokeLambdaFunction(lambdaArn:str, parameters:Dict):
    """
    Invokes a lambda function.
    :param lambdaArn: ARN of the lambda function
    :param parameters: parameters passed to the lambda function, including HTTP method and functionID (ARN)
    :return: the response of the lambda function
    """
    client = boto3.client('lambda')
    payload = json.dumps(parameters).encode()
    try:
        response = client.invoke(
            FunctionName = lambdaArn,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=payload
        )
    except ClientError as e:
        raise LambdaInvocationError(e)
    return response


def invokeLambdaFunction(lambdaArn:str, parameters:Dict=None) -> Dict:
    """
    Invokes a lambda function. The lambda function is required to return a json response.
    :param lambdaArn: ARN of the lambda function
    :param parameters: parameters passed to the lambda function
    :return: the response of the lambda function as dictionary
    """
    payloadDict = {
        'http_verb': 'POST',
        'functionID': lambdaArn,
    }
    if parameters:
        payloadDict['parameters'] = parameters
    return json.loads(_invokeLambdaFunction(lambdaArn, payloadDict)['Payload'].read().decode('utf-8'))


"""
deployLambdaFunctionFromZip(
    'new1',
    'arn:aws:iam::378432614195:role/lambda-role',
    'test_lambda_function.lambda_handler',
    Path('/home/tg/research/tptp/tptp/tptp/utils/aws_test/test_lambda_function.zip')
)
"""

"""
deployLambdaFunctionFromS3(
    'new1',
    'arn:aws:iam::378432614195:role/lambda-role',
    'test_lambda_function.lambda_handler',
    'sdfio2a34kj',
    'test-object'
)
"""

#deleteLambdaFunction('new1')

#print(invokeLambdaFunction('arn:aws:lambda:eu-central-1:378432614195:function:function1'))


