import os.path

from FileManager import FileManager, PDFFile
from WordCloudGenerator import WordCloudGenerator

PDFS_DIR = "pdfs"
IMAGES_DIR = "images"
INDEX_PAGE_TEMPLATE = os.path.join("templates", "index_page.txt")
PDF_PAGE_TEMPLATE = os.path.join("templates", "pdf_page.txt")


class HTMLBuilder:
    def __init__(self, address):
        self.address = address

    def build_index_page(self) -> str:
        pdf_files = FileManager.get_pdf_files(pdfs_dir=PDFS_DIR)
        index_page = IndexPage(self.address, INDEX_PAGE_TEMPLATE, pdf_files)
        return index_page.html

    def build_pdf_page(self, pdf_address) -> str:
        pdf_path = os.path.join(PDFS_DIR, f"{os.path.basename(pdf_address)}.pdf")
        pdf_file = PDFFile(path=pdf_path)
        image_path = os.path.join(IMAGES_DIR, f"{pdf_file.name_stripped}.png")
        WordCloudGenerator.generate_wordcloud_to_file(pdf_file.path, image_path)
        pdf_page = PDFPage(self.address, PDF_PAGE_TEMPLATE, pdf_file, image_path)
        return pdf_page.html


class HTMLTemplate:
    def __init__(self, address, template):
        with open(template, 'r') as template_file:
            self.html_page = template_file.read()
            self.address = address

    @property
    def html(self):
        return self.html_page


class IndexPage(HTMLTemplate):
    def __init__(self, address, template, pdf_files):
        super().__init__(address, template)
        pdf_list = ""
        for pdf_file in pdf_files:
            pdf_file_address = os.path.join(self.address, pdf_file.name_stripped)
            pdf_list += f"\t<li><form action=\"{pdf_file_address}\"><input type=\"submit\" value=\"{pdf_file.name}\" /></form></li>\n"
        self.html_page = self.html_page.format_map({"pdf_list": pdf_list})


class PDFPage(HTMLTemplate):
    def __init__(self, address, template, pdf_file, image_path):
        super().__init__(address, template)
        self.html_page = self.html_page.format_map({"file_name": pdf_file.name,
                                                    "image_path": os.path.join(self.address, image_path)})


if __name__ == '__main__':
    address = "127.0.0.1:8888"
    html_builder = HTMLBuilder(address="127.0.0.1:8888")
    _index_page = html_builder.build_index_page()
    print(f"{_index_page}")
    pdf_file_path = os.path.join(address, "file-sample_150kB")
    _pdf_page = html_builder.build_pdf_page(pdf_file_path)
    print(f"{_pdf_page}")
