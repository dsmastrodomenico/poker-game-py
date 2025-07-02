# main.py

from deck import Deck
from player import Player
from hand_evaluator import compare_hands, RANK_VALUES # RANK_VALUES es usado por player.py para IA

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

    player_cards_to_change_indices = []
    while True:
        try:
            choice = input("Tu elección: ").strip()
            if choice == '0':
                player_cards_to_change_indices = []
                break
            
            cards_to_change_indices = [int(x) - 1 for x in choice.split()]
            
            # Validar que los índices sean válidos y únicos
            if not all(0 <= idx < len(player.hand) for idx in cards_to_change_indices):
                print("Error: Ingresa números de carta válidos (1-5).")
                continue
            if len(set(cards_to_change_indices)) != len(cards_to_change_indices):
                print("Error: No puedes seleccionar la misma carta varias veces.")
                continue
            player_cards_to_change_indices = cards_to_change_indices # Asignar si es válido
            break
        except ValueError:
            print("Entrada inválida. Por favor, ingresa números separados por espacios.")

    if player_cards_to_change_indices:
        print(f"Cambiando {len(player_cards_to_change_indices)} carta(s) para ti...")
        current_hand_copy = list(player.hand) 
        player.hand = [] 

        removed_cards = [] 
        for i, card in enumerate(current_hand_copy):
            if i not in player_cards_to_change_indices:
                player.hand.append(card)

        try:
            player.add_cards(deck.deal(len(player_cards_to_change_indices)))
            print("Tus cartas fueron cambiadas exitosamente.")
        except ValueError as e:
            print(f"Error al cambiar tus cartas: {e}. No hay suficientes cartas en el mazo.")

    player.display_hand()
    print(f"Cartas restantes en el mazo: {len(deck)}")

    # --- Fase de cambio de cartas de la Computadora ---
    print("\n--- Turno de la Computadora para cambiar cartas ---")
    # La IA toma su decisión
    computer_cards_to_change_indices = computer.decide_cards_to_discard() 

    if computer_cards_to_change_indices:
        print(f"La computadora ha decidido cambiar {len(computer_cards_to_change_indices)} carta(s).")
        current_hand_copy = list(computer.hand)
        computer.hand = []

        for i, card in enumerate(current_hand_copy):
            if i not in computer_cards_to_change_indices:
                computer.hand.append(card)
        
        try:
            computer.add_cards(deck.deal(len(computer_cards_to_change_indices)))
        except ValueError as e:
            print(f"Error al cambiar las cartas de la computadora: {e}. No hay suficientes cartas en el mazo.")
    else:
        print("La computadora no ha cambiado ninguna carta.")


    # --- EVALUACIÓN Y COMPARACIÓN DE MANOS FINALES ---
    print("\n--- Evaluando Manos Finales ---")
    print("Tu mano final es:")
    player.display_hand(hide_all=False)

    print("\nLa mano de la Computadora es:")
    computer.display_hand(hide_all=False)
    
    winner = compare_hands(player.hand, computer.hand)

    if winner == 1:
        print("\n🏆 ¡Felicidades! ¡Tu mano es la ganadora! 🏆")
    elif winner == 2:
        print("\n🤖 ¡La Computadora gana!")
    else:
        print("\n🤝 ¡Es un empate! Nadie gana esta ronda.")
        
    print("\n--- Fin del Juego ---")

if __name__ == "__main__":
    main()