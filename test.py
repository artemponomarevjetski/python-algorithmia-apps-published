from . import extract_email_address

def test_extract_email_address():
    assert extract_email_address.apply("Jane") == "hello Jane"
