import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRScanner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Scanner")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.resize(700, 400)

        self.label_font = QtGui.QFont("Segoe UI", 10)
        self.btn_font = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        self.btn_scan = QtWidgets.QPushButton("Scan File")
        self.btn_scan.setFont(self.btn_font)
        self.btn_scan.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_scan.setFixedHeight(35)
        self.btn_scan.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                border-radius: 6px;
                padding-left: 15px;
                padding-right: 15px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        self.btn_scan.clicked.connect(self.scan_file)
        self.btn_scan.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.btn_scan, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.label_field = QtWidgets.QLabel("OCR Text")
        self.label_field.setFont(self.label_font)
        self.main_layout.addWidget(self.label_field)

        self.text_field = QtWidgets.QPlainTextEdit()
        self.text_field.setReadOnly(True)
        self.text_field.setStyleSheet("""
            QPlainTextEdit {
                background-color: #f5f5f5;
                color: black;
                border: 1px solid #777777;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.main_layout.addWidget(self.text_field, stretch=1)

        self.setStyleSheet("background-color: #2b2b2b;")

    def scan_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File or Screenshot", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        if not file_path:
            return

        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            self.text_field.setPlainText(text)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Fout", str(e))

app = QtWidgets.QApplication(sys.argv)
window = OCRScanner()
window.show()
sys.exit(app.exec())