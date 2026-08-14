import pytest
from src import Ebook

@pytest.fixture
def sample_ebook():
    return Ebook("The easy way","John Smith", "234763", "30")

def test_borrow_marks_ebook_borrowed(sample_ebook):
    sample_ebook.borrow()
    assert sample_ebook.is_borrowed is True
    
def test_borrow_twice_raises_error(sample_ebook):
    sample_ebook.borrow()
    with pytest.raises(ValueError):
        sample_ebook.borrow()

def test_setting_valid_title_update_it(sample_ebook):
    sample_ebook.title = "The new way"
    assert sample_ebook.title == "The new way"

def test_setting_empty_title_raises_error(sample_ebook):
    with pytest.raises(ValueError):
        sample_ebook.title = ""


