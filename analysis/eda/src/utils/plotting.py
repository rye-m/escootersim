from PIL import Image
from io import BytesIO
from base64 import b64encode

def image_to_altair(image_path, outfile=None):
    pil_image = Image.open(image_path)
    output = BytesIO()
    pil_image.save(output, format='PNG')
    b64_image = "data:image/png;base64," + b64encode(output.getvalue()).decode()
    if outfile:
        with open(outfile, 'w') as f:
            f.write(b64_image)
    return b64_image