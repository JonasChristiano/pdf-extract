import fitz  # PyMuPDF
import os
import argparse

class PDFExtractor:
    def __init__(self, pdf_path, output_folder):
        """
        Initialize the PDFExtractor with the path to the PDF document and the output folder.
        
        :param pdf_path: Path to the PDF file.
        :param output_folder: Path to the folder where the extracted information will be saved.
        """
        self.pdf_document = fitz.open(pdf_path)
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def save_to_file(self, file_path, content, mode="w", encoding="utf-8"):
        """
        Save the given content to a file.
        
        :param file_path: Path to the file.
        :param content: Content to be saved.
        :param mode: File open mode (default is write).
        :param encoding: File encoding (default is UTF-8).
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode, encoding=encoding) as file:
            file.write(content)
        print(f"Content saved to: {file_path}")

    def process_pages(self, pages, process_function):
        """
        Process specified pages with the given function.
        
        :param pages: List of page numbers to process or None for all pages.
        :param process_function: Function to execute for each page.
        """
        page_numbers = range(len(self.pdf_document)) if pages is None else [page -1 for page in pages]
        for page_number in page_numbers:
            page = self.pdf_document.load_page(page_number)
            process_function(page, page_number)

    def extract_images(self, pages=None):
        """
        Extract images from the specified pages.
        
        :param pages: List of page numbers to process or None for all pages.
        """
        images_output_folder = os.path.join(self.output_folder, "images")
        os.makedirs(images_output_folder, exist_ok=True)

        def process_image(page, page_number):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = self.pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_path = os.path.join(images_output_folder, f"page{page_number + 1}_img{img_index + 1}.{image_ext}")
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                print(f"Image saved to: {image_path}")

        self.process_pages(pages, process_image)

    def extract_font_styles_and_sizes(self, pages=None):
        """
        Extract font styles and sizes from the specified pages.
        
        :param pages: List of page numbers to process or None for all pages.
        """
        content = ""

        def process_fonts(page, page_number):
            nonlocal content
            blocks = page.get_text("dict")["blocks"]
            content += f"Page {page_number + 1}\n"
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_name = span["font"]
                            font_size = span["size"]
                            font_color = span["color"]
                            text = span["text"]
                            info = f"Font: {font_name}, Size: {font_size}, Color: {font_color}, Text: {text[:10]}"
                            content += info + "\n"
            content += "\n"

        self.process_pages(pages, process_fonts)
        output_file = os.path.join(self.output_folder, "font_styles.txt")
        self.save_to_file(output_file, content)

    def extract_text(self, pages=None):
        """
        Extract text from the specified pages.
        
        :param pages: List of page numbers to process or None for all pages.
        """
        content = ""

        def process_text(page, page_number):
            nonlocal content
            text = page.get_text("text")
            content += f"Page {page_number + 1}\n{text}\n\n"
            print(f"Text from page {page_number + 1} extracted.")

        self.process_pages(pages, process_text)
        output_file = os.path.join(self.output_folder, "text.txt")
        self.save_to_file(output_file, content)

    def extract_metadata(self):
        """
        Extract metadata from the PDF document.
        """
        metadata = self.pdf_document.metadata
        content = ""
        for key, value in metadata.items():
            content += f"{key}: {value}\n"
        
        output_file = os.path.join(self.output_folder, "metadata.txt")
        self.save_to_file(output_file, content)

    def extract_all(self, pages=None):
        """
        Extract all information from the PDF document.
        
        :param pages: List of page numbers to process or None for all pages.
        """
        self.extract_metadata()
        self.extract_text(pages)
        self.extract_font_styles_and_sizes(pages)
        self.extract_images(pages)

def main():
    parser = argparse.ArgumentParser(description="Extract information from PDF files")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("-e", "--extract",type=str, choices=["images", "fonts", "text", "metadata", "all"], default="all", help="Type of extraction")
    parser.add_argument("-p", "--pages", type=int, nargs="+", default=None, help="Specific pages to extract information from")
    parser.add_argument("-o", "--output_folder", type=str, help="Path to the output folder")

    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    extract_option = args.extract
    pages = args.pages
    output_folder = args.output_folder if args.output_folder else os.path.join(os.getcwd(), "pdf_extract")

    extractor = PDFExtractor(pdf_path, output_folder)

    if extract_option == "images":
        extractor.extract_images(pages)
    elif extract_option == "fonts":
        extractor.extract_font_styles_and_sizes(pages)
    elif extract_option == "text":
        extractor.extract_text(pages)
    elif extract_option == "metadata":
        extractor.extract_metadata()
    elif extract_option == "all":
        extractor.extract_all(pages)

if __name__ == "__main__":
    main()
