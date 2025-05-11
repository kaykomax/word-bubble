from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils import set_window_title_bar_theme

class CustomInputDialog(QDialog):
    def __init__(self, parent, title, prompt, items=None, default_input="", current_item="", dark_mode=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.dark_mode = dark_mode
        self.inputs = []
        self.selected_item = None
        self.init_ui(prompt, items, default_input, current_item)
        self.update_theme()
        self.setMinimumWidth(400)  

    def init_ui(self, prompt, items, default_input, current_item):
        layout = QVBoxLayout()

        if isinstance(prompt, list):
            for p in prompt:
                label = QLabel(p)
                line_edit = QLineEdit()
                line_edit.setText(default_input if isinstance(default_input, str) else default_input[prompt.index(p)])
                layout.addWidget(label)
                layout.addWidget(line_edit)
                self.inputs.append(line_edit)
        else:
            label = QLabel(prompt)
            layout.addWidget(label)
            if items:
                self.combo = QComboBox()
                self.combo.addItems(items)
                if current_item:
                    self.combo.setCurrentText(current_item)
                layout.addWidget(self.combo)
            else:
                self.line_edit = QLineEdit()
                self.line_edit.setText(default_input)
                layout.addWidget(self.line_edit)
                self.inputs.append(self.line_edit)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK" if self.parent().language == "en" else "تأیید")
        cancel_btn = QPushButton("Cancel" if self.parent().language == "en" else "لغو")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_theme(self):
        set_window_title_bar_theme(self, self.dark_mode)

        if self.dark_mode:
            self.setStyleSheet("""
                QDialog { 
                    background-color: #2E2E2E; 
                    color: #FFFFFF; 
                }
                QLineEdit, QComboBox { 
                    background-color: #4A4A4A; 
                    color: #FFFFFF; 
                    border: 1px solid #555555; 
                    padding: 5px; 
                }
                QPushButton { 
                    background-color: #4A4A4A; 
                    color: #FFFFFF; 
                    border: 1px solid #555555; 
                    padding: 8px; 
                    border-radius: 4px; 
                }
                QPushButton:hover { 
                    background-color: #555555; 
                }
                QLabel { 
                    color: #FFFFFF; 
                }
                QComboBox::drop-down { 
                    width: 20px; 
                    border-left: 1px solid #555555; 
                }
                QComboBox QAbstractItemView { 
                    background-color: #4A4A4A; 
                    color: #FFFFFF; 
                    selection-background-color: #555555; 
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog { 
                    background-color: #F0F0F0; 
                    color: #000000; 
                }
                QLineEdit, QComboBox { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                    border: 1px solid #AAAAAA; 
                    padding: 5px; 
                }
                QPushButton { 
                    background-color: #E0E0E0; 
                    color: #000000; 
                    border: 1px solid #AAAAAA; 
                    padding: 8px; 
                    border-radius: 4px; 
                }
                QPushButton:hover { 
                    background-color: #CCCCCC; 
                }
                QLabel { 
                    color: #000000; 
                }
                QComboBox::drop-down { 
                    width: 20px; 
                    border-left: 1px solid #AAAAAA; 
                }
                QComboBox QAbstractItemView { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                    selection-background-color: #CCCCCC; 
                }
            """)

    def get_input(self):
        return self.line_edit.text() if hasattr(self, 'line_edit') else ""

    def get_inputs(self):
        return [input_field.text() for input_field in self.inputs]

    def get_selected_item(self):
        return self.combo.currentText() if hasattr(self, 'combo') else None