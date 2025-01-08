from PIL.ImageFont import truetype
from docx2pdf import convert
import PyPDF2
import tempfile
from docx import Document

import time

from back.ebookgenV1.app.formulation.content_formulator import ContentFormulation
from back.ebookgenV1.app.formulation.cover_formulator import CoverFormulation
from back.ebookgenV1.app.generation.content_generator import ContentGenerator

#TODO fix this shit


class AssBook:

    def __init__(self,title, topic, language, age, gender, extra_info, n_chapters, n_subsections):
        # creating book file
        self.book = Document()

        self.title, self.topic, self.language, self.age, self.gender, self.extra_info, self.n_chapters, self.n_subsections = (
            title, topic, language, age, gender, extra_info, n_chapters, n_subsections)


    async def assemble_book(self):
        # adding cover
        cover = CoverFormulation(self.book)
        cover.add_cover()

        #generating book content
        book_content = ContentGenerator()
        book_content.generate_outline()
        book_content.generate_chapters_content()

        # formating content
        content = ContentFormulation(self, book_content.book_info )
        content.setup_document_layout()
        content.add_cover_page()
        content.add_description_page()
        content.add_table_of_contents()
        content.add_content(book_content.content_array) # add content here
        content.add_summary()
        content.add_sources()

        self.book.save()

    # async def save(self):
    #     return


    async def save_and_convert(self):
        current_time = time.strftime("%Y%m%d-%H%M%S")

        convert(self.book.save(), f'generated_books/{self.title}_ebook_{current_time}.pdf')











