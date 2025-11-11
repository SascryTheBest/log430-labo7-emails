"""
Handler: User Created
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
from pathlib import Path
from handlers.base import EventHandler
from typing import Dict, Any


class UserCreatedHandler(EventHandler):
    """Handles UserCreated events"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        super().__init__()
    
    def get_event_type(self) -> str:
        """Return the event type this handler processes"""
        return "UserCreated"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Create an HTML email based on user creation data"""

        user_id = event_data.get('id')
        name = event_data.get('name')
        email = event_data.get('email')
        user_type_id = event_data.get('user_type_id')
        datetime = event_data.get('datetime')

        try:
            user_type_id_int = int(user_type_id) if user_type_id is not None else 1
        except ValueError:
            user_type_id_int = 1

        # Message personnalisé
        if user_type_id_int == 1:
            custom_message = "Merci d'avoir visité notre magasin !"
        elif user_type_id_int == 2:
            custom_message = "Salut et bienvenue dans l'équipe !"
        elif user_type_id_int == 3:
            custom_message = "Bienvenue dans l'équipe de direction du magasin !"
        else:
            custom_message = "Merci d'être avec nous !"

        current_file = Path(__file__)
        project_root = current_file.parent.parent   
        with open(project_root / "templates" / "welcome_client_template.html", 'r') as file:
            html_content = file.read()
            html_content = html_content.replace("{{user_id}}", str(user_id))
            html_content = html_content.replace("{{name}}", name)
            html_content = html_content.replace("{{email}}", email)
            html_content = html_content.replace("{{creation_date}}", datetime)
            html_content = html_content.replace("{{custom_message}}", custom_message)
        
        filename = os.path.join(self.output_dir, f"welcome_{user_id}.html")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.debug(f"Courriel HTML généré à {name} (ID: {user_id}; Type: {user_type_id}), {filename}")