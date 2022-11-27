class Launcher:

    def restart(self, leScore, boutonRestart, choix_categories):
        leScore.destroy()
        boutonRestart.destroy()
        choix_categories()

    def lancer_game(self, boutonStart, choix_categories):
        boutonStart.destroy()
        choix_categories()