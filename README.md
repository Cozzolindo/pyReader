# 📄 pyReader

**pyReader** is a Python automation tool that reads all PDF files from a specified folder, extracts structured information, and writes it to a CSV file. Designed for simplicity and utility, this project is ideal for automating manual data collection from structured documents like receipts, reports, or form-based PDFs.

---

## 🚀 Features

- Batch processing of all `.pdf` files in a folder
- Data extraction tailored to specific fields within each PDF
- Automatically appends data to existing CSVs (no overwrite)
- Minimal setup, designed to be beginner-friendly and extensible
- Uses modular structure for future enhancements like validations or UI

---

## 🛠️ Built With

- **Python 3.10+**
- [pdfplumber](https://github.com/jsvine/pdfplumber) – for extracting text from PDFs
- [pandas](https://pandas.pydata.org/) – for data manipulation and CSV generation
- `os`, `pathlib` – for file handling and directory management

---

## 📁 Folder Structure

```
pyReader/
├── main.py               # Main script that handles the workflow
├── pdf/                  # Place all PDF files to be processed here
└── output/               # Final CSV output will be stored here
```

---

## ⚙️ How It Works

1. **Prepare Your Files**:
   - Place all the PDF documents inside the `/pdf` folder.

2. **Run the Script**:
   ```bash
   python main.py
   ```

3. **Output**:
   - A `data.csv` file will be generated inside the `/output` folder.
   - If a CSV already exists, new data will be appended automatically.

4. **Custom Logic**:
   - The `main.py` script includes parsing logic tailored to specific PDF structures. You can modify it to fit your documents.

---

## ✨ Example Use Cases

- Extracting financial summaries from invoices
- Compiling survey results from PDF forms
- Automating repetitive PDF data transcription

---

## 📌 Future Improvements

- Add support for scanned PDFs using OCR (e.g., Tesseract)
- GUI for selecting input/output directories
- Unit tests and logging for better maintainability

---

## 🤝 Contributions

Contributions are welcome! If you want to improve the parsing logic or extend functionality, feel free to open a pull request or fork the repository.

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Created by [Carlos Cozzolino](https://github.com/Cozzolindo)

