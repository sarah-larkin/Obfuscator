import logging
import boto3
from botocore.exceptions import ClientError

# connect to external sources (whatever they may be)
# this case AWS / boto3 

# get_file()

class S3Client: 
    def __init__(self): 
        self.s3 = boto3.client("s3")
  
    def download_file(self, bucket, key):    
        try:
            file_object = self.s3.get_object(bucket=bucket, Key=key)  # returns dict -> ["Body"]=streaming object
            data_bytes = file_object["Body"].read() # body can only be read once, .read() returns bytes (reusable)
            logging.info("file retrieved")
            return data_bytes

        except ClientError as err:
            error_code = err.response["Error"]["Code"]
            error_msg = err.response["Error"]["Message"]

            logging.error(f"for s3://{bucket}/{key} -> {error_code} : {error_msg}")
            raise err
    
    def upload_file(self): 
        pass



