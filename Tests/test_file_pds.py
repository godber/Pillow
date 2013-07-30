from tester import assert_equal

from PIL import Image

SAMPLE_FILE = "Images/sample_PDS.IMG"


def test_sanity():
    """Basic Open Test"""
    img = Image.open(SAMPLE_FILE)
    img.load()
    assert_equal(img.mode, "RGB")
    assert_equal(img.size, (128, 128))
    assert_equal(img.format, "PPM")
