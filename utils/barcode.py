from io import BytesIO
from typing import Union

from barcode import Code128
from barcode.writer import ImageWriter


def generate_barcode(payload: Union[str, int]):
    if isinstance(payload, int):
        payload = f'{payload}'

    img = BytesIO()
    Code128(payload, writer=ImageWriter()).write(img)
    img.seek(0)
    return img.getvalue()
