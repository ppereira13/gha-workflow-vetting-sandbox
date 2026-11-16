from sample_app.masking import mask_secret


def test_keeps_last_four_characters():
    assert mask_secret("ghp_abcdef123456") == "************3456"

def test_short_values_are_fully_hidden():
    assert mask_secret("abc") == "***"