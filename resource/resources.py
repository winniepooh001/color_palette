
from PySide6.QtCore import QSize
import os
resource_dir = os.path.dirname(os.path.abspath(__file__))
LayoutSettings = {
    'login_window': QSize(400, 600),
    'theme_file': f"{resource_dir}/themes.json",
    "setting_file": f"{resource_dir}/settings.json",
    "links_file": f"{resource_dir}/links.json",
    "style_sheet": f"{resource_dir}/style.txt",
    "style_sheet_variables": f"{resource_dir}/stylesheet_settings.json",
    "custom_style_sheet": f"{resource_dir}/custom_style.txt",
    "custom_style_json": f"{resource_dir}/custom_style_variable.json"
}
