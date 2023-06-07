from typing import Union
from io import BytesIO

from qrcode import QRCode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


def generate_qrcode(payload: Union[int, str]):
    if isinstance(payload, int):
        payload = f'{payload}'

    qr = QRCode()
    qr.add_data(payload)
    qr = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask()
    )
    image = BytesIO()
    qr.save(image)
    image.seek(0)
    return image.getvalue()
