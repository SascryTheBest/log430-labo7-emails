"""
Kafka Historical User Event Consumer (Event Sourcing)
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
from logger import Logger
from typing import Optional
from kafka import KafkaConsumer
from handlers.handler_registry import HandlerRegistry

class UserEventHistoryConsumer:
    """A consumer that starts reading Kafka events from the earliest point from a given topic"""
    
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        registry: HandlerRegistry
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.registry = registry

        # lire depuis le début (auto_offset_reset="earliest")
        # group_id dédié (passé en paramètre)
        self.consumer: Optional[KafkaConsumer] = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")) if v else None,
        )

        self.logger = Logger.get_instance("UserEventHistoryConsumer")
        self.output_file = "user_events_history.json"

    def start(self) -> None:
        """Start consuming messages from Kafka"""
        self.logger.info(f"Démarrer un consommateur historique : {self.group_id}")
        
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                # On va écrire un événement JSON par ligne (JSON Lines)
                for message in self.consumer:
                    value = message.value
                    self.logger.debug(f"Message reçu (offset={message.offset}): {value}")

                    # Sauvegarde
                    f.write(json.dumps(value, ensure_ascii=False))
                    f.write("\n")
                    f.flush()
        except Exception as e:
            self.logger.error(f"Erreur: {e}", exc_info=True)
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the consumer gracefully"""
        if self.consumer:
            self.consumer.close()
            self.logger.info("Arrêter le consommateur!")
