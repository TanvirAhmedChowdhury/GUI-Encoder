import os

try:
    import sys
    import marshal
    import zlib
    import base64
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit, QSpacerItem, QSizePolicy
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt, QTimer

except ImportError:
    os.system("pip3 install PyQt5")
    os.system("pip3 install base64")
    os.system("pip3 install zlib")
    os.system("pip3 install sys")
    os.system("pip3 install marshal")
    import sys
    import marshal
    import zlib
    import base64
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit, QSpacerItem, QSizePolicy
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt, QTimer

class ScriptHandlerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.encoded_code = None
        self.file_name = ""
        self.output_dir = ""
        self.modules_name = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Script Encoder Tool')  # Updated title
        self.setGeometry(100, 100, 600, 400)
        
        # Set window flags to remove the full-screen button
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint)
        
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.header_label = QLabel('\nPY-Script Encoder Tool')  # Updated header text
        self.header_label.setFont(QFont('Comic MS', 18, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.header_label)

        # Spacer to push content down
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_top)

        # Centered content layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(20)

        self.upload_button = QPushButton('Upload Python Script')
        self.upload_button.setFont(QFont('Comic MS', 12))
        self.upload_button.setStyleSheet(self.button_style())
        self.upload_button.clicked.connect(self.upload_file)
        content_layout.addWidget(self.upload_button)

        self.modules_input = QLineEdit()
        self.modules_input.setPlaceholderText('Enter All Modules used in Your Project (e.g., sys requests time)')
        self.modules_input.setFont(QFont('Comic MS', 12))
        self.modules_input.setStyleSheet("background-color: #333333; color: #FFFFFF; padding: 5px;")
        self.modules_input.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.modules_input)

        # Add 'Select Destination Folder' button before 'Encode Script' button
        self.save_path_button = QPushButton('Select Destination Folder')
        self.save_path_button.setFont(QFont('Comic MS', 12))
        self.save_path_button.setStyleSheet(self.button_style())
        self.save_path_button.clicked.connect(self.select_save_path)
        content_layout.addWidget(self.save_path_button)

        self.encode_button = QPushButton('Encode Script')
        self.encode_button.setFont(QFont('Comic MS', 12))
        self.encode_button.setStyleSheet(self.button_style())
        self.encode_button.clicked.connect(self.encode_script)
        content_layout.addWidget(self.encode_button)

        main_layout.addLayout(content_layout)

        # Spacer to push footer down
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer_bottom)

        # Footer
        self.footer_label = QLabel('© Developed by Tanvir Ahmed Chowdhury\n')
        self.footer_label.setFont(QFont('Comic MS', 12))
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setStyleSheet("background-color: #121212; color: #FFFFFF;")
        main_layout.addWidget(self.footer_label)

        self.start_color_transition(self.header_label)

    def start_color_transition(self, label):
        colors = ['#FF5733', '#33FF57', '#3357FF', '#F033FF', '#FFD700']
        self.color_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_color(label, colors))
        self.timer.start(500)

    def update_color(self, label, colors):
        label.setStyleSheet(f"color: {colors[self.color_index]};")
        self.color_index = (self.color_index + 1) % len(colors)

    def button_style(self):
        return """
            QPushButton {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 2px solid #555555;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #777777;
            }
        """

    def upload_file(self):
        file_dialog = QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_name, _ = file_dialog.getOpenFileName(self, "Select Python Script", "", "Python Files (*.py);;All Files (*)", options=options)
        
        if self.file_name:
            self.show_message("File Selected", f"File '{self.file_name}' selected.", QMessageBox.Information)
        # No notification for no file selected

    def select_save_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if directory:
            self.output_dir = directory
            self.show_message("Path Selected", f"Destination folder set to '{self.output_dir}'.", QMessageBox.Information)
        else:
            self.show_message("Path Error", "No folder selected. Please choose a destination folder.", QMessageBox.Warning)

    def show_message(self, title, message, icon_type):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        msg_box.exec_()

    def encode_script(self):
        if not self.file_name:
            self.show_message("Encoding Error", "Please upload a Python script first.", QMessageBox.Warning)
            return
        
        if not self.output_dir:
            self.show_message("Encoding Error", "Please select a destination folder first.", QMessageBox.Warning)
            return
        
        self.modules_name = self.modules_input.text().strip().split()

        if not os.path.isfile(self.file_name):
            self.show_message("File Error", f"File '{self.file_name}' does not exist. Please try again.", QMessageBox.Critical)
            return

        with open(self.file_name, 'r') as file:
            script_content = file.read()

        compiled_code = compile(script_content, self.file_name, 'exec')
        serialized_code = marshal.dumps(compiled_code)
        compressed_code = zlib.compress(serialized_code)
        self.encoded_code = base64.b64encode(compressed_code).decode('utf-8')

        output_file_name = os.path.join(self.output_dir, f"echo_{os.path.splitext(os.path.basename(self.file_name))[0]}.py")
        self.create_decoder_file(output_file_name)
        self.show_message("Encoding Success", f"Script encoded successfully. Run File Name: {os.path.basename(output_file_name)}", QMessageBox.Information)

    def create_decoder_file(self, output_file_name):
        if self.encoded_code:
            import_statements = '\n'.join([f"\timport {module}" for module in self.modules_name])
            install_statements = '\n'.join([f"        os.system('pip3 install {module}')" for module in self.modules_name])
            import_statement = '\n'.join([f"import {module}" for module in self.modules_name])
            decoder_code = f"""
'''
            #####################################
            #####################################
            #########                  ##########
            #########   Developed by   ##########
            #########     Tanvir       ##########
            #########                  ##########
            #####################################
            #####################################
'''

import os
import marshal
import zlib
import base64

try:
{import_statements}
except ImportError:
    modules = {self.modules_name}
    for module in modules:
{install_statements}
{import_statement}
def Decoder():
    encoded_script = \"\"\"{self.encoded_code}\"\"\"
    decoded_data = base64.b64decode(encoded_script)
    decompressed_data = zlib.decompress(decoded_data)
    code_object = marshal.loads(decompressed_data)
    exec(code_object)

if __name__ == "__main__":
    Decoder()
"""
            with open(output_file_name, 'w') as output_file:
                output_file.write(decoder_code)
        else:
            self.show_message("Encoding Error", "No encoded code found. Please encode the script first.", QMessageBox.Warning)

def main():
    app = QApplication(sys.argv)
    ex = ScriptHandlerGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
