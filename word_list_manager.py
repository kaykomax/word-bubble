import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QListWidget, 
    QMessageBox, QFileDialog, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from custom_input_dialog import CustomInputDialog
from utils import (
    TRANSLATIONS, list_word_files, load_words_from_file, save_words_to_file, 
    set_window_title_bar_theme
)

class WordListManager(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.language = parent.language
        self.trans = TRANSLATIONS[self.language]
        self.dark_mode = parent.dark_mode
        self.setWindowTitle(self.trans["manage_title"])
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.update_theme()

    def init_ui(self):
        self.list_combo = QComboBox()
        self.list_combo.addItems(list_word_files())
        self.list_combo.currentTextChanged.connect(self.load_words)
        font = QFont(QApplication.font())
        font.setPointSize(font.pointSize() + 2)
        self.list_combo.setFont(font)

        self.words_list = QListWidget()
        self.words_list.setFont(font)
        self.load_words(self.list_combo.currentText())

        self.add_word_btn = QPushButton(self.trans["add_word_btn"])
        self.add_word_btn.clicked.connect(self.add_word)

        self.edit_word_btn = QPushButton(self.trans["edit_word_btn"])
        self.edit_word_btn.clicked.connect(self.edit_word)

        self.delete_word_btn = QPushButton(self.trans["delete_word_btn"])
        self.delete_word_btn.clicked.connect(self.delete_word)

        self.new_list_btn = QPushButton(self.trans["new_list_btn"])
        self.new_list_btn.clicked.connect(self.new_list)

        self.rename_list_btn = QPushButton(self.trans["rename_list_btn"])
        self.rename_list_btn.clicked.connect(self.rename_list)

        self.delete_list_btn = QPushButton(self.trans["delete_list_btn"])
        self.delete_list_btn.clicked.connect(self.delete_list)

        self.import_list_btn = QPushButton(self.trans["import_list_btn"])
        self.import_list_btn.clicked.connect(self.import_list)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.add_word_btn)
        btn_layout.addWidget(self.edit_word_btn)
        btn_layout.addWidget(self.delete_word_btn)
        btn_layout.addSpacing(20)
        btn_layout.addWidget(self.new_list_btn)
        btn_layout.addWidget(self.rename_list_btn)
        btn_layout.addWidget(self.delete_list_btn)
        btn_layout.addWidget(self.import_list_btn)
        btn_layout.addStretch()

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.list_combo)
        list_layout.addWidget(self.words_list)

        main_layout = QHBoxLayout()
        main_layout.addLayout(list_layout, 3)
        main_layout.addLayout(btn_layout, 1)
        self.setLayout(main_layout)

    def update_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QDialog { 
                    background-color: #2E2E2E; 
                    color: #FFFFFF; 
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
                QListWidget { 
                    background-color: #3A3A3A; 
                    color: #FFFFFF; 
                    border: 1px solid #555555; 
                }
                QComboBox { 
                    background-color: #4A4A4A; 
                    color: #FFFFFF; 
                    border: 1px solid #555555; 
                    padding: 5px; 
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
                QListWidget { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                    border: 1px solid #AAAAAA; 
                }
                QComboBox { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                    border: 1px solid #AAAAAA; 
                    padding: 5px; 
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
        set_window_title_bar_theme(self, self.dark_mode)

    def load_words(self, file_name):
        self.words_list.clear()
        if file_name:
            words = load_words_from_file(file_name)
            for word, meaning in words:
                self.words_list.addItem(f"{word} :: {meaning}")

    def add_word(self):
        if not self.list_combo.currentText():
            QMessageBox.warning(self, "Error" if self.language == "en" else "خطا",
                               self.trans["no_list_error"])
            return
        dialog = CustomInputDialog(
            self, self.trans["add_word_title"],
            [self.trans["add_word_prompt"], self.trans["add_meaning_prompt"]],
            dark_mode=self.dark_mode
        )
        if dialog.exec_():
            word, meaning = dialog.get_inputs()
            if word and meaning:
                words = load_words_from_file(self.list_combo.currentText())
                words.append((word, meaning))
                save_words_to_file(self.list_combo.currentText(), words)
                self.load_words(self.list_combo.currentText())

    def edit_word(self):
        if not self.list_combo.currentText() or not self.words_list.currentItem():
            return
        current_text = self.words_list.currentItem().text()
        word, meaning = current_text.split(" :: ", 1)
        dialog = CustomInputDialog(
            self, self.trans["edit_word_title"],
            [self.trans["add_word_prompt"], self.trans["edit_meaning_prompt"]],
            [word, meaning], dark_mode=self.dark_mode
        )
        if dialog.exec_():
            new_word, new_meaning = dialog.get_inputs()
            if new_word and new_meaning:
                words = load_words_from_file(self.list_combo.currentText())
                index = self.words_list.currentRow()
                words[index] = (new_word, new_meaning)
                save_words_to_file(self.list_combo.currentText(), words)
                self.load_words(self.list_combo.currentText())

    def delete_word(self):
        if not self.list_combo.currentText() or not self.words_list.currentItem():
            return
        reply = QMessageBox.question(
            self, "Confirm" if self.language == "en" else "تأیید",
            self.trans["delete_word_confirm"],
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            words = load_words_from_file(self.list_combo.currentText())
            index = self.words_list.currentRow()
            words.pop(index)
            save_words_to_file(self.list_combo.currentText(), words)
            self.load_words(self.list_combo.currentText())

    def new_list(self):
        dialog = CustomInputDialog(
            self, self.trans["new_list_title"],
            self.trans["new_list_prompt"], dark_mode=self.dark_mode
        )
        if dialog.exec_():
            name = dialog.get_input()
            if name:
                file_name = f"{name}.txt"
                if file_name in list_word_files():
                    QMessageBox.warning(
                        self, "Error" if self.language == "en" else "خطا",
                        self.trans["list_exists_error"]
                    )
                    return
                save_words_to_file(file_name, [])
                self.list_combo.addItem(file_name)
                self.list_combo.setCurrentText(file_name)

    def rename_list(self):
        if not self.list_combo.currentText():
            return
        dialog = CustomInputDialog(
            self, self.trans["rename_list_title"],
            self.trans["rename_list_prompt"],
            default_input=os.path.splitext(self.list_combo.currentText())[0],
            dark_mode=self.dark_mode
        )
        if dialog.exec_():
            new_name = dialog.get_input()
            if new_name:
                new_file_name = f"{new_name}.txt"
                if new_file_name in list_word_files():
                    QMessageBox.warning(
                        self, "Error" if self.language == "en" else "خطا",
                        self.trans["list_exists_error"]
                    )
                    return
                old_file = self.list_combo.currentText()
                os.rename(
                    os.path.join("word_lists", old_file),
                    os.path.join("word_lists", new_file_name)
                )
                index = self.list_combo.currentIndex()
                self.list_combo.removeItem(index)
                self.list_combo.addItem(new_file_name)
                self.list_combo.setCurrentText(new_file_name)
                if self.parent().selected_file == old_file:
                    self.parent().selected_file = new_file_name
                    self.parent().update_selected_list_label()
                    self.parent().save_current_settings()

    def delete_list(self):
        if not self.list_combo.currentText():
            return
        reply = QMessageBox.question(
            self, "Confirm" if self.language == "en" else "تأیید",
            self.trans["delete_list_confirm"],
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            file_name = self.list_combo.currentText()
            os.remove(os.path.join("word_lists", file_name))
            self.list_combo.removeItem(self.list_combo.currentIndex())
            self.words_list.clear()
            if self.parent().selected_file == file_name:
                self.parent().selected_file = ""
                self.parent().update_selected_list_label()
                self.parent().save_current_settings()

    def import_list(self):
        dialog = CustomInputDialog(
            self, self.trans["import_list_title"],
            self.trans["import_list_prompt"],
            items=None,  # Explicitly set items to None for text input
            dark_mode=self.dark_mode
        )
        if dialog.exec_():
            name = dialog.get_input()
            if name:
                file_name = f"{name}.txt"
                if file_name in list_word_files():
                    reply = QMessageBox.question(
                        self, "Confirm" if self.language == "en" else "تأیید",
                        self.trans["import_list_replace"].format(name=name),
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                    if reply != QMessageBox.Yes:
                        return
                file_path, _ = QFileDialog.getOpenFileName(
                    self, self.trans["import_list_title"], "",
                    "Text Files (*.txt)"
                )
                if file_path:
                    words = []
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line and "::" in line:
                                    word, meaning = line.split("::", 1)
                                    word = word.strip()
                                    meaning = meaning.strip()
                                    if word and meaning:
                                        words.append((word, meaning))
                        if not words:
                            QMessageBox.warning(
                                self, "Error" if self.language == "en" else "خطا",
                                self.trans["import_list_empty"]
                            )
                            return
                        save_words_to_file(file_name, words)
                        if file_name not in [self.list_combo.itemText(i) for i in range(self.list_combo.count())]:
                            self.list_combo.addItem(file_name)
                        self.list_combo.setCurrentText(file_name)
                    except Exception:
                        QMessageBox.warning(
                            self, "Error" if self.language == "en" else "خطا",
                            self.trans["import_list_invalid"]
                        )