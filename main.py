import random
from collections import Counter

# --- Constantes para la Evaluación de Manos ---
# Mapeo de valores de cartas a un formato numérico para facilitar la comparación
# El 'As' (A) puede ser tanto 1 (para una escalera A-2-3-4-5) como 14 (para las demás)
RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# Clases de manos de póker (para asignar un "tipo" y un valor de desempate)
# Asignar un valor numérico a cada tipo de mano para poder compararlas
HAND_RANKS = {
    "Carta Alta": 0,
    "Par": 1,
    "Dos Pares": 2,
    "Trío": 3,
    "Escalera": 4,
    "Color": 5,
    "Full House": 6,
    "Póker": 7,
    "Escalera de Color": 8,
    "Escalera Real": 9
}

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

# --- Funciones Auxiliares para evaluar Escalera y Ases ---

def check_straight(sorted_ranks):
    """
    Verifica si una mano es una escalera.
    Considera el caso de la escalera de A-2-3-4-5 (A como 1).
    """
    # Escalera normal
    is_consecutive = all(sorted_ranks[i] - 1 == sorted_ranks[i+1] for i in range(len(sorted_ranks) - 1))
    if is_consecutive:
        return True

    # Caso especial de escalera baja (A-2-3-4-5)
    # Si las cartas son A, 5, 4, 3, 2 (valores numéricos 14, 5, 4, 3, 2)
    # Se Convierten los valores para la comparación a (1,2,3,4,5)
    if set(sorted_ranks) == {RANK_VALUES['A'], RANK_VALUES['5'], RANK_VALUES['4'], RANK_VALUES['3'], RANK_VALUES['2']}:
        # Si es A-2-3-4-5, se considera escalera. Aquí se normaliza el As a 1 si es necesario para el tie_breaker
        return True
    
    return False

# --- Función de Evaluación de Mano ---

