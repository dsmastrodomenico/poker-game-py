# main.py

import random
from card import Card
from deck import Deck
from player import Player
from hand_evaluator import evaluate_hand, compare_hands, RANK_VALUES # Importa las funciones y constantes necesarias

def main():
    print("¡Bienvenido al juego de Póker en Consola!")

    deck = Deck()
    deck.shuffle()

    player = Player("Tú")
    computer = Player("Computadora")

    print("\nRepartiendo cartas iniciales...")
    player.add_cards(deck.deal(5))
    computer.add_cards(deck.deal(5))

    player.display_hand()
    computer.display_hand(hide_all=True)
    print(f"\nLa computadora tiene {len(computer.hand)} cartas en su mano (ocultas).")

    print(f"\nCartas restantes en el mazo: {len(deck)}")

    # --- Fase de cambio de cartas del Jugador ---
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
            
            player_cards_to_change_indices = [int(x) - 1 for x in choice.split()]
            
            if not all(0 <= idx < len(player.hand) for idx in player_cards_to_change_indices):
                print("Error: Ingresa números de carta válidos (1-5).")
                continue
            if len(set(player_cards_to_change_indices)) != len(player_cards_to_change_indices):
                print("Error: No puedes seleccionar la misma carta varias veces.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, ingresa números separados por espacios.")

    if player_cards_to_change_indices:
        print(f"Cambiando {len(player_cards_to_change_indices)} carta(s) para ti...")
        current_hand_copy = list(player.hand) 
        player.hand = [] 

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
    computer_cards_to_change_indices = computer.decide_cards_to_discard() # La IA toma su decisión

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
    computer.display_hand(hide_all=False) # Se revela la mano de la computadora
    
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