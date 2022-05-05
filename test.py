import pytest

from main import _get_ninjable_content, _sanitize_message


def test_ninjable_content_full_first_matching_word_should_return_word():
    ninjable_content  = _get_ninjable_content("un pepino el")
    assert 'pepino' == ninjable_content


@pytest.mark.falla
def test_ninjable_content_not_full_matching_word_should_not_return_word():
    ninjable_content = _get_ninjable_content("un pepinoite el")
    assert None == ninjable_content

def test_ninjable_content_dot_first_matching_word_should_return_word():
    ninjable_content  = _get_ninjable_content("un.pepino el")
    assert 'pepino' == ninjable_content

def test_sanitize_message():
    result = _sanitize_message('. , ,pepinoite.')

    assert 'pepinoite' == result


