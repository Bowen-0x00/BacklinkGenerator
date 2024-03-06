from io import BytesIO
import base64

def image_to_base64(image):
    if isinstance(image, bytes):
        encoded_string = base64.b64encode(image)
        return f'data:image/png:base64,{encoded_string.decode("utf-8")}'
    else:
        with BytesIO() as byte_stream:
            image.save(byte_stream, format="PNG")
            byte_stream.seek(0)
            encoded_string = base64.b64encode(byte_stream.read())
            return f'data:image/png:base64,{encoded_string.decode("utf-8")}'
# def image_to_base64(image):
#     with BytesIO() as byte_stream:
#         image.save(byte_stream, format="PNG")
#         byte_stream.seek(0)
#         encoded_string = base64.b64encode(byte_stream.read())
#         return f'data:image/png:base64,{encoded_string.decode("utf-8")}'
    