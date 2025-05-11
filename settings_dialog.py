import os
from PyQt5.QtWidgets import QDialog, QSlider, QPushButton, QFormLayout, QComboBox, QFileDialog, QMessageBox, QColorDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from bubble import Bubble
import shutil
from utils import TRANSLATIONS, list_font_files, FONTS_FOLDER, set_window_title_bar_theme

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.language = parent.language
        self.trans = TRANSLATIONS[self.language]
        self.setWindowTitle(self.trans["settings_title"])
        self.resize(400, 600)

        self.init_ui(parent)
        self.update_theme(parent.dark_mode)

    def init_ui(self, parent):
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(1, 20)
        self.time_slider.setValue(parent.bubble_duration)
        self.time_label = QLabel(self.trans["seconds"].format(value=self.time_slider.value()))
        self.time_slider.valueChanged.connect(lambda: self.time_label.setText(self.trans["seconds"].format(value=self.time_slider.value())))

        self.interval_slider = QSlider(Qt.Horizontal)
        self.interval_slider.setRange(1, 60)
        self.interval_slider.setValue(parent.bubble_interval)
        self.interval_label = QLabel(self.trans["seconds"].format(value=self.interval_slider.value()))
        self.interval_slider.valueChanged.connect(lambda: self.interval_label.setText(self.trans["seconds"].format(value=self.interval_slider.value())))

        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setRange(8, 30)
        self.font_slider.setValue(parent.font_size)

        self.word_color_btn = QPushButton(self.trans["word_color"])
        self.word_color_btn.clicked.connect(self.select_word_color)

        self.meaning_color_btn = QPushButton(self.trans["meaning_color"])
        self.meaning_color_btn.clicked.connect(self.select_meaning_color)

        self.bg_color_btn = QPushButton(self.trans["bg_color"])
        self.bg_color_btn.clicked.connect(self.select_bg_color)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(int(parent.opacity * 100))

        self.top_most_combo = QComboBox()
        self.top_most_combo.addItems(self.trans["top_most_options"])
        self.top_most = parent.top_most
        self.top_most_combo.setCurrentIndex(1 if self.top_most else 0)

        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(self.trans["alignment_options"])
        self.alignment = parent.text_alignment
        alignment_map = {"right": 0, "left": 1, "center": 2}
        self.alignment_combo.setCurrentIndex(alignment_map.get(self.alignment, 0))

        self.font_combo = QComboBox()
        font_files = list_font_files()
        if font_files:
            self.font_combo.addItems(font_files)
            current_font = parent.selected_font if parent.selected_font in font_files else font_files[0]
            self.font_combo.setCurrentText(current_font)
        else:
            self.font_combo.addItem(self.trans["no_fonts_found"])
        self.font_combo.currentTextChanged.connect(self.update_font)

        self.import_font_btn = QPushButton(self.trans["import_font_btn"])
        self.import_font_btn.clicked.connect(self.import_font)

        self.position_combo = QComboBox()
        self.position_combo.addItems(self.trans["bubble_position_options"])
        self.bubble_position = parent.bubble_position
        position_map = {
            "random": 0, "top_left": 1, "top_right": 2, "bottom_left": 3, "bottom_right": 4, "center": 5,
            "cascade_top_left": 6, "cascade_top_right": 7, "cascade_top_center": 8,
            "left_to_right_top_left": 9, "left_to_right_bottom_left": 10,
            "right_to_left_top_right": 11, "right_to_left_bottom_right": 12,
            "cascade_right_to_left_top_right": 13, "cascade_left_to_right_top_left": 14,
            "cascade_right_to_left_bottom_right": 15, "cascade_left_to_right_bottom_left": 16,
            "top_to_bottom_top_left": 17, "top_to_bottom_top_center": 18, "top_to_bottom_top_right": 19
        }
        self.position_combo.setCurrentIndex(position_map.get(self.bubble_position, 0))

        self.language_combo = QComboBox()
        self.language_combo.addItems(self.trans["language_options"])
        language_map = {"fa": 0, "en": 1}
        self.language_combo.setCurrentIndex(language_map.get(self.language, 0))
        self.language_combo.currentIndexChanged.connect(self.update_language)

        self.preview_btn = QPushButton(self.trans["preview_btn"])
        self.preview_btn.clicked.connect(self.preview_bubble)

        self.save_btn = QPushButton(self.trans["save_btn"])
        self.save_btn.clicked.connect(self.accept)

        self.selected_word_color = parent.word_color
        self.selected_meaning_color = parent.meaning_color
        self.selected_bg_color = parent.bg_color
        self.selected_font = parent.selected_font

        form = QFormLayout()
        form.setSpacing(12)
        form.addRow(self.trans["bubble_duration"], self.time_slider)
        form.addRow("", self.time_label)
        form.addRow(self.trans["bubble_interval"], self.interval_slider)
        form.addRow("", self.interval_label)
        form.addRow(self.trans["font_size"], self.font_slider)
        form.addRow(self.trans["word_color"], self.word_color_btn)
        form.addRow(self.trans["meaning_color"], self.meaning_color_btn)
        form.addRow(self.trans["bg_color"], self.bg_color_btn)
        form.addRow(self.trans["opacity"], self.opacity_slider)
        form.addRow(self.trans["top_most"], self.top_most_combo)
        form.addRow(self.trans["alignment"], self.alignment_combo)
        form.addRow(self.trans["font_select"], self.font_combo)
        form.addRow(self.trans["import_font_btn"], self.import_font_btn)
        form.addRow(self.trans["bubble_position"], self.position_combo)
        form.addRow(self.trans["language_select"], self.language_combo)
        form.addRow(self.preview_btn)
        form.addRow(self.save_btn)
        self.setLayout(form)

    def update_theme(self, dark_mode):
        if dark_mode:
            self.setStyleSheet("""
                QDialog {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                }
                QComboBox {
                    background-color: #4A4A4A;
                    color: #FFFFFF;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                    border-radius: 4px;
                }
                QComboBox::drop-down {
                    width: 20px;
                    border-left: 1px solid #CCCCCC;
                }
                QComboBox QAbstractItemView {
                    background-color: #4A4A4A;
                    color: #FFFFFF;
                    selection-background-color: #555555;
                }
                QPushButton {
                    background-color: #4A4A4A;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QSlider::groove:horizontal {
                    background: #4A4A4A;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #FFFFFF;
                    width: 16px;
                    height: 16px;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #F0F0F0;
                    color: #000000;
                }
                QComboBox {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #AAAAAA;
                    padding: 5px;
                    border-radius: 4px;
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
                QPushButton {
                    background-color: #E0E0E0;
                    color: #000000;
                    border: 1px solid #AAAAAA;
                    padding: 5px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #CCCCCC;
                }
                QLabel {
                    color: #000000;
                }
                QSlider::groove:horizontal {
                    background: #E0E0E0;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #FFFFFF;
                    width: 16px;
                    height: 16px;
                    border-radius: 8px;
                }
            """)
        set_window_title_bar_theme(self, dark_mode)

    def update_font(self, font_name):
        self.selected_font = font_name

    def import_font(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.trans["import_font_title"], "",
            "Font Files (*.ttf *.otf)"
        )
        if not file_path:
            return

        try:
            font_name = os.path.basename(file_path)
            if not font_name.lower().endswith((".ttf", ".otf")):
                QMessageBox.warning(
                    self, "Error" if self.language == "en" else "خطا",
                    self.trans["import_font_error"]
                )
                return

            dest_path = os.path.join(FONTS_FOLDER, font_name)
            if os.path.exists(dest_path):
                reply = QMessageBox.question(
                    self, "Replace Font" if self.language == "en" else "جایگزینی فونت",
                    self.trans["font_exists_replace"].format(name=font_name)
                )
                if reply != QMessageBox.Yes:
                    return

            shutil.copyfile(file_path, dest_path)
            font_files = list_font_files()
            self.font_combo.clear()
            if font_files:
                self.font_combo.addItems(font_files)
                self.font_combo.setCurrentText(font_name)
                self.selected_font = font_name
            else:
                self.font_combo.addItem(self.trans["no_fonts_found"])

        except Exception as e:
            QMessageBox.warning(
                self, "Error" if self.language == "en" else "خطا",
                f"Failed to import font: {str(e)}" if self.language == "en" else f"خطا در وارد کردن فونت: {str(e)}"
            )

    def update_language(self, index):
        language_map = {0: "fa", 1: "en"}
        new_language = language_map.get(index, "fa")
        if new_language != self.language:
            self.language = new_language
            self.trans = TRANSLATIONS[self.language]
            self.update_ui_texts()

    def update_ui_texts(self):
        self.setWindowTitle(self.trans["settings_title"])
        
        form_layout = self.layout()
        row_labels = [
            ("bubble_duration", 0),
            ("bubble_interval", 2),
            ("font_size", 4),
            ("word_color", 5),
            ("meaning_color", 6),
            ("bg_color", 7),
            ("opacity", 8),
            ("top_most", 9),
            ("alignment", 10),
            ("font_select", 11),
            ("import_font_btn", 12),
            ("bubble_position", 13),
            ("language_select", 14)
        ]
        for key, row in row_labels:
            label_item = form_layout.itemAt(row, QFormLayout.LabelRole)
            if label_item and label_item.widget() and isinstance(label_item.widget(), QLabel):
                label_item.widget().setText(self.trans[key])

        self.time_label.setText(self.trans["seconds"].format(value=self.time_slider.value()))
        self.interval_label.setText(self.trans["seconds"].format(value=self.interval_slider.value()))

        current_top_most = self.top_most
        current_alignment = self.alignment
        current_language = self.language
        current_position = self.bubble_position

        self.top_most_combo.blockSignals(True)
        self.top_most_combo.clear()
        self.top_most_combo.addItems(self.trans["top_most_options"])
        self.top_most_combo.setCurrentIndex(1 if current_top_most else 0)
        self.top_most_combo.blockSignals(False)

        self.alignment_combo.blockSignals(True)
        self.alignment_combo.clear()
        self.alignment_combo.addItems(self.trans["alignment_options"])
        alignment_map = {"right": 0, "left": 1, "center": 2}
        self.alignment_combo.setCurrentIndex(alignment_map.get(current_alignment, 0))
        self.alignment_combo.blockSignals(False)

        self.position_combo.blockSignals(True)
        self.position_combo.clear()
        self.position_combo.addItems(self.trans["bubble_position_options"])
        position_map = {
            "random": 0, "top_left": 1, "top_right": 2, "bottom_left": 3, "bottom_right": 4, "center": 5,
            "cascade_top_left": 6, "cascade_top_right": 7, "cascade_top_center": 8,
            "left_to_right_top_left": 9, "left_to_right_bottom_left": 10,
            "right_to_left_top_right": 11, "right_to_left_bottom_right": 12,
            "cascade_right_to_left_top_right": 13, "cascade_left_to_right_top_left": 14,
            "cascade_right_to_left_bottom_right": 15, "cascade_left_to_right_bottom_left": 16,
            "top_to_bottom_top_left": 17, "top_to_bottom_top_center": 18, "top_to_bottom_top_right": 19
        }
        self.position_combo.setCurrentIndex(position_map.get(current_position, 0))
        self.position_combo.blockSignals(False)

        self.language_combo.blockSignals(True)
        self.language_combo.clear()
        self.language_combo.addItems(self.trans["language_options"])
        language_map = {"fa": 0, "en": 1}
        self.language_combo.setCurrentIndex(language_map.get(current_language, 0))
        self.language_combo.blockSignals(False)

        self.word_color_btn.setText(self.trans["word_color"])
        self.meaning_color_btn.setText(self.trans["meaning_color"])
        self.bg_color_btn.setText(self.trans["bg_color"])
        self.import_font_btn.setText(self.trans["import_font_btn"])
        self.preview_btn.setText(self.trans["preview_btn"])
        self.save_btn.setText(self.trans["save_btn"])

    def select_word_color(self):
        color = QColorDialog.getColor(self.selected_word_color)
        if color.isValid():
            self.selected_word_color = color

    def select_meaning_color(self):
        color = QColorDialog.getColor(self.selected_meaning_color)
        if color.isValid():
            self.selected_meaning_color = color

    def select_bg_color(self):
        color = QColorDialog.getColor(self.selected_bg_color)
        if color.isValid():
            self.selected_bg_color = color

    def preview_bubble(self):
        Bubble(
            self.trans["preview_word"], self.trans["preview_meaning"],
            self.font_slider.value(), self.selected_word_color,
            self.selected_meaning_color, self.selected_bg_color,
            self.opacity_slider.value() / 100.0, self.top_most,
            self.alignment, self.selected_font, self.language,
            self.time_slider.value(), self.bubble_position
        ).show()

    def accept(self):
        position_map = {
            0: "random", 1: "top_left", 2: "top_right", 3: "bottom_left", 4: "bottom_right", 5: "center",
            6: "cascade_top_left", 7: "cascade_top_right", 8: "cascade_top_center",
            9: "left_to_right_top_left", 10: "left_to_right_bottom_left",
            11: "right_to_left_top_right", 12: "right_to_left_bottom_right",
            13: "cascade_right_to_left_top_right", 14: "cascade_left_to_right_top_left",
            15: "cascade_right_to_left_bottom_right", 16: "cascade_left_to_right_bottom_left",
            17: "top_to_bottom_top_left", 18: "top_to_bottom_top_center", 19: "top_to_bottom_top_right"
        }
        self.bubble_position = position_map.get(self.position_combo.currentIndex(), "random")
        self.parent().bubble_duration = self.time_slider.value()
        self.parent().bubble_interval = self.interval_slider.value()
        self.parent().font_size = self.font_slider.value()
        self.parent().word_color = self.selected_word_color
        self.parent().meaning_color = self.selected_meaning_color
        self.parent().bg_color = self.selected_bg_color
        self.parent().opacity = self.opacity_slider.value() / 100.0
        self.parent().top_most = self.top_most_combo.currentIndex() == 1
        self.parent().text_alignment = ["right", "left", "center"][self.alignment_combo.currentIndex()]
        self.parent().selected_font = self.selected_font
        self.parent().language = self.language
        self.parent().bubble_position = self.bubble_position
        self.parent().timer.setInterval(self.parent().bubble_interval * 1000)
        super().accept()