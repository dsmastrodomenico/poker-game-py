# main.py

from deck import Deck
from player import Player
from hand_evaluator import compare_hands, RANK_VALUES, VALUE_RANKS
import os 
import time 

def clear_console():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Constantes para el sistema de apuestas ---
STARTING_CHIPS = 1000 # Fichas iniciales para cada jugador
ANTE_AMOUNT = 10     # Apuesta inicial por ronda de póker

def _play_round_poker(deck, player, computer):
    """
    Encapsula la lógica de una única ronda de póker con apuestas.
    Retorna (True, pot) si el Jugador gana la ronda de póker, (False, 0) si pierde o empata.
    Si un jugador no puede cubrir el ante, el juego principal termina.
    """
    print("\n--- Iniciando Ronda de Póker ---")
    
    current_pot = 0 # El bote para esta ronda

    # Verificar si los jugadores tienen suficientes fichas para el ante
    if player.chips < ANTE_AMOUNT:
        print(f"¡{player.name} no tiene suficientes fichas para el ante! Fichas: {player.chips}")
        return None, None # Indicar que no se puede jugar la ronda
    if computer.chips < ANTE_AMOUNT:
        print(f"¡{computer.name} no tiene suficientes fichas para el ante! Fichas: {computer.chips}")
        return None, None # Indicar que no se puede jugar la ronda

    # Ambos jugadores ponen el ante en el bote
    try:
        current_pot += player.bet(ANTE_AMOUNT)
        current_pot += computer.bet(ANTE_AMOUNT)
        print(f"\nAmbos jugadores ponen {ANTE_AMOUNT} fichas de ante. Bote actual: {current_pot} fichas.")
    except ValueError as e:
        # Esto no debería ocurrir si ya verificamos las fichas, pero es una buena práctica
        print(f"Error al apostar el ante: {e}")
        return None, None
        
    # Limpiar manos antes de repartir
    player.hand = []
    computer.hand = []

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
        print(f"Fichas de {player.name}: {player.chips} | Fichas de {computer.name}: {computer.chips} | Bote: {current_pot}") # Mostrar fichas
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
        print(f"\n🏆 ¡Felicidades! ¡El Jugador gana la ronda de Póker y se lleva {current_pot} fichas! 🏆")
        player.receive_chips(current_pot)
        return True, current_pot # El jugador ganó, devuelve el bote para el juego rápido
    elif winner == 2:
        print(f"\n🤖 ¡La Computadora gana la ronda de Póker y se lleva {current_pot} fichas!")
        computer.receive_chips(current_pot)
        return False, 0 # La computadora ganó o hubo empate, no hay bote para el juego rápido
    else:
        print("\n🤝 ¡Es un empate! El bote se divide.")
        player.receive_chips(current_pot // 2) # Divide el bote si es impar, uno se lleva un poco más
        computer.receive_chips(current_pot - (current_pot // 2)) # El resto para el otro
        return False, 0 # Empate, no hay juego rápido


def _play_quick_game(deck, player, computer, quick_game_pot): # Añadir quick_game_pot
    """
    Mecánica de juego rápido de "carta más alta".
    Usa las cartas restantes del mazo de la ronda de póker.
    Retorna True si el mazo se agotó, False si el jugador decide detenerse o pierde.
    """
    print("\n--- Iniciando Juego Rápido: ¡Carta Más Alta! ---")
    print(f"¡El bote del juego rápido es de {quick_game_pot} fichas!") # Mostrar el bote inicial
    
    while True:
        clear_console() 
        print("\n--- Juego Rápido: ¡Carta Más Alta! ---")
        print(f"Fichas de {player.name}: {player.chips} | Fichas de {computer.name}: {computer.chips} | Bote Juego Rápido: {quick_game_pot}") # Mostrar fichas y bote rápido
        print(f"Cartas restantes en el mazo: {len(deck)}")

        if len(deck) < 2: # Necesitamos al menos 2 cartas para que cada uno saque una
            print("\n¡El mazo se ha agotado para el juego rápido! Volviendo al Póker regular.")
            input("Presiona Enter para continuar...") 
            return True, quick_game_pot # Indica que el mazo se agotó, devuelve el bote restante

        input("\nPresiona Enter para sacar una carta...")
        
        # Sacar una carta para cada uno
        player_card = deck.deal(1)[0]
        computer_card = deck.deal(1)[0]

        # Mano temporal para el Jugador
        temp_player = Player("Jugador") # Se recrea, no necesita fichas para display
        temp_player.add_cards([player_card])
        print("\nTu carta:")
        temp_player.display_hand()

        # Mano temporal para la Computadora
        temp_computer = Player("Computadora") # Se recrea, no necesita fichas para display
        temp_computer.add_cards([computer_card])
        print("\nLa carta de la Computadora:")
        temp_computer.display_hand()

        player_rank_val = RANK_VALUES[player_card.rank]
        computer_rank_val = RANK_VALUES[computer_card.rank]

        if player_rank_val > computer_rank_val:
            quick_game_pot *= 2 # Dobla el bote
            print(f"\n¡El Jugador gana esta ronda rápida con un {VALUE_RANKS.get(player_rank_val, str(player_rank_val))}! ¡Bote duplicado a {quick_game_pot}!")
            # Si el jugador gana, se le da la opción de continuar
            while True:
                choice = input("\n¿Continuar jugando el juego rápido (c) o volver al Póker regular (v)? ").strip().lower()
                if choice == 'c':
                    break # Continúa el bucle while True para otra ronda rápida
                elif choice == 'v':
                    print(f"Volviendo al juego de Póker regular. Te llevas {quick_game_pot} fichas.")
                    player.receive_chips(quick_game_pot) # El jugador se lleva el bote actual
                    input("Presiona Enter para continuar...") 
                    return False, 0 # Indica que el jugador decidió volver
                else:
                    print("Opción inválida. Por favor, ingresa 'c' para continuar o 'v' para volver.")

        elif computer_rank_val > player_rank_val:
            print(f"\n¡La Computadora gana esta ronda rápida con un {VALUE_RANKS.get(computer_rank_val, str(computer_rank_val))}! ¡Has perdido el bote de {quick_game_pot} fichas!")
            print("El juego rápido ha terminado. Volviendo al Póker regular.")
            input("Presiona Enter para continuar...") 
            return False, 0 # El jugador perdió, se termina el juego rápido y pierde el bote

        else: # Empate
            print("\n¡Empate en esta ronda rápida! Ambos sacaron la misma carta. El bote se mantiene.")
            # Si es empate, se le da la opción de continuar
            while True:
                choice = input("\n¿Continuar jugando el juego rápido (c) o volver al Póker regular (v)? ").strip().lower()
                if choice == 'c':
                    break # Continúa el bucle while True para otra ronda rápida
                elif choice == 'v':
                    print(f"Volviendo al juego de Póker regular. Te llevas {quick_game_pot} fichas.")
                    player.receive_chips(quick_game_pot) # El jugador se lleva el bote actual
                    input("Presiona Enter para continuar...") 
                    return False, 0 # Indica que el jugador decidió volver
                else:
                    print("Opción inválida. Por favor, ingresa 'c' para continuar o 'v' para volver.")


def main():
    print("¡Bienvenido al juego de Póker en Consola!")
    print(f"Cada jugador comienza con {STARTING_CHIPS} fichas. El ante por ronda es de {ANTE_AMOUNT} fichas.")

    # Inicializar jugadores con fichas al inicio del juego completo
    # Estas instancias de Player son persistentes a través de las rondas de poker y quick game
    player = Player("Jugador", STARTING_CHIPS)
    computer = Player("Computadora", STARTING_CHIPS)

    # Bucle principal del juego
    game_state = 'POKER' 
    current_deck = None 
    quick_game_current_pot = 0 # Para persistir el bote del juego rápido

    while True:
        # Verificar si algún jugador se quedó sin fichas para terminar el juego principal
        if player.chips <= 0:
            print(f"\n¡{player.name} se ha quedado sin fichas! ¡GAME OVER!")
            break
        if computer.chips <= 0:
            print(f"\n¡La Computadora se ha quedado sin fichas! ¡GANASTE EL JUEGO!")
            break

        if game_state == 'POKER':
            clear_console()
            print(f"\n--- Nueva Partida de Póker Regular ---")
            print(f"Fichas de {player.name}: {player.chips} | Fichas de {computer.name}: {computer.chips}")

            current_deck = Deck() 
            current_deck.shuffle()
            
            # Limpiar manos antes de la ronda de poker (si los objetos player/computer son persistentes)
            # Ya se hace dentro de _play_round_poker ahora
            
            # player_won_poker_round retorna (True/False/None, pot)
            player_won_poker_round, poker_round_pot = _play_round_poker(current_deck, player, computer)

            if poker_round_pot is None: # Si no se pudo jugar la ronda (ej. falta de fichas)
                print("No se pudo iniciar la ronda de póker. Saliendo del juego.")
                break # Sale del bucle principal

            if player_won_poker_round:
                game_state = 'QUICK_GAME'
                quick_game_current_pot = poker_round_pot # El bote ganado es el inicial para el juego rápido
                print("\n¡Pasando al juego rápido de Carta Más Alta!")
            else:
                game_state = 'POKER' 
                play_again = input("\n¿Quieres jugar otra ronda de Póker regular? (s/n): ").strip().lower()
                if play_again != 's' and play_again != 'si':
                    print("\n¡Gracias por jugar! ¡Hasta la próxima!")
                    break 

        elif game_state == 'QUICK_GAME':
            clear_console()
            # Asegurarse de que las manos de los jugadores estén vacías para el quick game
            player.hand = []
            computer.hand = []

            # _play_quick_game devuelve si el mazo se agotó y el bote final del juego rápido
            deck_exhausted, final_quick_game_pot = _play_quick_game(current_deck, player, computer, quick_game_current_pot)

            if deck_exhausted:
                # Si el mazo se agotó, el jugador ya se llevó el bote si ganó la última ronda rápida,
                # o lo perdió si la computadora ganó, o se lo quedó si empató y decidió continuar.
                # No hay que hacer nada más con final_quick_game_pot aquí.
                game_state = 'POKER' 
                print("\nEl mazo se agotó en el juego rápido. Se inicia una nueva partida de Póker.")
                input("Presiona Enter para continuar...") 
            else:
                # Si no se agotó el mazo, significa que el jugador perdió o decidió volver.
                # La lógica de recibir/perder el bote ya está dentro de _play_quick_game.
                game_state = 'POKER' 
                print("\nEl jugador decidió volver al juego de Póker regular o perdió en el juego rápido.")
                input("Presiona Enter para continuar...")
        
        else:
            print("Error: Estado de juego desconocido. Saliendo.")
            break

if __name__ == "__main__":
    main()