from src.game import game_loop

if __name__ == "__main__":
    while True:
        if not game_loop():
            break
