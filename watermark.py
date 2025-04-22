from PIL import Image

def add_watermark(image_path, watermark_path="logo.png"):
    base_image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")
    watermark = watermark.resize((150, 150))

    base_image.paste(watermark, (10, 10), watermark)
    output_path = image_path.replace(".jpg", "_wm.jpg")
    base_image.save(output_path)
    return output_path
