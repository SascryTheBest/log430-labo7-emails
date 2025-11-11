"""
Handler: User Deleted
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
from datetime import datetime
from pathlib import Path
from handlers.base import EventHandler
from typing import Dict, Any

class UserDeletedHandler(EventHandler):
    """Handles UserDeleted events"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        super().__init__()
    
    def get_event_type(self) -> str:
        """Return the event type this handler processes"""
        return "UserDeleted"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Create an HTML email based on user deletion data"""
        # TODO: implémentation basée sur UserCreated
        # On récupère les champs envoyés dans l’événement UserDeleted
        user_id = event_data.get("id")
        name = event_data.get("name")
        email = event_data.get("email")
        user_type_id = event_data.get("user_type_id") ###########
        deleted_at = event_data.get("datetime")

        try:
            user_type_id_int = int(user_type_id) if user_type_id is not None else 1 ###########
        except ValueError:
            user_type_id_int = 1

        # Message personnalisé
        if user_type_id_int == 1:
            custom_message = "Merci d'avoir magasiné chez nous. Nous espérons vous revoir bientôt."
        elif user_type_id_int == 2:
            custom_message = "Merci pour ton travail au sein de l'équipe. Bonne continuation !"
        elif user_type_id_int == 3:
            custom_message = "Merci pour votre leadership au sein du magasin. Bonne continuation !"
        else:
            custom_message = "Merci pour votre temps avec nous." ###########

        current_file = Path(__file__)
        project_root = current_file.parent.parent
        template_path = project_root / "templates" / "goodbye_client_template.html"

        with open(template_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            html_content = html_content.replace("{{user_id}}", str(user_id))
            html_content = html_content.replace("{{name}}", name or "")
            html_content = html_content.replace("{{email}}", email or "")
            html_content = html_content.replace("{{deletion_date}}", deleted_at or "")
            html_content = html_content.replace("{{custom_message}}", custom_message)

        filename = os.path.join(self.output_dir, f"goodbye_{user_id}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.logger.debug(event_data)
        self.logger.debug(f"Courriel HTML généré à {name} (ID: {user_id}) at {filename}")
