from pathlib import Path
from organizer.organizer_engine import create_base_structure, save_files
from organizer.zip_builder import create_zip
from io import BytesIO

class DummyUpload:
    """Simple stand-in for UploadFile used in tests."""
    def __init__(self, filename, data=b"test"):
        self.filename = filename
        self.file = BytesIO(data)

def test_create_base_structure(tmp_path):
    create_base_structure(tmp_path)
    expected = ["Code", "Documents", "Media", "Data", "Notes", "Misc"]

    for folder in expected:
        assert (tmp_path / folder).exists()

def test_save_files(tmp_path):
    create_base_structure(tmp_path)

    files = [
        DummyUpload("script.py"),
        DummyUpload("doc.pdf"),
        DummyUpload("image.png"),
        DummyUpload("data.csv"),
        DummyUpload("meeting.note"),
        DummyUpload("other.xyz")
    ]

    save_files(tmp_path, files)

    assert (tmp_path / "Code" / "script.py").exists()
    assert (tmp_path / "Documents" / "doc.pdf").exists()
    assert (tmp_path / "Media" / "image.png").exists()
    assert (tmp_path / "Data" / "data.csv").exists()
    assert (tmp_path / "Notes" / "meeting.note").exists()
    assert (tmp_path / "Misc" / "other.xyz").exists()

def test_create_zip(tmp_path):
    # create folders and files
    create_base_structure(tmp_path)
    (tmp_path / "Code" / "test.py").write_text("print('hello')")

    zip_path = tmp_path / "output.zip"
    create_zip(tmp_path, zip_path)

    assert zip_path.exists()
    assert zip_path.stat().st_size > 0
