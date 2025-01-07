from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Cm
from io import BytesIO


class CoverFormulation:
    PAGE_WIDTH_CM = 21.0
    PAGE_HEIGHT_CM = 29.7
    COVER_IMAGE_PATH_F = 'pics/female.png'
    COVER_IMAGE_PATH_M = 'pics/neutral.png'

    def __init__(self, document: Document(),  title: str, author: str, gender, font_paths=None, file_name="book_cover.docx"):
        """
        Initializes the CoverFormulation class.


        :param title: Title of the book.
        :param author: Author of the book.
        :param gender: Gender for selecting the appropriate cover image.
        :param font_paths: Dictionary with font paths (optional).
        :param file_name: Path for saving the output DOCX file.
        """

        self.title = title
        self.author = author
        self.gender = gender
        self.output_docx = file_name
        self.font_paths = font_paths or {
            'title_font': 'fonts/Alike-Regular.ttf',
            'author_font': 'fonts/OpenSans-Regular.ttf',
        }
        self.document = document

    def _create_cover_image(self):
        """
        Creates a cover image with text overlay.
        :return: BytesIO object containing the image.
        """
        width_px = int((self.PAGE_WIDTH_CM / 2.54) * 300)  # Convert cm to pixels
        height_px = int((self.PAGE_HEIGHT_CM / 2.54) * 300)

        # Select the appropriate cover image based on gender
        cover_path = self.COVER_IMAGE_PATH_M if self.gender.lower() == "male" else self.COVER_IMAGE_PATH_F

        with Image.open(cover_path) as img:
            img = img.resize((width_px, height_px))
            draw = ImageDraw.Draw(img)

            try:
                title_font = ImageFont.truetype(self.font_paths['title_font'], 100)  # Font for title
                author_font = ImageFont.truetype(self.font_paths['author_font'], 60)  # Font for author
            except IOError:
                print("Fallback to default font")
                title_font = author_font = ImageFont.load_default()

            # Calculate positions for the text
            title_width = draw.textlength(self.title, font=title_font)
            title_x = (width_px - title_width) / 2
            title_y = int(height_px * 0.4)  # Title positioned at 40% height

            author_width = draw.textlength(self.author, font=author_font)
            author_x = (width_px - author_width) / 2
            author_y = int(height_px * 0.5)  # Author positioned at 50% height

            # Draw the text on the image
            draw.text((title_x, title_y), self.title, font=title_font, fill="black")
            draw.text((author_x, author_y), self.author, font=author_font, fill="gray")

            # Save the modified image to a BytesIO object
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)  # Reset the pointer to the beginning of the BytesIO object

            return img_bytes

    def add_cover(self):
        cover_image= self._create_cover_image()
        self.document.add_picture(cover_image, width=Cm(self.PAGE_WIDTH_CM), height=Cm(self.PAGE_HEIGHT_CM))



