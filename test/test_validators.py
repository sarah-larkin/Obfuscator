from input.validators import ObfuscationRequest 
import logging
import pytest
import json

#testing happy path
class TestObfuscationRequestCsv:
    def test_ObfuscationRequest_returns_details_and_fields(
        self, mock_input_json_for_csv_file, caplog):

        caplog.set_level(logging.INFO)

        request = ObfuscationRequest(mock_input_json_for_csv_file) #initialise class

        assert isinstance(request.file_details, dict)
        assert request.file_details == {
        "Scheme": "s3",
        "Bucket": "test_bucket",
        "Key": "test_file.csv",
        "File_Name": "test_file.csv",
        "File_Type": "csv"}

        assert request.fields == ["Name", "Email", "Phone", "DOB"]

        #logging only - note: will break if you change msg (potential to remove)
        assert "Valid JSON and valid fields" in caplog.text
        assert "file details extracted" in caplog.text
        assert "pii fields extracted" in caplog.text

    def test_ObfuscationRequest_accepts_longer_file_path(self):
        input_json =(
        '{"file_to_obfuscate": "s3://test_bucket_TR_NC/outer_folder/inner_folder/test_file.csv",'
        '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
        )
        
        request = ObfuscationRequest(input_json)
        
        assert request.file_details == {
            "Scheme": "s3",
            "Bucket": "test_bucket_TR_NC",
            "Key": "outer_folder/inner_folder/test_file.csv",
            "File_Name": "test_file.csv",
            "File_Type": "csv",
        }

        assert request.fields == ["Name", "Email", "Phone", "DOB"]


class TestExceptionsForLoadAndValidateJSON:
    #testing error handling
    def test_TypeError_raised_for_invalid_json_string(self, caplog):
        caplog.set_level(logging.ERROR)
        input_json = ({
            "file_to_obfuscate":
            "s3://tr-nc-test-source-files/Titanic-Dataset.csv",
            "pii_fields": ["Name", "Sex", "Age"],
        })  # dict not json

        with pytest.raises(TypeError):
            ObfuscationRequest(input_json)

        assert (
            "invalid input JSON type:"
        ) in caplog.text

    def test_JSONDecodeError_raised_when_json_invalid(self, caplog):
        caplog.set_level(logging.ERROR)

        input_json = (
            '{"file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",'
            '"pii_fields": ["Name", "Email", "Phone", "DOB"],}'
        )  # additional comma

        with pytest.raises(json.JSONDecodeError):
            ObfuscationRequest(input_json)
        
        assert "invalid JSON syntax:" in caplog.text

    def test_ValueError_raised_format_not_dict(self, caplog):
        caplog.set_level(logging.ERROR)
        input_json = '["file_to_obfuscate","pii_fields"]'

        with pytest.raises(ValueError):
            ObfuscationRequest(input_json)
        
        assert "dictionary format required" in caplog.text

    def test_ValueError_raised_if_missing_required_key(self, caplog):
        caplog.set_level(logging.ERROR)
        
        input_json = '{"pii_fields": ["Name", "Email", "Phone", "DOB"]}'

        with pytest.raises(ValueError):
            ObfuscationRequest(input_json)
        assert (
            "missing key(s) from json str: ['file_to_obfuscate']"
        ) in caplog.text

    def test_ValueError_raised_if_missing_both_required_keys(self, caplog):
        caplog.set_level(logging.ERROR)
        input_json = '{"other": "other","thing": ["Name", "Email"]}'
        with pytest.raises(ValueError):
            ObfuscationRequest(input_json)
        assert (
            "missing key(s) from json str: " ""
            "['file_to_obfuscate', 'pii_fields']"
        ) in caplog.text

    def test_ValueError_raised_if_file_value_type_invalid(self, caplog):
        caplog.set_level(logging.ERROR)
        input_json = (
            '{"file_to_obfuscate": [1,2,3],'
            '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
        )
        with pytest.raises(ValueError):
            ObfuscationRequest(input_json)
        assert "file_to_obfuscate must have a string value" in caplog.text


    def test_valueError_raised_if_fields_value_type_invalid(self, caplog):
        caplog.set_level(logging.ERROR)
        input_json = (
            '{"file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",'
            '"pii_fields": "Name"}'
        )
        with pytest.raises(ValueError):
            ObfuscationRequest(input_json)
        assert "pii_fields must contain a list" in caplog.text



class TestExceptionsForExtractAndValidateFileDetails:
    def test_ValueError_raised_if_URL_is_empty_string(self, caplog):
        caplog.set_level(logging.ERROR)
        with pytest.raises(ValueError):
            ObfuscationRequest(
                '{"file_to_obfuscate": "",'
                '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
            )
        assert "no URL" in caplog.text

    def test_ValueError_raised_if_not_valid_s3_url(self, caplog):
        caplog.set_level(logging.ERROR)
        with pytest.raises(ValueError):
            # missing s3://
            ObfuscationRequest(
                '{"file_to_obfuscate":"HTTPS://test_bucket_TR_NC/test_file.csv",'
                '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
            )
        assert "URL does not contain permitted file location" in caplog.text

    def test_url_raises_and_logs_error_invalid_file_type(self, caplog):
        caplog.set_level(logging.ERROR)
        with pytest.raises(ValueError):
            # no file extension
            ObfuscationRequest(
                '{"file_to_obfuscate": "s3://test_bucket_TR_NC/test_file",'
                    '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
            )
        assert "unable to confirm file type" in caplog.text

#     def test_raises_and_logs_error_if_not_accepted_file_type(self, caplog):
#         caplog.set_level(logging.ERROR)
#         file_path = "s3://test_bucket_TR_NC/test_file.pdf"
#         with pytest.raises(ValueError):
#             extract_file_location_details(
#                 {
#                     "file_to_obfuscate": file_path,
#                     "pii_fields": ["Name", "Email", "Phone", "DOB"],
#                 }
#             )
#         assert "unable to process pdf files" in caplog.text

class TestExceptionsForExtractAndValidateFields:
    pass

    # check you have tests for 
    #invalid s3 URL 
    #invalid pii fields
