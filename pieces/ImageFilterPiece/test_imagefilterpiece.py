from domino.testing import piece_dry_run
from pathlib import Path
from PIL import Image
from io import BytesIO
import base64


# Open test image and convert to base64 string using Pillow
img_path = str(Path(__file__).parent / "test_image.png")
img = Image.open(img_path)
buffered = BytesIO()
img.save(buffered, format="PNG")
image_bytes = buffered.getvalue()
base64_image = base64.b64encode(image_bytes).decode("utf-8")


def test_imagefilterpiece():
    input_data = dict(
        input_image=[base64_image],
        sepia=True,
        blue=True,
        output_type="both"
    )
    piece_output = piece_dry_run(
        piece_name="ImageFilterPiece",
        input_data=input_data
    )
    assert piece_output is not None
    assert isinstance(piece_output.get('image_file_path'), list)
    assert piece_output['image_file_path'][0].endswith('.png')


def test_imagefilterpiece_list_of_images():
    input_data = dict(
        input_image=[base64_image, base64_image, base64_image],
        sepia=True,
        output_type="both"
    )
    piece_output = piece_dry_run(
        piece_name="ImageFilterPiece",
        input_data=input_data
    )
    assert piece_output is not None
    assert len(piece_output['image_file_path']) == 3
    assert len(piece_output['image_base64_string']) == 3
    for path in piece_output['image_file_path']:
        assert path.endswith('.png')
    for b64 in piece_output['image_base64_string']:
        assert len(b64) > 0


def test_imagefilterpiece_skips_empty_entries():
    input_data = dict(
        input_image=[base64_image, "", base64_image],
        sepia=True,
        output_type="both"
    )
    piece_output = piece_dry_run(
        piece_name="ImageFilterPiece",
        input_data=input_data
    )
    assert len(piece_output['image_file_path']) == 3
    assert piece_output['image_file_path'][0].endswith('.png')
    assert piece_output['image_file_path'][1] == ""
    assert piece_output['image_file_path'][2].endswith('.png')
