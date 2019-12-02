import json
import os
import io
import boto3
import csv
import array

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    payload = event['query']['data']
    payload = payload.encode()
    payload = io.BytesIO(payload)
    payload = payload.getvalue().decode().rstrip()
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)
    print(response)
    result = json.loads(response['Body'].read().decode())
    test_pred =result['instances'][0]['features']
    instances = []
    instances.append({"predicted_label": test_pred})
    json_output = {"predictions": instances}
    response = json.dumps(json_output)
    result = json.loads(response)
    
    return result
