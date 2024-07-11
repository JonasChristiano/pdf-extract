from setuptools import setup, find_packages

setup(
    name="pdf_extractor",
    version="1.0.0",
    author="Jonas Christiano",
    author_email="jonaschristianoti@gmail.com",
    description="This project allows you to extract images, text, metadata and text style from PDF files.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JonasChristiano/pdf-extractor",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
