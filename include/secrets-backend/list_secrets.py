import boto3
import json

client = boto3.client('secretsmanager')

response = client.list_secrets(
    IncludePlannedDeletion=True|False,
    MaxResults=123,
    NextToken='string',
    Filters=[
        {
            'Key': 'description'|'name'|'tag-key'|'tag-value'|'primary-region'|'owning-service'|'all',
            'Values': [
                'string',
            ]
        },
    ],
    SortOrder='asc'|'desc'
)

print(json.dumps(response,indent=2))

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/list_secrets.html#SecretsManager.Client.list_secrets
