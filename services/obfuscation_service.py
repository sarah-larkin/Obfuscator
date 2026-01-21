from input.validators import ObfuscationRequest
from infrastructure.s3_client import S3Client
import time

#orchestration

#obfuscator()

#creating the structure
class ObfuscationService:
    def __init__(self, s3_client: S3Client): 
        self.s3_client = s3_client #calling in from infra/s3_client.py

    def run(self, request: ObfuscationRequest):
        #get file using request.file_details
        bucket = request.file_details["Bucket"]
        key = request.file_details["Key"]
        data_bytes = self.s3_client.download_file(bucket, key) 
        
        #convert to df
        df = self.parse(request.file_details, data_bytes) # TODO: write parse code 
        
        #obfuscate using request.fields
        obf_df = self.obfuscate(df, request.fields) # TODO: write obfuscate code
        
        #output 
        self.write_output(df) # TODO: write write_output code






