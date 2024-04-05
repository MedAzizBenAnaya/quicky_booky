from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Cm
from PIL import Image

# Constants for A4 size and image path
PAGE_WIDTH_CM = 21.0
PAGE_HEIGHT_CM = 29.7
COVER_IMAGE_PATH_F = 'pics/female.png'
COVER_IMAGE_PATH_M = 'pics/neutral.png'



RESIZED_COVER_PATH = "refactoredImg/new.png"  # Make sure to include the file extension

doc = Document()


def convert_image_to_pdf(image_path, pdf_path):
    image = Image.open(image_path)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(pdf_path, "PDF", resolution=300.0)


def add_text_to_image(output_path, text, gender):
    width_px = int((PAGE_WIDTH_CM / 2.54) * 300)
    height_px = int((PAGE_HEIGHT_CM / 2.54) * 300)
    if gender == "male":
        with Image.open(COVER_IMAGE_PATH_M) as img:
            img = img.resize((width_px, height_px))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype('fonts/Alike-Regular.ttf', 150, )  # Adjust the font size as needed
            except IOError:
                print("Fallback to default font")
                font = ImageFont.load_default()

            text_width = draw.textlength(text, font=font)
            text_x = (width_px - text_width) / 2
            text_y = 1250

            draw.text((text_x, text_y), text, font=font, fill="black")

            img.save(output_path)
            convert_image_to_pdf(output_path, 'coverDoc/cover.pdf')
    else:
        with Image.open(COVER_IMAGE_PATH_F) as img:
            img = img.resize((width_px, height_px))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype('fonts/OpenSans-ExtraBold.ttf', 150, )  # Adjust the font size as needed
            except IOError:
                print("Fallback to default font")
                font = ImageFont.load_default()

            text_width = draw.textlength(text, font=font)
            text_x = (width_px - text_width) / 2
            text_y = 1250

            draw.text((text_x, text_y), text, font=font, fill="black")

            img.save(output_path)
            convert_image_to_pdf(output_path, 'coverDoc/cover.pdf')

# test
# add_text_to_image(RESIZED_COVER_PATH,'MR WORLD WIDE', 'Male')
