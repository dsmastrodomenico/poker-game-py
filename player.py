# player.py

from card import Card # Importa la clase Card para poder usar sus métodos de display

class Player:
    """Representa a un jugador (humano o computadora)."""
    def __init__(self, name="Jugador"):
        self.name = name
        self.hand = []

    def add_cards(self, cards):
        """Añade cartas a la mano del jugador."""
        self.hand.extend(cards)

    def display_hand(self, hide_all=False):
        """
        Muestra las cartas en la mano del jugador.
        Si hide_all es True, oculta todas las cartas (para la computadora).
        """
        print(f"\n--- Mano de {self.name} ---")
        if not self.hand:
            print("Mano vacía.")
            return

        # Obtener las representaciones ASCII de cada carta
        card_lines = []
        for i, card in enumerate(self.hand):
            if hide_all:
                card_lines.append(card.display_ascii(hidden=True))
            else:
                card_lines.append(card.display_ascii())

        # Imprimir las cartas una al lado de la otra
        # Asumiendo que todas las cartas tienen el mismo número de líneas (5)
        for i in range(5): 
            line_to_print = ""
            for j, card_display in enumerate(card_lines):
                line_to_print += card_display[i] + "  " # Agrega un espacio entre cartas
            print(line_to_print)
        
        # Opcional: Mostrar los números de las cartas para selección
        if not hide_all:
            indices_line = ""
            for i in range(len(self.hand)):
                # Ajusta el espaciado para que los números coincidan con las cartas
                indices_line += f"    ({i+1})    " 
            print(indices_line)