import json
import logging
from urllib.parse import urlparse

#entry point/boundary 
#interpret and validate input 

#class to incorporate: 
# validate_input_json()
# extract_file_location()
# extract_fields_to_alter()

#validated request object 
class ObfuscationRequest: 
    def __init__(self, input_json):
        verified_input = self._load_and_validate_json(input_json) # temp, not state, do not store this process 

        self.__file_details = self._extract_and_validate_file_details(verified_input)
        self.__fields = self._extract_and_validate_fields(verified_input)

    def _load_and_validate_json(self, input_json): 
        try:
            data = json.loads(input_json)

        # if not valid json string:
        except TypeError as err:
            logging.error(f"invalid JSON: {err}")
            raise

        # invalid json syntax
        except json.JSONDecodeError as err:
            logging.error(f"invalid JSON syntax: {err}")
            raise

        # invalid output format
        if not isinstance(data, dict):
            logging.error("dictionary format required")
            raise ValueError("dictionary format required")

        # missing required output keys
        expected_keys = ["file_to_obfuscate", "pii_fields"]
        input_keys = list(data.keys())

        missing_keys = [
            field for field in expected_keys if field not in input_keys
        ]

        if missing_keys:
            logging.error(f"missing key(s) from json str: {missing_keys}")
            raise ValueError(f"missing key(s) from json str: {missing_keys}")

        # invalid output values format
        if not isinstance(data["file_to_obfuscate"], str):
            logging.error("file_to_obfuscate must have a string value")
            raise ValueError("file_to_obfuscate must have a string value")

        if not isinstance(data["pii_fields"], list):
            logging.error("pii_fields must contain a list")
            raise ValueError("pii_fields must contain a list")

        # valid output
        logging.info("Valid JSON and valid fields")
        return data

    def _extract_and_validate_file_details(self, verified_input): 
        permitted_file_types = ["csv", "json"]  # update here for extension
        permitted_scheme = ["s3"] # update here if scope grows

        url = verified_input["file_to_obfuscate"]

        o = urlparse(url)

        scheme = o.scheme
        bucket = o.netloc
        key = o.path.lstrip("/")  # file_path/file_name (with first / removed)
        file_name = key.split("/")[-1]
        file_type = file_name.split(".")[-1]

        if len(url) == 0:
            logging.error("no URL")
            raise ValueError("no URL")

        if scheme not in permitted_scheme:
            logging.error("URL does not contain permitted file location")
            raise ValueError("URL does not contain permitted file location")

        if not file_name or "." not in file_name:
            file_type = None
            logging.error("unable to confirm file type")
            raise ValueError("unable to confirm file type")

        if file_type not in permitted_file_types:
            logging.error(f"unable to process {file_type} files")
            raise ValueError(f"unable to process {file_type} files")

        file_details = {
            "Scheme": scheme,
            "Bucket": bucket,
            "Key": key,
            "File_Name": file_name,
            "File_Type": file_type,
        }

        return file_details

    def _extract_and_validate_fields(self, verified_input):

        fields = verified_input["pii_fields"]

        if len(fields) == 0:
            logging.error("no fields to obfuscate provided")
            raise ValueError("no fields to obfuscate provided")

        invalid_fields = (
            [heading for heading in fields if not isinstance(heading, str)]
        )

        if invalid_fields:
            logging.error(f"The headings : {invalid_fields} are not strings")
            raise TypeError(f"The headings : {invalid_fields} are not strings")

        logging.info("pii fields extracted")
        return fields
     
    


