from meraki_subnets import check, get_api_key

def test():
    assert "hello" == "hello"

def test_meraki_subnet():
    assert check() == True

def empty_api_key_fails():
    if not get_api_key():
        thing = 1234
        assert thing == "raise exception"