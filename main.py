import sys
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QListWidgetItem, QWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

from ui_design import Ui_MainWindow


# ================= 1. КАСТОМНЫЕ ВИДЖЕТЫ =================

class EventCard(QWidget):
    # Создаем сигналы для общения с главным окном
    clicked = pyqtSignal(dict)
    edit_clicked = pyqtSignal(dict)
    delete_clicked = pyqtSignal(dict)

    def __init__(self, event_data):
        super().__init__()
        self.event_data = event_data
        self.setMinimumHeight(70)
        self.setObjectName("EventCard")

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)

        # Время события
        time_label = QLabel(event_data["time"])
        time_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        # Центральная часть: Имя и Название
        center_layout = QVBoxLayout()
        name_label = QLabel(event_data["user"])
        name_label.setStyleSheet(f"color: {event_data['color']}; font-weight: bold; font-size: 10pt;")
        title_label = QLabel(event_data["title"])
        title_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        title_label.setWordWrap(True)

        center_layout.addWidget(name_label)
        center_layout.addWidget(title_label)

        layout.addWidget(time_label)
        layout.addSpacing(15)
        layout.addLayout(center_layout, stretch=1)

        # Кнопки Редактировать и Удалить
        btn_layout = QVBoxLayout()
        btn_edit = QPushButton("✏️")
        btn_edit.setFixedSize(30, 30)
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 16px; padding: 0px; color: black; } QPushButton:hover { background-color: #e0e0e0; border-radius: 5px; }")
        btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.event_data))

        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(30, 30)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 16px; padding: 0px; color: black; } QPushButton:hover { background-color: #e0e0e0; border-radius: 5px; }")
        btn_delete.clicked.connect(lambda: self.delete_clicked.emit(self.event_data))

        btn_layout.addWidget(btn_edit, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        btn_layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Красивая обводка слева в цвет пользователя
        self.setStyleSheet(f"""
            #EventCard {{
                background-color: #ffffff; border-radius: 15px;
                border-left: 6px solid {event_data['color']};
                border-top: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;
            }}
            #EventCard:hover {{ background-color: #f0f0f0; }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.event_data)


class DayHeader(QWidget):
    def __init__(self, day_str, date_str):
        super().__init__()
        self.setMinimumHeight(40)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 10, 5, 5)
        header_label = QLabel(f"{day_str}, {date_str}")
        header_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #333333;")
        layout.addWidget(header_label)
        layout.addStretch()
        self.setLayout(layout)


class MonthlyCard(QWidget):
    edit_clicked = pyqtSignal(dict)
    delete_clicked = pyqtSignal(dict)

    def __init__(self, item_data, next_date, days_left):
        super().__init__()
        self.item_data = item_data
        self.setMinimumHeight(70)
        self.setObjectName("MonthlyCard")

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)

        # Текстовая часть
        text_layout = QVBoxLayout()
        title_label = QLabel(item_data["title"])
        title_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))

        # Логика цвета: если осталось мало дней - красный
        if days_left <= 3:
            color = "#E91E63"
            status_text = f"⚠️ Осталось {days_left} дн. (до {next_date})"
        else:
            color = "#888888"
            status_text = f"Следующий раз: {next_date} (через {days_left} дн.)"

        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"color: {color}; font-size: 10pt;")
        text_layout.addWidget(title_label)
        text_layout.addWidget(status_label)

        # Кнопки
        btn_layout = QVBoxLayout()
        btn_edit = QPushButton("✏️")
        btn_edit.setFixedSize(30, 30)
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 16px; padding: 0px; color: black; } QPushButton:hover { background-color: #e0e0e0; border-radius: 5px; }")
        btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.item_data))

        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(30, 30)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setStyleSheet(
            "QPushButton { background: transparent; border: none; font-size: 16px; padding: 0px; color: black; } QPushButton:hover { background-color: #e0e0e0; border-radius: 5px; }")
        btn_delete.clicked.connect(lambda: self.delete_clicked.emit(self.item_data))

        btn_layout.addWidget(btn_edit, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        btn_layout.addWidget(btn_delete, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        layout.addLayout(text_layout, stretch=1)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.setStyleSheet("""
            #MonthlyCard {
                background-color: #ffffff; border-radius: 15px; border: 1px solid #e0e0e0;
            }
        """)


# ================= 2. ГЛАВНОЕ ОКНО =================

class MyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        QLocale.setDefault(QLocale(QLocale.Language.Russian, QLocale.Country.Russia))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Временный вызов для проверки карточек (удалим позже)
        self.test_cards()

    def test_cards(self):
        # 1. Тестовая карточка события
        test_event = {"time": "14:00", "user": "Тестовый пользователь", "color": "#2196F3", "title": "Поход к врачу"}
        card = EventCard(test_event)
        item = QListWidgetItem()
        item.setSizeHint(card.sizeHint())
        self.ui.list_events.addItem(item)
        self.ui.list_events.setItemWidget(item, card)

        # 2. Тестовая карточка ежемесячного дела
        test_monthly = {"title": "Поменять фильтр для воды"}
        m_card = MonthlyCard(test_monthly, "25.11.2026", 5)
        m_item = QListWidgetItem()
        m_item.setSizeHint(m_card.sizeHint())
        self.ui.list_monthly.addItem(m_item)
        self.ui.list_monthly.setItemWidget(m_item, m_card)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Базовые стили для приложения
    app.setStyleSheet("""
        QMainWindow { background-color: #f5f7fa; }
        QPushButton { background-color: #4A90E2; color: white; border-radius: 8px; padding: 10px 15px; font-weight: bold; border: none; }
        QPushButton:hover { background-color: #357ABD; }
    """)

    window = MyPlanner()
    window.show()
    sys.exit(app.exec())
