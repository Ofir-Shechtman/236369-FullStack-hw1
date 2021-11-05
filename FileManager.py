from typing import Tuple
import os


class PDFFile:
    def __init__(self, path):
        if not (path.endswith(".pdf") and os.path.exists(path)):
            raise Exception("no pdf")
        self._path = path
        self._name = os.path.basename(path)
        self._name_stripped = self._name.split(".pdf")[0]

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def name_stripped(self):
        return self._name_stripped


class FileManager:
    @staticmethod
    def get_pdf_files(pdfs_dir) -> Tuple[PDFFile]:
        return tuple([PDFFile(os.path.join(pdfs_dir, file)) for file in os.listdir(pdfs_dir) if file.endswith(".pdf")])

    @staticmethod
    def exists(path) -> bool:
        return os.path.exists(path) and path.endswith(".pdf")


if __name__ == '__main__':
    pdf_files = FileManager.get_pdf_files("pdfs")
    for pdf_file in pdf_files:
        print(f"path: {pdf_file.path}, name: {pdf_file.name}, name_stripped: {pdf_file.name_stripped}")
