# hand_evaluator.py

from collections import Counter
# No necesitamos importar Card aquí si solo trabajamos con sus ranks numéricos

# --- Constantes para la Evaluación de Manos ---
# Mapeo de valores de cartas a un formato numérico para facilitar la comparación
# El 'As' (A) puede ser tanto 1 (para una escalera A-2-3-4-5) como 14 (para las demás)
RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# Mapeo inverso para mostrar los nombres de las cartas
VALUE_RANKS = {
    2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 1: 'A' # Para el As como 1 en la escalera baja
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

    # Asegúrate de que 'hand' contiene objetos Card con atributo 'rank'
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

# --- Función para formatear los valores de desempate a su representación de carta ---
def format_tie_breaker_for_display(tie_breaker_tuple):
    """
    Convierte una tupla de valores numéricos de desempate en sus equivalentes de carta.
    """
    formatted_values = []
    for val in tie_breaker_tuple:
        if isinstance(val, int):
            # Usar VALUE_RANKS para convertir números a su denominación de carta
            formatted_values.append(VALUE_RANKS.get(val, str(val)))
        else: # Si ya es una cadena (ej. un 'A' si viene del sorted_ranks_for_tiebreaker, aunque el uso actual es solo con int)
            formatted_values.append(str(val))
    return tuple(formatted_values)

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

    # Formatear los valores de desempate para la impresión
    formatted_tb1 = format_tie_breaker_for_display(tie_breaker1)
    formatted_tb2 = format_tie_breaker_for_display(tie_breaker2)

    # Impresión de manos para depuración/información al usuario
    print(f"Tu mano: {type1} {formatted_tb1}")
    print(f"Mano de la Computadora: {type2} {formatted_tb2}")


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