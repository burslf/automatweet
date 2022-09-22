import boto3
import json

# boto3.setup_default_session(profile_name='personal')

def get_s3_json_file(
    bucket_name, 
    file_name
):
    s3 = boto3.resource('s3')
    
    try:
        content_object = s3.Object(bucket_name, file_name)
    
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
    
        return json_content
    
    except Exception:
        return None


def add_json_file_to_s3(
    bucket_name, 
    file_name, 
    json_data
):
    s3 = boto3.resource('s3')

    try:
        s3object = s3.Object(bucket_name, f"{file_name}.json")

        s3object.put(
            Body=(bytes(json.dumps(json_data).encode('UTF-8')))
        )

    except Exception as e:
        raise e