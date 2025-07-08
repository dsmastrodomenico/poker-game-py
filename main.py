# main.py

from deck import Deck
from player import Player
from hand_evaluator import compare_hands, RANK_VALUES 
import os 

def clear_console():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def _play_round(deck, player, computer):
    """
    Encapsula la lógica de una única ronda de póker.
    Asume que deck, player y computer ya están inicializados para la ronda.
    """
    print("\n--- Nueva Ronda ---")
    
    # Repartir 5 cartas a cada uno
    print("\nRepartiendo cartas iniciales...")
    player.add_cards(deck.deal(5))
    computer.add_cards(deck.deal(5))

    # Mostrar la mano del Jugador
    player.display_hand()

    # Mostrar la mano de la Computadora (oculta)
    computer.display_hand(hide_all=True)
    print(f"\nLa computadora tiene {len(computer.hand)} cartas en su mano (ocultas).")

    print(f"\nCartas restantes en el mazo: {len(deck)}")

    # --- Fase de cambio de cartas del Jugador (CON CURSOR) ---
    print("\n--- Fase de cambio de cartas ---")
    
    current_selected_card_index = 0
    cards_to_discard = set()

    while True:
        clear_console()
        print("--- Fase de cambio de cartas ---")
        print("\nComandos: 'a' (izquierda), 'd' (derecha), 'x' (seleccionar/deseleccionar), 'enter' (confirmar).")
        print("\nTu mano actual:") 
        player.display_hand(selected_index=current_selected_card_index, marked_for_discard=cards_to_discard)
        print(f"Cartas seleccionadas para descarte: {[idx + 1 for idx in sorted(list(cards_to_discard))]}")
        
        command = input("Tu acción: ").strip().lower()

        if command == 'a':
            current_selected_card_index = (current_selected_card_index - 1 + len(player.hand)) % len(player.hand)
        elif command == 'd':
            current_selected_card_index = (current_selected_card_index + 1) % len(player.hand)
        elif command == 'x':
            if current_selected_card_index in cards_to_discard:
                cards_to_discard.remove(current_selected_card_index)
            else:
                cards_to_discard.add(current_selected_card_index)
        elif command == '':
            break
        else:
            print("Comando inválido. Usa 'a', 'd', 'x' o 'enter'.")
            input("Presiona Enter para continuar...")

    player_cards_to_change_indices = sorted(list(cards_to_discard))

    if player_cards_to_change_indices:
        print(f"\nCambiando {len(player_cards_to_change_indices)} carta(s) para el jugador...") 
        current_hand_copy = list(player.hand) 
        player.hand = [] 

        for i, card in enumerate(current_hand_copy):
            if i not in player_cards_to_change_indices:
                player.hand.append(card)

        try:
            player.add_cards(deck.deal(len(player_cards_to_change_indices)))
            print("Las cartas del jugador fueron cambiadas exitosamente.")
        except ValueError as e:
            print(f"Error al cambiar las cartas del jugador: {e}. No hay suficientes cartas en el mazo.") 
    else:
        print("\nEl jugador no ha cambiado ninguna carta.") 

    player.display_hand()
    print(f"Cartas restantes en el mazo: {len(deck)}")

    # --- Fase de cambio de cartas de la Computadora ---
    print("\n--- Turno de la Computadora para cambiar cartas ---")
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
    print("La mano final del Jugador es:") 
    player.display_hand(hide_all=False)

    print("\nLa mano de la Computadora es:")
    computer.display_hand(hide_all=False)
    
    winner = compare_hands(player.hand, computer.hand)

    if winner == 1:
        print("\n🏆 ¡Felicidades! ¡El Jugador gana la ronda! 🏆") 
    elif winner == 2:
        print("\n🤖 ¡La Computadora gana la ronda!") 
    else:
        print("\n🤝 ¡Es un empate! Nadie gana esta ronda.")
            
    print("\n--- Fin de la Ronda ---")


def main():
    print("¡Bienvenido al juego de Póker en Consola!")

    while True:
        deck = Deck()
        deck.shuffle()
        player = Player("Jugador")
        computer = Player("Computadora")

        _play_round(deck, player, computer)

        play_again = input("\n¿Quieres jugar otra ronda? (s/n): ").strip().lower()
        if play_again != 's' and play_again != 'si':
            print("\n¡Gracias por jugar! ¡Hasta la próxima!")
            break 

if __name__ == "__main__":
    main()