def evaluate_hand(hand):
    """
    Evalúa una mano de 5 cartas y retorna el tipo de mano y los valores de desempate.
    Los valores de desempate son importantes para romper empates entre manos del mismo tipo.
    """
    if len(hand) != 5:
        raise ValueError("Una mano debe tener exactamente 5 cartas.")

    ranks = [RANK_VALUES[card.rank] for card in hand]
    suits = [card.suit for card in hand]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    # Ordenar los valores numéricos de las cartas de mayor a menor para desempate
    sorted_ranks = sorted(ranks, reverse=True)

    # Convertir las cuentas a listas de tuplas (cantidad, valor) y ordenar por cantidad descendente,
    # luego por valor descendente para un fácil acceso a pares, tríos, etc.
    counts = sorted([(count, rank) for rank, count in rank_counts.items()], key=lambda item: (item[0], item[1]), reverse=True)
    
    # --- Verificar combinaciones de mayor a menor valor ---

    is_flush = len(suit_counts) == 1
    is_straight = check_straight(sorted_ranks)
    
    # Para la escalera A-2-3-4-5, el As debe tratarse como el valor más bajo (1) para su desempate
    # Reajustamos sorted_ranks para el desempate de la escalera A-2-3-4-5
    straight_sorted_ranks_for_tiebreaker = sorted_ranks
    if is_straight and sorted_ranks == [RANK_VALUES['A'], RANK_VALUES['5'], RANK_VALUES['4'], RANK_VALUES['3'], RANK_VALUES['2']]:
        straight_sorted_ranks_for_tiebreaker = [RANK_VALUES['5'], RANK_VALUES['4'], RANK_VALUES['3'], RANK_VALUES['2'], 1] # As como 1


    # 1. Escalera Real (Royal Flush) y Escalera de Color (Straight Flush)
    if is_flush and is_straight:
        if sorted_ranks[0] == RANK_VALUES['A'] and sorted_ranks[1] == RANK_VALUES['K'] and sorted_ranks[2] == RANK_VALUES['Q'] and sorted_ranks[3] == RANK_VALUES['J'] and sorted_ranks[4] == RANK_VALUES['10']: # A, K, Q, J, 10 del mismo palo
            return "Escalera Real", (straight_sorted_ranks_for_tiebreaker[0],) # La carta más alta
        return "Escalera de Color", (straight_sorted_ranks_for_tiebreaker[0],) # La carta más alta de la escalera

    # 2. Póker (Four of a Kind)
    if counts[0][0] == 4:
        four_of_a_kind_rank = counts[0][1]
        kicker = counts[1][1]
        return "Póker", (four_of_a_kind_rank, kicker)

    # 3. Full House
    if counts[0][0] == 3 and counts[1][0] == 2:
        three_of_a_kind_rank = counts[0][1]
        pair_rank = counts[1][1]
        return "Full House", (three_of_a_kind_rank, pair_rank)

    # 4. Color (Flush)
    if is_flush:
        return "Color", tuple(sorted_ranks) # Usar todas las cartas para desempate

    # 5. Escalera (Straight)
    if is_straight:
        return "Escalera", (straight_sorted_ranks_for_tiebreaker[0],) # La carta más alta de la escalera

    # 6. Trío (Three of a Kind)
    if counts[0][0] == 3:
        three_of_a_kind_rank = counts[0][1]
        # Kickers son las otras dos cartas, ordenadas descendentemente
        kickers = sorted([c[1] for c in counts[1:]], reverse=True)
        return "Trío", (three_of_a_kind_rank, kickers[0], kickers[1])

    # 7. Dos Pares (Two Pair)
    if counts[0][0] == 2 and counts[1][0] == 2:
        pair1_rank = counts[0][1]
        pair2_rank = counts[1][1]
        kicker = counts[2][1]
        # Asegurarse de que el par más alto esté primero para desempate
        return "Dos Pares", (max(pair1_rank, pair2_rank), min(pair1_rank, pair2_rank), kicker)

    # 8. Par (One Pair)
    if counts[0][0] == 2:
        pair_rank = counts[0][1]
        # Kickers son las otras tres cartas, ordenadas descendentemente
        kickers = sorted([c[1] for c in counts[1:]], reverse=True)
        return "Par", (pair_rank, kickers[0], kickers[1], kickers[2])

    # 9. Carta Alta (High Card)
    return "Carta Alta", tuple(sorted_ranks) # Usar todas las cartas para desempate

# --- Función de Comparación de Manos ---

def compare_hands(hand1, hand2):
    """
    Compara dos manos de póker y determina cuál es la ganadora.
    Retorna 1 si hand1 gana, 2 si hand2 gana, 0 si es empate.
    """
    type1, tie_breaker1 = evaluate_hand(hand1)
    type2, tie_breaker2 = evaluate_hand(hand2)

    rank1 = HAND_RANKS[type1]
    rank2 = HAND_RANKS[type2]

    # Impresión de manos para depuración/información al usuario
    print(f"Tu mano: {type1} {tuple(tb1 for tb1 in tie_breaker1 if isinstance(tb1, int) or isinstance(tb1, tuple))}")
    print(f"Mano de la Computadora: {type2} {tuple(tb2 for tb2 in tie_breaker2 if isinstance(tb2, int) or isinstance(tb2, tuple))}")


    # Paso 1: Comparar el tipo de mano
    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return 2
    else:
        # Paso 2: El tipo de mano es el mismo, usar los valores de desempate
        # Aseguramos que los tie_breakers sean siempre tuplas para comparación directa
        tb1_final = tie_breaker1 if isinstance(tie_breaker1, tuple) else tuple(tie_breaker1)
        tb2_final = tie_breaker2 if isinstance(tie_breaker2, tuple) else tuple(tie_breaker2)

        if tb1_final > tb2_final:
            return 1
        elif tb2_final > tb1_final:
            return 2
        else:
            return 0 # Empate total

