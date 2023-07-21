class Launcher:

    @staticmethod
    def restart(label_score, bouton_redemarrer, choisir_categorie):
        """
        Redémarre le jeu en supprimant les éléments affichés,
        puis en appelant la méthode pour choisir une catégorie.
        
        :param label_score: Le label affichant le score du joueur.
        :param bouton_redemarrer: Le bouton pour redémarrer le jeu.
        :param choisir_categorie: La méthode pour choisir une catégorie.
        """
        label_score.destroy()
        bouton_redemarrer.destroy()
        choisir_categorie()

    @staticmethod
    def lancer_jeu(bouton_demarrer, choisir_categorie):
        """
        Lance le jeu en supprimant le bouton de démarrage,
        puis en appelant la méthode pour choisir une catégorie.
        
        :param bouton_demarrer: Le bouton de démarrage du jeu.
        :param choisir_categorie: La méthode pour choisir une catégorie.
        """
        bouton_demarrer.destroy()
        choisir_categorie()
