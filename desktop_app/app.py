import sys
import requests
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


API_URL = "http://127.0.0.1:8000/api/upload/"


class EquipmentVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer (Desktop)")
        self.setGeometry(200, 200, 600, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Upload CSV file to visualize equipment data")
        layout.addWidget(self.label)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(self.upload_btn)

        self.summary_label = QLabel("")
        layout.addWidget(self.summary_label)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                response = requests.post(API_URL, files={"file": f})

            if response.status_code != 200:
                raise Exception("Upload failed")

            data = response.json()
            self.show_summary(data)
            self.plot_chart(data["equipment_type_distribution"])

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_summary(self, data):
        text = (
            f"Total Count: {data['total_count']}\n"
            f"Average Flowrate: {data['average_flowrate']}\n"
            f"Average Pressure: {data['average_pressure']}\n"
            f"Average Temperature: {data['average_temperature']}"
        )
        self.summary_label.setText(text)

    def plot_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = list(distribution.keys())
        counts = list(distribution.values())

        ax.bar(types, counts)
        ax.set_title("Equipment Type Distribution")
        ax.set_xlabel("Equipment Type")
        ax.set_ylabel("Count")

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentVisualizer()
    window.show()
    sys.exit(app.exec_())
