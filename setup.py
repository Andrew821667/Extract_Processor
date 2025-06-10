from setuptools import setup, find_packages

setup(
    name='pdf-extract-processor',
    version='2.1.0',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF>=1.23.0',
        'pdfplumber>=0.9.0',
        'pytesseract>=0.3.10',
        'opencv-python>=4.8.0',
        'Pillow>=10.0.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'tqdm>=4.65.0',
        'click>=8.1.0',
        'PyYAML>=6.0.1',
    ]
)
