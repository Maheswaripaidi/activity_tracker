import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QTextEdit, QLabel, QLineEdit
)

from tracker import ActivityTracker
from report import create_report, export_report
from logger import init_db, clear_database


class ActivityApp(QWidget):
    def __init__(self):
        super().__init__()

        init_db()
        self.tracker = ActivityTracker()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Activity Tracker")

        #  Buttons
        self.start_btn = QPushButton("▶ Start Session")
        self.stop_btn = QPushButton("⏹ Stop Session")
        self.report_btn = QPushButton("📊 Generate Report")

        #  Input
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Enter notes or URL...")

        #  Output
        self.timeline = QTextEdit()
        self.timeline.setReadOnly(True)

        #  Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Session Notes / URL:"))
        layout.addWidget(self.notes_input)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.report_btn)
        layout.addWidget(QLabel("Activity Timeline & Report:"))
        layout.addWidget(self.timeline)

        self.setLayout(layout)

        # 🔗 Button Connections
        self.start_btn.clicked.connect(self.start_session)
        self.stop_btn.clicked.connect(self.stop_session)
        self.report_btn.clicked.connect(self.generate_report)

    # Start Session
    def start_session(self):
        try:
            clear_database()              # 🧹 Clear old DB data
            self.timeline.clear()         # 🧹 Clear UI

            self.tracker.start()

            self.timeline.setText(" Session started...\n")

        except Exception as e:
            self.timeline.setText(f"Error starting session: {e}")

    # Stop Session
    def stop_session(self):
        try:
            self.tracker.stop()
            self.timeline.append("\n Session stopped...\n")

        except Exception as e:
            self.timeline.append(f"\nError stopping session: {e}")

    #  Generate Report
    #  Generate Report
    def generate_report(self):
        try:
            report = create_report()

            self.timeline.setText(report)

            export_report()

            self.timeline.append("\n\n Report exported successfully!")

        except Exception as e:
            self.timeline.setText(f"Error generating report: {e}")


# ▶ Run App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ActivityApp()
    window.resize(650, 750)   # Slightly bigger for better UI
    window.show()
    sys.exit(app.exec())