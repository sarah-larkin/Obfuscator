from input.validators import ObfuscationRequest
import time

#orchestration

#obfuscator()

#creating the structure
class ObfuscationService:
    def run(self, request: ObfuscationRequest):
        #get file using request.file_details
        file = self.load_file(request.file_details) # TODO write load_file code 
        #convert to df
        df = self.parse(file) # TODO: write parse code 
        #obfuscate using request.fields
        df = self.obfuscate(df, request.fields) # TODO: write obfuscate code
        #output 
        self.write_output(df) # TODO: write write_output code






