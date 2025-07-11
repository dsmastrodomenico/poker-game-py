# card.py

class Card:
    """Representa una carta individual del mazo."""
    def __init__(self, suit, rank):
        self.suit = suit  # Palo (Corazones, Diamantes, Tréboles, Espadas)
        self.rank = rank  # Valor (2, 3, ..., 10, J, Q, K, A)

    def __str__(self):
        """Representación de cadena de la carta (ej. 'As de Corazones')."""
        return f"{self.rank} de {self.suit}"

    def display_ascii(self, hidden=False):
        """
        Muestra la carta usando caracteres ASCII.
        Si hidden es True, muestra una carta boca abajo.
        """
        if hidden:
            return [
                "┌───────┐",
                "│░░░░░░░│",
                "│░░░░░░░│",
                "│░░░░░░░│",
                "│░░░░░░░│",
                "└───────┘"
            ]

        # Mapeo de palos a caracteres Unicode
        suit_chars = {
            'Corazones': '♥',
            'Diamantes': '♦',
            'Tréboles': '♣',
            'Espadas': '♠'
        }
        suit_char = suit_chars[self.suit]

        # Ajuste para el 10, que ocupa más espacio
        rank_display = self.rank
        if self.rank == '10':
            rank_display = '10' # Asegura que siempre sea '10' y no ' 10'

        lines = [
            "┌───────┐",
            f"│{rank_display:<2}     │", # Alineado a la izquierda
            f"│   {suit_char}   │",
            f"│     {rank_display:>2}│", # Alineado a la derecha
            "└───────┘"
        ]

        # Ajuste para el 10 en la esquina superior izquierda si es necesario
        if len(rank_display) == 1: # Si es un solo caracter (A, K, Q, J, 2-9)
             lines[1] = f"│{rank_display}      │"
             lines[3] = f"│      {rank_display}│"
        else: # Si es '10'
             lines[1] = f"│{rank_display}     │"
             lines[3] = f"│     {rank_display}│"

        return lines