# --- Lógica Principal del Juego ---
def main():
    print("¡Bienvenido al juego de Póker en Consola!")

    # 1. Crear y Barajar el Mazo
    deck = Deck()
    deck.shuffle()

    # 2. Crear Jugadores
    player = Player("Tú")
    computer = Player("Computadora")

    # 3. Repartir 5 cartas a cada uno
    print("\nRepartiendo cartas iniciales...")
    player.add_cards(deck.deal(5))
    computer.add_cards(deck.deal(5)) # Las cartas de la computadora se almacenan pero no se muestran

    # 4. Mostrar la mano del Jugador
    player.display_hand()

    # 5. Mostrar la mano de la Computadora (oculta)
    computer.display_hand(hide_all=True) # Sigue oculta
    print(f"\nLa computadora tiene {len(computer.hand)} cartas en su mano (ocultas).")

    print(f"\nCartas restantes en el mazo: {len(deck)}")

    # --- Simulación de un cambio de cartas (sin cursor interactivo por ahora) ---
    print("\n--- Fase de cambio de cartas ---")
    print("¿Qué cartas deseas cambiar? Ingresa los números separados por espacios (ej. 1 3 5).")
    print("Ingresa 0 si no deseas cambiar ninguna carta.")

    while True:
        try:
            choice = input("Tu elección: ").strip()
            if choice == '0':
                cards_to_change_indices = []
                break
            
            cards_to_change_indices = [int(x) - 1 for x in choice.split()]
            
            # Validar que los índices sean válidos y únicos
            if not all(0 <= idx < len(player.hand) for idx in cards_to_change_indices):
                print("Error: Ingresa números de carta válidos (1-5).")
                continue
            if len(set(cards_to_change_indices)) != len(cards_to_change_indices):
                print("Error: No puedes seleccionar la misma carta varias veces.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, ingresa números separados por espacios.")

    if cards_to_change_indices:
        print(f"Cambiando {len(cards_to_change_indices)} carta(s)...")
        # Remover las cartas seleccionadas y añadir nuevas
        # Se crea una nueva lista de la mano para no modificarla mientras se itera
        current_hand_copy = list(player.hand) 
        player.hand = [] # Vacía la mano actual del jugador

        removed_cards = [] # En un juego real, estas irían a la pila de descarte
        for i, card in enumerate(current_hand_copy):
            if i in cards_to_change_indices:
                removed_cards.append(card)
            else:
                player.hand.append(card) # Conserva las cartas no seleccionadas

        # Repartir nuevas cartas
        try:
            player.add_cards(deck.deal(len(cards_to_change_indices)))
            print("Cartas cambiadas exitosamente.")
        except ValueError as e:
            print(f"Error al cambiar cartas: {e}. No hay suficientes cartas en el mazo.")

    player.display_hand()
    print(f"Cartas restantes en el mazo: {len(deck)}")

    # --- EVALUACIÓN Y COMPARACIÓN DE MANOS FINALES ---
    print("\n--- Evaluando Manos Finales ---")
    print("Tu mano final es:")
    player.display_hand(hide_all=False) # Asegúrar que la mano del jugador sea visible

    print("\nLa mano de la Computadora (oculta) es:")
    computer.display_hand(hide_all=True) # La mano de la computadora sigue oculta
    
    winner = compare_hands(player.hand, computer.hand)

    if winner == 1:
        print("\n🏆 ¡Felicidades! ¡Tu mano es la ganadora! 🏆")
    elif winner == 2:
        print("\n🤖 ¡La Computadora gana! Aquí está su mano:")
        computer.display_hand(hide_all=False) # Revelar la mano de la computadora si gana
    else:
        print("\n🤝 ¡Es un empate! Nadie gana esta ronda.")
        print("La mano de la Computadora fue:")
        computer.display_hand(hide_all=False) # Revelar la mano de la computadora en caso de empate
        
    print("\n--- Fin del Juego ---")

if __name__ == "__main__":
    main()