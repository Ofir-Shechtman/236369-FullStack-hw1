import os.path
from FileManager import FileManager, PDFFile
from WordCloudGenerator import WordCloudGenerator



PDFS_DIR = "pdfs"
IMAGES_DIR = "images"
INDEX_PAGE_TEMPLATE = os.path.join("templates", "index_page.txt")
PDF_PAGE_TEMPLATE = os.path.join("templates", "pdf_page.txt")


class HTMLBuilder:
    @staticmethod
    def build_index_page() -> bytes:
        pdf_files = FileManager.get_pdf_files(pdfs_dir=PDFS_DIR)
        index_page = IndexPage(INDEX_PAGE_TEMPLATE, pdf_files)
        return index_page.html

    @staticmethod
    def build_pdf_page(pdf_address) -> bytes:
        pdf_path = os.path.join(PDFS_DIR, f"{os.path.relpath(pdf_address,os.sep)}.pdf")
        pdf_file = PDFFile(path=pdf_path)
        image_path = os.path.join(IMAGES_DIR, f"{pdf_file.name_stripped}.png")
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        WordCloudGenerator.generate_wordcloud_to_file(pdf_file.path, image_path)
        pdf_page = PDFPage(PDF_PAGE_TEMPLATE, pdf_file, image_path)
        return pdf_page.html

    @staticmethod
    def build_image_page(image_address) -> bytes:
        image_address = image_address[image_address.find(IMAGES_DIR):]
        with open(image_address, 'rb') as image:
            message = image.read()
        return message


class HTMLTemplate:
    def __init__(self, template):
        with open(template, 'r') as template_file:
            self.html_page = template_file.read()

    @property
    def html(self):
        return self.html_page.encode('utf-8')


class IndexPage(HTMLTemplate):
    def __init__(self, template, pdf_files):
        super().__init__(template)
        pdf_list = ""
        for pdf_file in pdf_files:
            pdf_list += f"<li><a href={pdf_file.name_stripped}><button type=button>{pdf_file.name}</button></a></li>"
        self.html_page = self.html_page.format_map({"pdf_list": pdf_list})


class PDFPage(HTMLTemplate):
    def __init__(self, template, pdf_file, image_path):
        super().__init__(template)
        self.html_page = self.html_page.format_map({"file_name": pdf_file.name,
                                                    "image_path": image_path})


if __name__ == '__main__':
    html_builder = HTMLBuilder()
    _index_page = html_builder.build_index_page()
    print(f"{_index_page}")
    pdf_file_path = os.path.join("/file-sample_150kB")
    _pdf_page = html_builder.build_pdf_page(pdf_file_path)
    print(f"{_pdf_page}")
