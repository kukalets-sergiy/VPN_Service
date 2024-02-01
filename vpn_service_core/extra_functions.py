from PIL import Image

FILE_UPLOAD_MAX_MEMORY_SIZE = 8 * 1024 * 1024
# Can be used to resize an image
max_image_height = 128
max_image_width = 128


def reduce_image_size(image):
    try:
        # Open the image file using the PIL library
        with Image.open(image.path) as img:
            # Check if the image dimensions exceed the specified maximum values
            if img.height > max_image_height or img.width > max_image_width:
                # Calculate the new size while maintaining the aspect ratio
                output_size = (max_image_height, max_image_width)
                # Resize the image to the new dimensions
                img.thumbnail(output_size)
                # Save the resized image back to the original file path
                img.save(image.path)
    except:
        pass
