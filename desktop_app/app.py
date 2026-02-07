import sys
import base64
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

USERNAME = "admin"
PASSWORD = "whatsupgang"

AUTH_HEADER = {
    "Authorization": "Basic "
    + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
}

API_UPLOAD = "http://127.0.0.1:8000/api/upload/"
API_PDF = "http://127.0.0.1:8000/api/report/pdf/"


class EquipmentVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 200, 700, 500)

        layout = QVBoxLayout()

        self.label = QLabel("Click to load summary")
        layout.addWidget(self.label)

        self.load_btn = QPushButton("Load Summary")
        self.load_btn.clicked.connect(self.load_summary)
        layout.addWidget(self.load_btn)

        self.pdf_btn = QPushButton("Download PDF")
        self.pdf_btn.clicked.connect(self.download_pdf)
        layout.addWidget(self.pdf_btn)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def load_summary(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            self.label.setText("No file selected")
            return

        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                API_UPLOAD, headers=AUTH_HEADER, files=files
            )

        if response.status_code != 200:
            self.label.setText("Failed to load summary")
            return

        data = response.json()
        distribution = data["equipment_type_distribution"]
        self.plot_chart(distribution)
        self.label.setText("Summary loaded")

    def plot_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(distribution.keys(), distribution.values())
        ax.set_title("Equipment Type Distribution")
        ax.set_xlabel("Equipment Type")
        ax.set_ylabel("Count")
        self.canvas.draw()

    def download_pdf(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            "chemical_equipment_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not save_path:
            self.label.setText("PDF save cancelled")
            return

        response = requests.get(API_PDF, headers=AUTH_HEADER)

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            self.label.setText("PDF downloaded successfully")
        else:
            self.label.setText("PDF download failed")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentVisualizer()
    window.show()
    sys.exit(app.exec_())
