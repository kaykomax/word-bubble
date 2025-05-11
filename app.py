import os
import random  # Added import
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, 
    QApplication, QMessageBox  # Added QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtNetwork import QLocalServer
from settings_dialog import SettingsDialog
from word_list_manager import WordListManager
from custom_input_dialog import CustomInputDialog
from bubble import Bubble
from utils import (
    TRANSLATIONS, load_settings, save_settings, list_word_files, load_words_from_file,
    set_window_title_bar_theme, ICON_FOLDER
)

class WordApp(QWidget):
    VALID_POSITIONS = [
        "random", "top_left", "top_right", "bottom_left", "bottom_right", "center",
        "cascade_top_left", "cascade_top_right", "cascade_top_center",
        "left_to_right_top_left", "left_to_right_bottom_left",
        "right_to_left_top_right", "right_to_left_bottom_right",
        "cascade_right_to_left_top_right", "cascade_left_to_right_top_left",
        "cascade_right_to_left_bottom_right", "cascade_left_to_right_bottom_left",
        "top_to_bottom_top_left", "top_to_bottom_top_center", "top_to_bottom_top_right"
    ]

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.settings = load_settings()
        self.language = self.settings.get("language", "fa")
        self.trans = TRANSLATIONS[self.language]
        self.dark_mode = self.settings.get("dark_mode", False)

        self.setWindowTitle(self.trans["window_title"])
        self.resize(600, 200)

        self.selected_file = self.settings.get("selected_file", "")
        self.playing = True
        self.bubble_duration = self.settings.get("bubble_duration", 5)
        self.bubble_interval = self.settings.get("bubble_interval", 15)
        self.font_size = self.settings.get("font_size", 13)
        self.word_color = QColor(self.settings.get("word_color", "#000000"))
        self.meaning_color = QColor(self.settings.get("meaning_color", "#0000FF"))
        self.bg_color = QColor(self.settings.get("bg_color", "#CCFFFF"))
        self.opacity = self.settings.get("opacity", 0.9)
        self.top_most = self.settings.get("top_most", True)
        self.text_alignment = self.settings.get("text_alignment", "right")
        self.selected_font = self.settings.get("selected_font", "Vazir.ttf")
        self.play_mode = self.settings.get("play_mode", "random")
        self.current_word_index = 0
        self.bubble_position = self.settings.get("bubble_position", "random")
        if self.bubble_position not in self.VALID_POSITIONS:
            self.bubble_position = "random"

        # Initialize single-instance server
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self.handle_new_connection)

        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_bubble)
        if self.playing:
            self.timer.start(self.bubble_interval * 1000)

        self.update_theme()

    def init_ui(self):
        self.settings_btn = QPushButton(self.trans["settings_btn"])
        settings_icon_path = os.path.join(ICON_FOLDER, "settings.png")
        if os.path.exists(settings_icon_path):
            self.settings_btn.setIcon(QIcon(settings_icon_path))
        self.settings_btn.clicked.connect(self.open_settings)

        self.manage_btn = QPushButton(self.trans["manage_btn"])
        manage_icon_path = os.path.join(ICON_FOLDER, "manage.png")
        if os.path.exists(manage_icon_path):
            self.manage_btn.setIcon(QIcon(manage_icon_path))
        self.manage_btn.clicked.connect(self.open_manage)

        self.select_list_btn = QPushButton(self.trans["select_list_btn"])
        select_list_icon_path = os.path.join(ICON_FOLDER, "select_list.png")
        if os.path.exists(select_list_icon_path):
            self.select_list_btn.setIcon(QIcon(select_list_icon_path))
        self.select_list_btn.clicked.connect(self.select_list)

        self.play_mode_btn = QPushButton(self.trans["play_mode_btn"])
        play_mode_icon_path = os.path.join(ICON_FOLDER, "play_mode.png")
        if os.path.exists(play_mode_icon_path):
            self.play_mode_btn.setIcon(QIcon(play_mode_icon_path))
        self.play_mode_btn.clicked.connect(self.select_play_mode)

        self.toggle_btn = QPushButton(self.trans["toggle_play"]["pause"] if self.playing else self.trans["toggle_play"]["play"])
        toggle_icon_path = os.path.join(ICON_FOLDER, "pause.png" if self.playing else "play.png")
        if os.path.exists(toggle_icon_path):
            self.toggle_btn.setIcon(QIcon(toggle_icon_path))
        default_font = QApplication.font()
        font = QFont(default_font)
        font.setWeight(QFont.Bold)
        font.setPointSize(default_font.pointSize() + 4)
        self.toggle_btn.setFont(font)
        self.toggle_btn.setFixedSize(150, 40)
        self.toggle_btn.clicked.connect(self.toggle_play)

        self.dark_mode_switch = QCheckBox(self.trans["dark_mode_label"])
        self.dark_mode_switch.setChecked(self.dark_mode)
        self.dark_mode_switch.stateChanged.connect(self.toggle_dark_mode)

        self.selected_list_label = QLabel(self.get_display_list_name())
        self.selected_list_label.setAlignment(Qt.AlignCenter)
        label_font = QFont(default_font)
        label_font.setWeight(QFont.Bold)
        self.selected_list_label.setFont(label_font)

        hl = QHBoxLayout()
        hl.addWidget(self.settings_btn)
        hl.addWidget(self.manage_btn)
        hl.addWidget(self.select_list_btn)
        hl.addWidget(self.play_mode_btn)

        toggle_layout = QHBoxLayout()
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()

        bottom_hl = QHBoxLayout()
        bottom_hl.addWidget(self.dark_mode_switch)
        bottom_hl.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(hl)
        layout.addSpacing(15)
        layout.addWidget(self.selected_list_label)
        layout.addSpacing(10)
        layout.addLayout(toggle_layout)
        layout.addSpacing(10)
        layout.addLayout(bottom_hl)
        self.setLayout(layout)

    def update_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget { 
                    background-color: #2E2E2E; 
                    color: #FFFFFF; 
                    border: 1px solid #2E2E2E; 
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
                QCheckBox { 
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
            """)
        else:
            self.setStyleSheet("""
                QWidget { 
                    background-color: #F0F0F0; 
                    color: #000000; 
                    border: 1px solid #F0F0F0; 
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
                QCheckBox { 
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
            """)
        set_window_title_bar_theme(self, self.dark_mode)

    def toggle_dark_mode(self, state):
        self.dark_mode = state == Qt.Checked
        self.update_theme()
        self.save_current_settings()

    def get_display_list_name(self):
        if not self.selected_file:
            return self.trans["no_list_selected"]
        return self.trans["selected_list_label"].format(list_name=os.path.splitext(self.selected_file)[0])

    def update_selected_list_label(self):
        self.selected_list_label.setText(self.get_display_list_name())

    def show_bubble(self):
        if not self.playing or not self.selected_file:
            return
        ws = load_words_from_file(self.selected_file)
        if ws:
            if self.play_mode == "random":
                word, meaning = random.choice(ws)
            else:
                word, meaning = ws[self.current_word_index]
                self.current_word_index = (self.current_word_index + 1) % len(ws)
            bubble = Bubble(
                word, meaning, self.font_size, self.word_color,
                self.meaning_color, self.bg_color, self.opacity,
                self.top_most, self.text_alignment, self.selected_font,
                self.language, self.bubble_duration, self.bubble_position
            )
            bubble.show()

    def toggle_play(self):
        self.playing = not self.playing
        self.toggle_btn.setText(self.trans["toggle_play"]["pause"] if self.playing else self.trans["toggle_play"]["play"])
        toggle_icon_path = os.path.join(ICON_FOLDER, "pause.png" if self.playing else "play.png")
        if os.path.exists(toggle_icon_path):
            self.toggle_btn.setIcon(QIcon(toggle_icon_path))
        if self.playing:
            self.timer.start(self.bubble_interval * 1000)
        else:
            self.timer.stop()

    def select_play_mode(self):
        items = self.trans["play_mode_options"]
        current = items[0] if self.play_mode == "sequential" else items[1]
        dialog = CustomInputDialog(
            self, self.trans["play_mode_title"],
            self.trans["play_mode_prompt"],
            items, current_item=current, dark_mode=self.dark_mode
        )
        if dialog.exec_():
            mode = dialog.get_selected_item()
            self.play_mode = "sequential" if mode == items[0] else "random"
            self.current_word_index = 0
            self.save_current_settings()

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec_():
            self.language = dlg.language
            self.trans = TRANSLATIONS[self.language]
            self.bubble_position = dlg.bubble_position
            self.update_ui_texts()
            self.save_current_settings()

    def open_manage(self):
        dlg = WordListManager(self)
        dlg.exec_()

    def select_list(self):
        items = [os.path.splitext(f)[0] for f in list_word_files()]
        if not items:
            QMessageBox.information(self, "Info" if self.language == "en" else "اطلاعات",
                                   self.trans["no_lists_found"])
            return
        dialog = CustomInputDialog(
            self, self.trans["select_list_title"],
            self.trans["select_list_prompt"],
            items, dark_mode=self.dark_mode
        )
        if dialog.exec_():
            file = dialog.get_selected_item()
            self.selected_file = file + ".txt"
            self.current_word_index = 0
            self.save_current_settings()
            self.update_selected_list_label()

    def update_ui_texts(self):
        self.setWindowTitle(self.trans["window_title"])
        self.settings_btn.setText(self.trans["settings_btn"])
        settings_icon_path = os.path.join(ICON_FOLDER, "settings.png")
        if os.path.exists(settings_icon_path):
            self.settings_btn.setIcon(QIcon(settings_icon_path))
        self.manage_btn.setText(self.trans["manage_btn"])
        manage_icon_path = os.path.join(ICON_FOLDER, "manage.png")
        if os.path.exists(manage_icon_path):
            self.manage_btn.setIcon(QIcon(manage_icon_path))
        self.select_list_btn.setText(self.trans["select_list_btn"])
        select_list_icon_path = os.path.join(ICON_FOLDER, "select_list.png")
        if os.path.exists(select_list_icon_path):
            self.select_list_btn.setIcon(QIcon(select_list_icon_path))
        self.play_mode_btn.setText(self.trans["play_mode_btn"])
        play_mode_icon_path = os.path.join(ICON_FOLDER, "play_mode.png")
        if os.path.exists(play_mode_icon_path):
            self.play_mode_btn.setIcon(QIcon(play_mode_icon_path))
        self.toggle_btn.setText(self.trans["toggle_play"]["pause"] if self.playing else self.trans["toggle_play"]["play"])
        toggle_icon_path = os.path.join(ICON_FOLDER, "pause.png" if self.playing else "play.png")
        if os.path.exists(toggle_icon_path):
            self.toggle_btn.setIcon(QIcon(toggle_icon_path))
        self.dark_mode_switch.setText(self.trans["dark_mode_label"])
        self.update_selected_list_label()

    def save_current_settings(self):
        self.settings.update({
            "selected_file": self.selected_file,
            "bubble_duration": self.bubble_duration,
            "bubble_interval": self.bubble_interval,
            "font_size": self.font_size,
            "word_color": self.word_color.name(),
            "meaning_color": self.meaning_color.name(),
            "bg_color": self.bg_color.name(),
            "opacity": self.opacity,
            "top_most": self.top_most,
            "text_alignment": self.text_alignment,
            "selected_font": self.selected_font,
            "language": self.language,
            "play_mode": self.play_mode,
            "bubble_position": self.bubble_position,
            "dark_mode": self.dark_mode
        })
        save_settings(self.settings)

    def handle_new_connection(self):
        socket = self.server.nextPendingConnection()
        socket.readyRead.connect(lambda: self.handle_socket_data(socket))
        socket.disconnected.connect(socket.deleteLater)

    def handle_socket_data(self, socket):
        data = socket.readAll().data().decode()
        if data == "activate":
            self.activate_window()

    def activate_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()