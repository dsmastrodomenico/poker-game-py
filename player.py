# player.py

from card import Card
from hand_evaluator import evaluate_hand, RANK_VALUES # Se mantiene si evaluate_hand es usado internamente por Player, sino se remueve

class Player:
    """Representa a un jugador (humano o computadora)."""
    def __init__(self, name="Jugador"):
        self.name = name
        self.hand = []

    def add_cards(self, cards):
        """Añade cartas a la mano del jugador."""
        self.hand.extend(cards)

    # display_hand ahora acepta 'selected_index' y 'marked_for_discard' ---
    def display_hand(self, hide_all=False, selected_index=-1, marked_for_discard=None):
        """
        Muestra las cartas en la mano del jugador.
        Si hide_all es True, oculta todas las cartas (para la computadora).
        selected_index: Índice de la carta sobre la que está el cursor (-1 si no hay cursor).
        marked_for_discard: Lista/Set de índices de cartas marcadas para descarte.
        """
        if marked_for_discard is None:
            marked_for_discard = set() # Inicializa como un set vacío si no se proporciona

        print(f"\n--- Mano de {self.name} ---")
        if not self.hand:
            print("Mano vacía.")
            return

        card_lines_list = [] # Lista de listas de líneas ASCII para cada carta
        for i, card in enumerate(self.hand):
            card_display_lines = card.display_ascii(hidden=hide_all)
            
            # --- Personalizar la visualización de la carta ---
            # Si la carta está marcada para descarte, añadir un indicador
            if not hide_all and i in marked_for_discard:
                card_display_lines[0] = card_display_lines[0].replace('┌', '╔').replace('─', '═').replace('┐', '╗')
                card_display_lines[4] = card_display_lines[4].replace('└', '╚').replace('─', '═').replace('┘', '╝')
                card_display_lines[2] = card_display_lines[2][:3] + " [X] " + card_display_lines[2][7:] # Marca central
                
            # Si esta es la carta seleccionada por el cursor
            if not hide_all and i == selected_index:
                # Cambiar los bordes para resaltar el cursor
                card_display_lines[0] = card_display_lines[0].replace('┌', '►').replace('┐', '◄')
                card_display_lines[4] = card_display_lines[4].replace('└', '►').replace('┘', '◄')

            card_lines_list.append(card_display_lines)

        # Imprimir las cartas una al lado de la otra
        if card_lines_list: # Asegúrate de que haya cartas para imprimir
            for i in range(len(card_lines_list[0])): # Itera sobre las líneas de una carta (asumiendo que todas tienen 5 líneas)
                line_to_print = ""
                for j, card_display in enumerate(card_lines_list):
                    line_to_print += card_display[i] + "  " # Agrega un espacio entre cartas
                print(line_to_print)
        
        # Mostrar los números de las cartas para selección
        if not hide_all:
            indices_line = ""
            for i in range(len(self.hand)):
                indices_line += f"    ({i+1})    " # Alinea los números con las cartas
            print(indices_line)
    
    def decide_cards_to_discard(self):
        """
        [IA Básica] Decide qué cartas descartar de la mano.
        Esta lógica es para la computadora.
        Retorna una lista de índices de cartas a descartar.
        """
        if not self.hand:
            return []

        hand_type, tie_breaker_values = evaluate_hand(self.hand)
        
        cards_to_discard_indices = []
        
        hand_ranks_numeric = [RANK_VALUES[card.rank] for card in self.hand]
        indexed_hand_ranks = sorted([(rank, i) for i, rank in enumerate(hand_ranks_numeric)], key=lambda x: x[0], reverse=True)


        if hand_type in ["Escalera Real", "Escalera de Color", "Póker", "Full House", "Escalera", "Color"]:
            print(f"{self.name} no descarta ninguna carta (tiene un/una {hand_type}).")
            return []
        
        elif hand_type == "Trío":
            three_of_a_kind_rank = tie_breaker_values[0]
            
            for i, card in enumerate(self.hand):
                if RANK_VALUES[card.rank] != three_of_a_kind_rank:
                    cards_to_discard_indices.append(i)
            print(f"{self.name} descarta 2 cartas para mantener su Trío.")
            
        elif hand_type == "Dos Pares":
            pair1_rank = tie_breaker_values[0]
            pair2_rank = tie_breaker_values[1]
            
            for i, card in enumerate(self.hand):
                card_rank_value = RANK_VALUES[card.rank]
                if card_rank_value != pair1_rank and card_rank_value != pair2_rank:
                    cards_to_discard_indices.append(i)
            print(f"{self.name} descarta 1 carta para mantener sus Dos Pares.")

        elif hand_type == "Par":
            pair_rank = tie_breaker_values[0]
            
            for i, card in enumerate(self.hand):
                if RANK_VALUES[card.rank] != pair_rank:
                    cards_to_discard_indices.append(i)
            print(f"{self.name} descarta 3 cartas para mantener su Par.")

        else: # Carta Alta
            sorted_by_rank_asc = sorted([(RANK_VALUES[card.rank], i) for i, card in enumerate(self.hand)])
            
            for i in range(3): 
                cards_to_discard_indices.append(sorted_by_rank_asc[i][1])
            print(f"{self.name} descarta 3 cartas para intentar mejorar su mano.")

        return cards_to_discard_indices