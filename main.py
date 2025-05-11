import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtNetwork import QLocalSocket
from PyQt5.QtCore import QSystemSemaphore
from app import WordApp
from utils import TRANSLATIONS, load_settings, ICON_FOLDER

def main():
    app = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(font.pointSize() + 2)
    app.setFont(font)

    # Unique name identifier for the application
    SERVER_NAME = "WordBubbleApp"

    # Check if another instance is running
    semaphore = QSystemSemaphore(SERVER_NAME, 1)
    socket = QLocalSocket()

    socket.connectToServer(SERVER_NAME)
    if socket.waitForConnected(500):
        # Another instance is running, send activation message and exit
        socket.write(b"activate")
        socket.waitForBytesWritten(500)
        socket.disconnectFromServer()
        language = load_settings().get("language", "fa")
        trans = TRANSLATIONS[language]
        QMessageBox.warning(None, trans["window_title"], trans["already_running"])
        sys.exit(0)
    else:
        # No instance running, acquire semaphore and start server
        semaphore.acquire()
        window = WordApp()
        if not window.server.listen(SERVER_NAME):
            QMessageBox.warning(None, "Error", "Failed to start single-instance server")
            sys.exit(1)

        icon_path = os.path.join(ICON_FOLDER, "ico.png")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))

        window.show()
        exit_code = app.exec_()

        # Cleanup
        window.server.close()
        semaphore.release()
        sys.exit(exit_code)

if __name__ == "__main__":
    main()