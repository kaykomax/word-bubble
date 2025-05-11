import random
import os
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont, QFontDatabase
from utils import FONTS_FOLDER, is_rtl

class Bubble(QWidget):
    _cascade_index = {
        "top_left": 0, "top_right": 0, "top_center": 0,
        "right_to_left_top_right": 0, "left_to_right_top_left": 0,
        "right_to_left_bottom_right": 0, "left_to_right_bottom_left": 0
    }
    _index_lock = {}

    def __init__(self, word, meaning, font_size, word_color, meaning_color, bg_color, opacity, top_most, alignment, font_file, language, duration, position_mode):
        super().__init__()
        flags = Qt.FramelessWindowHint | Qt.Tool
        if top_most:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)

        text = f'<span style="color:{word_color.name()}; font-weight: bold;">{word}</span><br><span style="color:{meaning_color.name()};">({meaning})</span>'
        label = QLabel(text, self)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color.name()};
                border-radius: 15px;
                padding: 12px;
                border: 1px solid #AAAAAA;
            }}
        """)
        font_path = os.path.join(FONTS_FOLDER, font_file)
        if os.path.exists(font_path):
            font_db = QFontDatabase()
            font_id = font_db.addApplicationFont(font_path)
            font_families = font_db.applicationFontFamilies(font_id)
            font_family = font_families[0] if font_families else "Arial"
            font = QFont(font_family, font_size)
        else:
            font = QFont("Arial", font_size)
        label.setFont(font)

        alignment_map = {
            "right": Qt.AlignRight | Qt.AlignVCenter,
            "left": Qt.AlignLeft | Qt.AlignVCenter,
            "center": Qt.AlignCenter | Qt.AlignVCenter
        }
        label.setAlignment(alignment_map.get(alignment, Qt.AlignRight | Qt.AlignVCenter))
        label.setLayoutDirection(Qt.RightToLeft if alignment == "right" or (language == "fa" and is_rtl(text)) else Qt.LeftToRight)

        self.resize(label.sizeHint().width() + 20, label.sizeHint().height() + 20)
        geom = QApplication.primaryScreen().geometry()
        screen_width, screen_height = geom.width(), geom.height()
        margin = 20
        bubble_width = self.width()
        bubble_height = self.height()

        bubble_spacing = 200 
        max_bubbles = max(1, (screen_width - 2 * margin) // bubble_spacing) 


        def update_index(key):
            if key not in self._index_lock:
                self._index_lock[key] = False
            if not self._index_lock[key]:
                self._index_lock[key] = True
                current_index = self._cascade_index[key]
                self._cascade_index[key] = (current_index + 1) % max_bubbles
                self._index_lock[key] = False
                return current_index
            return self._cascade_index[key]

        if position_mode == "random":
            x = random.randint(margin, screen_width - bubble_width - margin)
            y = random.randint(margin, screen_height - bubble_height - margin)
        elif position_mode == "top_left":
            x, y = margin, margin
        elif position_mode == "top_right":
            x, y = screen_width - bubble_width - margin, margin
        elif position_mode == "bottom_left":
            x, y = margin, screen_height - bubble_height - margin
        elif position_mode == "bottom_right":
            x, y = screen_width - bubble_width - margin, screen_height - bubble_height - margin
        elif position_mode == "center":
            x, y = (screen_width - bubble_width) // 2, (screen_height - bubble_height) // 2
        elif position_mode.startswith("cascade_") and not position_mode.startswith("cascade_right_to_left_") and not position_mode.startswith("cascade_left_to_right_"):
            key = "_".join(position_mode.split("_")[1:])
            if key == "top_center":
                x = (screen_width - bubble_width) // 2
            elif key == "top_right":
                x = screen_width - bubble_width - margin
            else:
                x = margin
            y = margin + self._cascade_index[key] * (bubble_height + 10)
            self._cascade_index[key] = (self._cascade_index[key] + 1) % ((screen_height - 2 * margin) // (bubble_height + 10))
        elif position_mode == "left_to_right_top_left":
            x, y = margin, margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(screen_width - bubble_width - margin, y))
            self.pos_anim.start()
        elif position_mode == "left_to_right_bottom_left":
            x, y = margin, screen_height - bubble_height - margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(screen_width - bubble_width - margin, y))
            self.pos_anim.start()
        elif position_mode == "right_to_left_top_right":
            x, y = screen_width - bubble_width - margin, margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(margin, y))
            self.pos_anim.start()
        elif position_mode == "right_to_left_bottom_right":
            x, y = screen_width - bubble_width - margin, screen_height - bubble_height - margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(margin, y))
            self.pos_anim.start()
        elif position_mode == "cascade_right_to_left_top_right":
            y = margin
            index = update_index("right_to_left_top_right")
            x = screen_width - bubble_width - margin - (index * bubble_spacing)
            if x < margin:
                self._cascade_index["right_to_left_top_right"] = 0
                x = screen_width - bubble_width - margin
        elif position_mode == "cascade_left_to_right_top_left":
            y = margin
            index = update_index("left_to_right_top_left")
            x = margin + (index * bubble_spacing)
            if x > screen_width - bubble_width - margin:
                self._cascade_index["left_to_right_top_left"] = 0
                x = margin
        elif position_mode == "cascade_right_to_left_bottom_right":
            y = screen_height - bubble_height - margin
            index = update_index("right_to_left_bottom_right")
            x = screen_width - bubble_width - margin - (index * bubble_spacing)
            if x < margin:
                self._cascade_index["right_to_left_bottom_right"] = 0
                x = screen_width - bubble_width - margin
        elif position_mode == "cascade_left_to_right_bottom_left":
            y = screen_height - bubble_height - margin
            index = update_index("left_to_right_bottom_left")
            x = margin + (index * bubble_spacing)
            if x > screen_width - bubble_width - margin:
                self._cascade_index["left_to_right_bottom_left"] = 0
                x = margin
        elif position_mode == "top_to_bottom_top_left":
            x, y = margin, margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(x, screen_height - bubble_height - margin))
            self.pos_anim.start()
        elif position_mode == "top_to_bottom_top_center":
            x, y = (screen_width - bubble_width) // 2, margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(x, screen_height - bubble_height - margin))
            self.pos_anim.start()
        elif position_mode == "top_to_bottom_top_right":
            x, y = screen_width - bubble_width - margin, margin
            self.pos_anim = QPropertyAnimation(self, b"pos")
            self.pos_anim.setDuration(duration * 1000)
            self.pos_anim.setStartValue(QPoint(x, y))
            self.pos_anim.setEndValue(QPoint(x, screen_height - bubble_height - margin))
            self.pos_anim.start()
        else:
            x = random.randint(margin, screen_width - bubble_width - margin)
            y = random.randint(margin, screen_height - bubble_height - margin)

        self.move(x, y)
        self.setWindowOpacity(opacity)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(duration * 1000)
        self.anim.setStartValue(opacity)
        self.anim.setEndValue(0)
        self.anim.finished.connect(self.close)
        self.anim.start()