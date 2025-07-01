# deck.py

import random
from card import Card # Importa la clase Card desde card.py

class Deck:
    """Representa el mazo de 52 cartas."""
    def __init__(self):
        self.cards = []
        self._build()

    def _build(self):
        """Construye un mazo estándar de 52 cartas."""
        suits = ['Corazones', 'Diamantes', 'Tréboles', 'Espadas']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Baraja las cartas del mazo."""
        random.shuffle(self.cards)
        print("Mazo barajado.")

    def deal(self, num_cards):
        """
        Reparte un número específico de cartas del mazo.
        Retorna una lista de objetos Card.
        """
        if len(self.cards) < num_cards:
            raise ValueError("No hay suficientes cartas en el mazo para repartir.")
        
        hand = [self.cards.pop() for _ in range(num_cards)]
        return hand

    def __len__(self):
        """Retorna el número de cartas restantes en el mazo."""
        return len(self.cards)

    def __str__(self):
        """Representación de cadena del mazo."""
        return f"Mazo con {len(self.cards)} cartas restantes."