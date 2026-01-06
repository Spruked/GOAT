from organizer.file_classifier import classify_file
from fastapi import UploadFile
from io import BytesIO

class DummyUpload:
    """Simple stand-in object for UploadFile used in tests."""
    def __init__(self, filename):
        self.filename = filename
        self.file = BytesIO(b"test data")

def test_classifier_code():
    f = DummyUpload("example.py")
    assert classify_file(f) == "Code"

def test_classifier_documents():
    f = DummyUpload("notes.pdf")
    assert classify_file(f) == "Documents"

def test_classifier_media():
    f = DummyUpload("image.png")
    assert classify_file(f) == "Media"

def test_classifier_data():
    f = DummyUpload("sheet.csv")
    assert classify_file(f) == "Data"

def test_classifier_notes():
    f = DummyUpload("meeting.note")
    assert classify_file(f) == "Notes"

def test_classifier_misc():
    f = DummyUpload("unknown.xyz")
    assert classify_file(f) == "Misc"
