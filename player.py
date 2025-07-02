# player.py

from card import Card # Importa la clase Card para poder usar sus métodos de display
# Importa evaluate_hand y RANK_VALUES de hand_evaluator para que el jugador pueda 'pensar'
from hand_evaluator import evaluate_hand, RANK_VALUES

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
    
    def decide_cards_to_discard(self):
        """
        [IA Básica] Decide qué cartas descartar de la mano.
        Esta lógica es para la computadora.
        Retorna una lista de índices de cartas a descartar.
        """
        if not self.hand:
            return []

        # Evaluar la mano actual de la computadora
        hand_type, tie_breaker_values = evaluate_hand(self.hand)
        
        cards_to_discard_indices = []
        
        # Obtener los valores numéricos de las cartas en la mano para facilitar la manipulación
        hand_ranks_numeric = [RANK_VALUES[card.rank] for card in self.hand]
        # Crear una lista de tuplas (valor_numerico, indice_original) para mantener el rastro de los índices
        indexed_hand_ranks = sorted([(rank, i) for i, rank in enumerate(hand_ranks_numeric)], key=lambda x: x[0], reverse=True)


        if hand_type in ["Escalera Real", "Escalera de Color", "Póker", "Full House", "Escalera", "Color"]:
            # Manos muy fuertes, no se descarta ninguna carta
            print(f"{self.name} no descarta ninguna carta (tiene un/una {hand_type}).")
            return []
        
        elif hand_type == "Trío":
            # Mantener el trío, descartar las 2 cartas restantes (kickers)
            three_of_a_kind_rank = tie_breaker_values[0] # El primer valor en el tie_breaker del Trío es el valor del trío
            
            for i, card in enumerate(self.hand):
                if RANK_VALUES[card.rank] != three_of_a_kind_rank:
                    cards_to_discard_indices.append(i)
            print(f"{self.name} descarta 2 cartas para mantener su Trío.")
            
        elif hand_type == "Dos Pares":
            # Mantener los dos pares, descartar la 1 carta restante (kicker)
            pair1_rank = tie_breaker_values[0]
            pair2_rank = tie_breaker_values[1]
            
            for i, card in enumerate(self.hand):
                card_rank_value = RANK_VALUES[card.rank]
                if card_rank_value != pair1_rank and card_rank_value != pair2_rank:
                    cards_to_discard_indices.append(i)
            print(f"{self.name} descarta 1 carta para mantener sus Dos Pares.")

        elif hand_type == "Par":
            # Mantener el par, descartar las 3 cartas restantes (kickers)
            pair_rank = tie_breaker_values[0] # El primer valor en el tie_breaker del Par es el valor del par
            
            for i, card in enumerate(self.hand):
                if RANK_VALUES[card.rank] != pair_rank:
                    cards_to_discard_indices.append(i)
            print(f"{self.name} descarta 3 cartas para mantener su Par.")

        else: # Carta Alta (la mano más débil)
            # Descartar las 3 cartas más bajas para intentar formar algo
            # Ordenar por valor numérico ascendente para seleccionar las más bajas
            # No necesitamos las originales, solo sus índices
            sorted_by_rank_asc = sorted([(RANK_VALUES[card.rank], i) for i, card in enumerate(self.hand)])
            
            # Descartar las 3 cartas con los valores más bajos
            for i in range(3): 
                cards_to_discard_indices.append(sorted_by_rank_asc[i][1])
            print(f"{self.name} descarta 3 cartas para intentar mejorar su mano.")

        return cards_to_discard_indices