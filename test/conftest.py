import pytest


# csv fixutres
@pytest.fixture(scope="function")
def mock_input_json_for_csv_file():
    """mocked input json string for a csv file"""
    mock_csv_json = (
        '{"file_to_obfuscate": "s3://test_bucket_TR_NC/test_file.csv",'
        '"pii_fields": ["Name", "Email", "Phone", "DOB"]}'
    )
    return mock_csv_json