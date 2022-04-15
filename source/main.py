from Visuals import PyGameRenderer

if __name__ == "__main__":
    game = PyGameRenderer()
    game.start()
    print("Quitting")
    game.destroy()