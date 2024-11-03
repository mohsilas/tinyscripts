# PDF OCR Text Extractor

A high-performance, multi-threaded Python script for extracting text from PDF files using Optical Character Recognition (OCR). This tool converts PDF pages to images and processes them in parallel using Tesseract OCR engine, making it significantly faster than traditional single-threaded solutions.

## Features

- Multi-threaded processing for improved performance
- Automatic dependency checking
- Progress tracking for each processed page
- Support for all PDF types (searchable and image-based)
- Configurable thread count
- Cross-platform compatibility (Windows, Linux, macOS)
- Detailed error reporting and handling
- Performance timing metrics

## Prerequisites

Before running the script, you need to install the following dependencies:

### Python Dependencies
```bash
pip install pytesseract pdf2image Pillow
```

### System Dependencies

#### Windows
1. Install Tesseract OCR:
   - Download from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add installation directory to system PATH

2. Install Poppler:
   - Download from [Poppler Releases](https://github.com/oschwartz10612/poppler-windows/releases/)
   - Extract and add `bin` directory to system PATH

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install tesseract
brew install poppler
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-ocr-extractor.git
cd pdf-ocr-extractor
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python pdf_ocr.py input.pdf -o output.txt
```

### Specify Thread Count
```bash
python pdf_ocr.py input.pdf -o output.txt --threads 4
```

### Command Line Arguments
- `pdf_path`: Path to the input PDF file (required)
- `--output`, `-o`: Path to save the extracted text (optional)
- `--threads`, `-t`: Number of threads to use (optional, defaults to CPU count)

### Using as a Module
```python
from pdf_ocr import extract_text_from_pdf

# Basic usage
text = extract_text_from_pdf("input.pdf", "output.txt")

# With custom thread count
text = extract_text_from_pdf("input.pdf", "output.txt", max_threads=4)
```

## Performance

The script's performance depends on several factors:
- Number of CPU cores available
- PDF size and complexity
- System memory
- Storage speed

On a typical modern system, you can expect:
- Single page processing: 2-5 seconds
- Multi-page documents: 1-3 seconds per page when using multiple threads
- Significant performance improvement with threading on multi-core systems

## Error Handling

The script includes comprehensive error handling for:
- Missing dependencies
- Invalid PDF files
- File system errors
- OCR processing failures
- Thread management issues

All errors are logged with detailed messages to help troubleshoot issues.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Guidelines for Contributing:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [Poppler](https://poppler.freedesktop.org/)
- [Python Pillow](https://python-pillow.org/)
