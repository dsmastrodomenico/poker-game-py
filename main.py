# main.py

from deck import Deck
from player import Player
from hand_evaluator import compare_hands, RANK_VALUES, VALUE_RANKS
import os 

def clear_console():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def _play_round_poker(deck, player, computer):
    """
    Encapsula la lógica de una única ronda de póker.
    Retorna True si el Jugador gana la ronda de póker, False si pierde o empata.
    """
    print("\n--- Iniciando Ronda de Póker ---")
    
    # Repartir 5 cartas a cada uno
    print("\nRepartiendo cartas iniciales...")
    player.add_cards(deck.deal(5))
    computer.add_cards(deck.deal(5))

    # Mostrar la mano del Jugador
    player.display_hand()

    # Mostrar la mano de la Computadora (oculta)
    print("\nLa mano de la Computadora (oculta) es:")
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
        print("\n🏆 ¡Felicidades! ¡El Jugador gana la ronda de Póker! 🏆")
        return True # El jugador ganó, para pasar al juego rápido
    elif winner == 2:
        print("\n🤖 ¡La Computadora gana la ronda de Póker!")
        return False # La computadora ganó o hubo empate
    else:
        print("\n🤝 ¡Es un empate! Nadie gana esta ronda de Póker.")
        return False # La computadora ganó o hubo empate
            
def _play_quick_game(deck, player, computer):
    """
    Mecánica de juego rápido de "carta más alta".
    Usa las cartas restantes del mazo de la ronda de póker.
    Retorna True si el mazo se agotó, False si el jugador decide detenerse.
    """
    print("\n--- Iniciando Juego Rápido: ¡Carta Más Alta! ---")
    
    while True:
        clear_console() # Limpiar la consola al inicio de cada turno rápido
        print("\n--- Juego Rápido: ¡Carta Más Alta! ---")
        print(f"Cartas restantes en el mazo: {len(deck)}")

        if len(deck) < 2: # Necesitamos al menos 2 cartas para que cada uno saque una
            print("\n¡El mazo se ha agotado para el juego rápido! Volviendo al Póker regular.")
            input("Presiona Enter para continuar...") # Pausa para que el usuario lea
            return True # Indica que el mazo se agotó

        input("\nPresiona Enter para sacar una carta...")
        
        # Sacar una carta para cada uno
        player_card = deck.deal(1)[0]
        computer_card = deck.deal(1)[0]

        # Mostrar las cartas sacadas usando display_hand de Player
        # Para esto, necesitamos que Player pueda "mostrar" una sola carta o una lista de cartas
        # temporalmente. La forma más sencilla es crear una mano temporal para cada uno.

        # Mano temporal para el Jugador
        temp_player = Player("Jugador")
        temp_player.add_cards([player_card])
        print("\nTu carta:")
        temp_player.display_hand()

        # Mano temporal para la Computadora
        temp_computer = Player("Computadora")
        temp_computer.add_cards([computer_card])
        print("\nLa carta de la Computadora:")
        temp_computer.display_hand()

        player_rank_val = RANK_VALUES[player_card.rank]
        computer_rank_val = RANK_VALUES[computer_card.rank]

        if player_rank_val > computer_rank_val:
            print(f"\n¡El Jugador gana esta ronda rápida con un {VALUE_RANKS.get(player_rank_val, str(player_rank_val))}!")
        elif computer_rank_val > player_rank_val:
            print(f"\n¡La Computadora gana esta ronda rápida con un {VALUE_RANKS.get(computer_rank_val, str(computer_rank_val))}!")
        else:
            print("\n¡Empate en esta ronda rápida! Ambos sacaron la misma carta.")
        
        # Opciones para el jugador en el juego rápido
        while True:
            choice = input("\n¿Continuar jugando el juego rápido (c) o volver al Póker regular (v)? ").strip().lower()
            if choice == 'c':
                break # Continúa el bucle while True para otra ronda rápida
            elif choice == 'v':
                print("Volviendo al juego de Póker regular.")
                input("Presiona Enter para continuar...") # Pausa para que el usuario lea
                return False # Indica que el jugador decidió volver
            else:
                print("Opción inválida. Por favor, ingresa 'c' para continuar o 'v' para volver.")

def main():
    print("¡Bienvenido al juego de Póker en Consola!")

    # Bucle principal del juego
    # 'game_state' puede ser 'POKER' o 'QUICK_GAME'
    game_state = 'POKER' 
    current_deck = None # El mazo actual, persistirá entre rondas rápidas

    while True:
        if game_state == 'POKER':
            clear_console()
            print("\n--- Iniciando Nueva Partida de Póker Regular ---")
            # Inicializar Deck y Players para la nueva ronda de póker
            current_deck = Deck() # Se crea un nuevo mazo completo
            current_deck.shuffle()
            player = Player("Jugador")
            computer = Player("Computadora")

            player_won_poker_round = _play_round_poker(current_deck, player, computer)

            if player_won_poker_round:
                game_state = 'QUICK_GAME' # El jugador ganó el póker, pasa al juego rápido
                # Las instancias de player y computer, y el current_deck se mantienen para el quick game
                # Las manos de player y computer ya están vacías por la lógica de _play_round_poker
                print("\n¡Pasando al juego rápido de Carta Más Alta!")
            else:
                # Si el jugador pierde o empata en póker, se le da la opción de reiniciar o salir
                game_state = 'POKER' # Asegura que la próxima iteración inicie otro juego de póker
                play_again = input("\n¿Quieres jugar otra ronda de Póker regular? (s/n): ").strip().lower()
                if play_again != 's' and play_again != 'si':
                    print("\n¡Gracias por jugar! ¡Hasta la próxima!")
                    break # Salir del juego principal

        elif game_state == 'QUICK_GAME':
            clear_console()
            # Asegurarse de que player y computer no tengan cartas de la ronda anterior
            # Se recrean para asegurar manos vacías, pero se usa el current_deck restante
            # Ojo: Si la lógica de player.add_cards es que extiende, no resetea,
            # Asegurarse de vaciar las manos antes de _play_quick_game si es necesario.
            # En nuestro caso, Player se crea por ronda de Poker, no es un Player "persistente"
            # por lo que para el quick game necesitamos que las manos estén limpias.
            # Para este caso, como player y computer se crean nuevos en 'POKER' state,
            # sus manos están vacias. Pero si _play_round_poker limpia las manos al inicio
            # o los _play_quick_game usan deal, podemos reusar los objetos Player.
            
            # Para asegurar manos limpias en cada sub-ronda de Quick Game:
            player.hand = []
            computer.hand = []

            deck_exhausted = _play_quick_game(current_deck, player, computer)

            if deck_exhausted:
                game_state = 'POKER' # Mazo agotado, vuelve a póker regular
                print("\nEl mazo se agotó en el juego rápido. Se inicia una nueva partida de Póker.")
                input("Presiona Enter para continuar...") # Pausa para que el usuario lea
            else:
                # El jugador eligió volver al póker regular
                game_state = 'POKER'
                print("\nEl jugador decidió volver al juego de Póker regular.")
                input("Presiona Enter para continuar...") # Pausa para que el usuario lea
        
        else:
            # Estado de juego desconocido, por seguridad.
            print("Error: Estado de juego desconocido. Saliendo.")
            break

if __name__ == "__main__":
    main()