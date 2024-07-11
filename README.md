# PDF Extractor

This project allows you to extract images, text, metadata and text style from PDF files.

## Functionality

- Extract images from PDF files.
- Extract font style and size.
- Extract text.
- Extract metadata.
- Extract all information.

## Requirements

- Python 3.x
- PyMuPDF (`pip install PyMuPDF`)

## Installation

Clone this repository and install dependencies using `PIP`.

```sh
git clone https://github.com/JonasChristiano/pdf-extractor
cd pdf-extractor
pip install -r requirements.txt
```

## Usage

Execute the script.

```sh
python3 pdf_extract.py path/to/file.pdf --extract [images|fonts|text|metadata|all] --pages 0 1 2 --output_folder output/folder
```

- --extract: What you want to extract (images, fonts, text, metadata, all). Default all.
- --pages: Specify the pages from which you want to extract the information (ex: 0 1 2). Optional.
- --output_folder: Path to output folder. Optional.

The help.

```sh
python3 pdf_extract.py --help
```

## Contribution

If you want to contribute to PDF Extractor, follow these steps:

1. Fork this repository.
2. Create a branch for your feature (git checkout -b my-feature).
3. Commit your changes (git commit -m "Add my feature").
4. Push to the branch (git push origin my-feature).
5. Open a Pull Request.

Please ensure that you follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) commit pattern when making your commits.

License
This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details.
