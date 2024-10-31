from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox
import sys
import subprocess

class FileCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Police Data File Cleaner')
        self.setGeometry(300, 300, 400, 200)
        self.label = QLabel('Drag and drop a file or click "Open File" to clean it', self)
        self.label.setGeometry(10, 20, 380, 40)

        self.open_button = QPushButton('Open File', self)
        self.open_button.setGeometry(150, 100, 100, 40)
        self.open_button.clicked.connect(self.open_file)
    
    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.clean_file(file_path)
    
    def clean_file(self, file_path):
        result = subprocess.run(['python', 'cleaning_script.py', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", "File cleaned and saved successfully!")
        else:
            QMessageBox.warning(self, "Error", f"Failed to clean file. \n{result.stderr}")

app = QApplication(sys.argv)
window = FileCleanerApp()
window.show()
sys.exit(app.exec_())