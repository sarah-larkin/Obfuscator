from input.validators import ObfuscationRequest 
import logging


class TestObfuscationRequest:

    def test_load_and_validate_json_returns_dict_if_valid(
        self, mock_input_json_for_csv_file, caplog
    ):
        #arrange
        caplog.set_level(logging.INFO)
        test_object = ObfuscationRequest(mock_input_json_for_csv_file) #initialise class

        #act
        result = test_object._load_and_validate_json(mock_input_json_for_csv_file)

        #assert
        assert result == {
            "file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",
            "pii_fields": ["Name", "Email", "Phone", "DOB"],
        }
        assert "Valid JSON and valid fields" in caplog.text
        

    # def test_validate_json_returns_dict_if_json_valid(
    #     self, mock_input_json_for_csv_file, caplog
    # ):
    #     caplog.set_level(logging.INFO)
    #     result = validate_input_json(mock_input_json_for_csv_file)
    #     assert result == {
    #         "file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",
    #         "pii_fields": ["Name", "Email", "Phone", "DOB"],
    #     }
    #     assert "Valid JSON and valid fields" in caplog.text

    # def test_TypeError_raised_if_invalid_json_string(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = ({
    #         "file_to_obfuscate":
    #         "s3://tr-nc-test-source-files/Titanic-Dataset.csv",
    #         "pii_fields": ["Name", "Sex", "Age"],
    #     })  # dict not json
    #     with pytest.raises(TypeError):
    #         validate_input_json(input_json)
    #     assert (
    #         "invalid JSON: the JSON object must be str, " ""
    #         "bytes or bytearray, not dict"
    #     ) in caplog.text

    # def test_JSONDecodeError_raised_when_json_invalid(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = (
    #         '{"file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",'
    #         '"pii_fields": ["Name", "Email", "Phone", "DOB"],}'
    #     )  # additional comma
    #     with pytest.raises(json.JSONDecodeError):
    #         validate_input_json(input_json)
    #         assert (
    #             "invalid JSON syntax: Expecting ',' delimiter"
    #             in caplog.text
    #         )

    # def test_ValueError_raised_format_not_dict(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = '["file_to_obfuscate","pii_fields"]'
    #     with pytest.raises(ValueError):
    #         validate_input_json(input_json)
    #         assert "dictionary format required" in caplog.text

    # def test_confirm_json_str_contains_specific_keys(
    #     self, mock_input_json_for_csv_file
    # ):
    #     result = validate_input_json(mock_input_json_for_csv_file)
    #     key_names = result.keys()
    #     assert list(key_names) == ["file_to_obfuscate", "pii_fields"]

    # def test_ValueError_raised_if_missing_required_key(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = '{"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
    #     with pytest.raises(ValueError):
    #         validate_input_json(input_json)
    #     assert (
    #         "missing key(s) from json str: ['file_to_obfuscate']"
    #     ) in caplog.text

    # def test_ValueError_raised_if_missing_both_required_keys(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = '{"other": "other","thing": ["Name", "Email"]}'
    #     with pytest.raises(ValueError):
    #         validate_input_json(input_json)
    #     assert (
    #         "missing key(s) from json str: " ""
    #         "['file_to_obfuscate', 'pii_fields']"
    #     ) in caplog.text

    # def test_ValueError_raised_if_file_value_type_invalid(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = (
    #         '{"file_to_obfuscate": [1,2,3],'
    #         '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
    #     )
    #     with pytest.raises(ValueError):
    #         validate_input_json(input_json)
    #     assert "file_to_obfuscate must have a string value" in caplog.text

    # def test_valueError_raised_if_fieds_value_type_invalid(self, caplog):
    #     caplog.set_level(logging.ERROR)
    #     input_json = (
    #         '{"file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",'
    #         '"pii_fields": "Name"}'
    #     )
    #     with pytest.raises(ValueError):
    #         validate_input_json(input_json)
    #     assert "pii_fields must contain a list" in caplog.text