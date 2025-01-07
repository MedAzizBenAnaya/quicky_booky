from docx2pdf import convert
import PyPDF2
from docx import Document

import time

from back.ebookgenV1.app.formulation.content_formulator import ContentFormulation
from back.ebookgenV1.app.formulation.cover_formulator import CoverFormulation
from back.ebookgenV1.app.generation.content_generator import ContentGenerator

#TODO fix this shit
img_doc_path = "coverDoc/cover.pdf"
pdf_path = "pdf/myEbook.pdf"

def generate_file_path():
    current_time = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"ebook_{current_time}.pdf"
    return f'generated_books/{file_name}'

def combine_pdfs(pdf_path1, pdf_path2, output_path):
    pdf_reader1 = PyPDF2.PdfReader(pdf_path1)
    pdf_reader2 = PyPDF2.PdfReader(pdf_path2)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(len(pdf_reader1.pages)):
        pdf_writer.add_page(pdf_reader1.pages[page_num])

    for page_num in range(len(pdf_reader2.pages)):
        pdf_writer.add_page(pdf_reader2.pages[page_num])

    with open(output_path, 'wb') as out_pdf_file:
        pdf_writer.write(out_pdf_file)


#creating book file
book = Document()

#generating book content
book_content = ContentGenerator()
book_content.generate_outline()
book_content.generate_chapters_content()


# adding cover
cover = CoverFormulation(book)
cover.add_cover()

# formating content
content = ContentFormulation(book, book_content.book_info )
content.setup_document_layout()
content.add_cover_page()
content.add_description_page()
content.add_table_of_contents()
content.add_content(book_content.content_array) # add content here
content.add_summary()
content.add_sources()

filename = 'whatever'
doc_path = f"docs/{filename}.docx"
book.save(doc_path)
convert(doc_path, pdf_path)




def create_ebook(filename, book_title, book_info, content_array, gender):
    path = generate_file_path()
    add_text_to_image(RESIZED_COVER_PATH, book_title, gender)
    create_word_book(book_info, content_array, filename)
    combine_pdfs(img_doc_path, pdf_path, path)

    return path