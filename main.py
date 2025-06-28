import random

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
    # Solo para verificar que se almacenaron, en un juego real no se mostraría así.
    # Aquí la mostramos oculta para demostrar la funcionalidad.
    computer.display_hand(hide_all=True)
    print(f"\nLa computadora tiene {len(computer.hand)} cartas en su mano (ocultas).")

    # Ejemplo de cómo interactuar con el mazo después de repartir
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
        new_cards = []
        for idx in sorted(cards_to_change_indices, reverse=True): # Eliminar de mayor a menor índice para no afectar los índices
            player.hand.pop(idx)
        
        # Repartir nuevas cartas
        try:
            player.add_cards(deck.deal(len(cards_to_change_indices)))
            print("Cartas cambiadas exitosamente.")
        except ValueError as e:
            print(f"Error al cambiar cartas: {e}. No hay suficientes cartas en el mazo.")

    player.display_hand()
    print(f"Cartas restantes en el mazo: {len(deck)}")


if __name__ == "__main__":
    main()