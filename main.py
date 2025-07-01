# main.py

import random
from card import Card # Necesario si necesitas instanciar Card directamente en main (aunque no se hace aquí)
from deck import Deck
from player import Player
from hand_evaluator import evaluate_hand, compare_hands, RANK_VALUES # Importa las funciones y constantes necesarias

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
    player.display_hand(hide_all=False) # Asegúrate de que la mano del jugador sea visible

    # La mano del oponente SIEMPRE se muestra al efectuar la comparación
    print("\nLa mano de la Computadora es:")
    computer.display_hand(hide_all=False) # Ahora siempre se revela aquí
    
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