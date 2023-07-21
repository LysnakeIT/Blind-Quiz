from launcher import *
import tkinter as tk
import random
import pygame
import json
import unidecode

class BlindTest:

    def __init__(self):
        """
        Constructeur de la classe BlindTest.
        Initialise les données du jeu et lance l'interface.
        """
        pygame.init()
        self.fichier_config = open('./config/data.json')
        self.donnees = json.load(self.fichier_config)
        self.lanceur = Launcher()
        self.afficher_interface()

    def afficher_resultat(self, score, label_question, labels_reponses):
        """
        Affiche le résultat final du joueur à la fin du jeu.

        Args:
            score (int): Le score final du joueur.
            label_question (tk.Label): Le label de la question.
            labels_reponses (List[tk.Label]): La liste des labels des réponses.
        """
        for label in labels_reponses:
            label.destroy()

        label_question.destroy()

        label_score = tk.Label(
            self.fenetre,
            font=("Consolas", 30),
            fg="#333333"
        )
        label_score.pack(pady=(300, 90))
        label_score.configure(text=f"Score: {score}/14!")

        bouton_recommencer = tk.Button(
            self.fenetre,
            text="Essayer une autre catégorie",
            relief=tk.FLAT,
            font=("Times", 20),
            command=lambda: self.lanceur.restart(label_score, bouton_recommencer, self.choisir_categorie),
            background="#F5F5F5",
            fg="#333333"
        )
        bouton_recommencer.pack()

    def choisir_reponse(self, ret, choix, label_question, labels_reponses):
        """
        Vérifie la réponse choisie par le joueur et gère la suite du jeu.

        Args:
            ret (int): L'index de la question en cours.
            choix (tk.IntVar): La variable du choix de réponse du joueur.
            label_question (tk.Label): Le label de la question en cours.
            labels_reponses (List[tk.Label]): La liste des labels des réponses en cours.
        """
        index = ret
        reponse_choisie = choix.get()
        choix.set(-1)

        if self.longueur_questions > 1 or self.longueur_questions <= 13:
            if reponse_choisie == self.reponses[self.tact]:
                self.score += 1
        else:
            if reponse_choisie == self.reponses[index]:
                self.score += 1

        while self.questions_choisies[index] and self.longueur_questions <= 13:
            index = random.randint(0, 13)

        if self.longueur_questions <= 13:
            pygame.mixer.stop()
            self.son = pygame.mixer.Sound(self.audio[index])
            self.son.play()
            label_question.config(text=self.questions[index])
            for i, label_reponse in enumerate(labels_reponses):
                label_reponse['text'] = self.choix_reponses[index][i]
            self.longueur_questions += 1
            self.questions_choisies[index] = True
            self.tact = index
        else:
            self.son.stop()
            self.afficher_resultat(self.score, label_question, labels_reponses)

    def debut_blind_test(self):
        """
        Démarre le Blind Test avec une nouvelle question.
        """
        self.questions_choisies[self.index] = True

        label_question = tk.Label(
            self.fenetre,
            text=self.questions[self.index],
            font=("Consolas", 20, "bold"),
            width=500,
            justify="center",
            wraplength=600,
            fg="#333333"
        )
        label_question.pack(pady=(100, 80))

        choix = tk.IntVar()
        choix.set(-1)

        labels_reponses = []

        for i, reponse in enumerate(self.choix_reponses[self.index]):
            label_reponse = tk.Radiobutton(
                self.fenetre,
                text=reponse,
                font=("Consolas", 25),
                value=i,
                variable=choix,
                anchor=tk.CENTER,
                background="#0000FF",
                foreground="#F5F5F5",
                relief=tk.RAISED
            )
            label_reponse.pack(pady=13)
            label_reponse.config(
                command=lambda: self.choisir_reponse(self.index, choix, label_question, labels_reponses)
            )
            labels_reponses.append(label_reponse)

    def lancer_categorie(self, boutons_categories, label_categorie, nom_categorie):
        """
        Lance le Blind Test pour une nouvelle catégorie.

        Args:
            boutons_categories (List[tk.Button]): La liste des boutons des catégories.
            label_categorie (tk.Label): Le label indiquant de choisir une catégorie.
            nom_categorie (str): Le nom de la catégorie choisie.
        """
        for bouton in boutons_categories:
            bouton.destroy()
        label_categorie.destroy()

        self.questions_choisies = [False] * 14
        self.index = random.randint(0, 13)
        self.score = 0
        self.longueur_questions = 1
        self.tact = 0
        self.questions = self.donnees.get(nom_categorie).get('questions')
        self.choix_reponses = self.donnees.get(nom_categorie).get('reponsesPossible')
        self.audio = self.donnees.get(nom_categorie).get("audio")
        self.reponses = self.donnees.get(nom_categorie).get('reponses')
        self.debut_blind_test()

    def choisir_categorie(self):
        """
        Affiche les boutons pour choisir une catégorie.
        """
        label_categorie = tk.Label(
            self.fenetre,
            text="Choisis une catégorie",
            font=("Times", "35", "bold italic"),
            bg="#F5F5F5",
            foreground="#333333",
            width=20
        )
        label_categorie.pack(pady=70)

        categories = ["Musique", "Cinéma", "Séries", "VideoGames"]
        boutons_categories = []

        for i, categorie in enumerate(categories):
            nom = categorie
            bouton_categorie = tk.Button(
                self.fenetre,
                text=categorie,
                font=("Broadway 20"),
                bg="#F5F5F5",
                foreground="#333333",
                width=20,
                height=1,
                state=tk.DISABLED,
                command=lambda nom=unidecode.unidecode(nom.lower()): self.lancer_categorie(
                    boutons_categories, label_categorie, nom
                )
            )
            bouton_categorie.pack(pady=10)
            boutons_categories.append(bouton_categorie)

        boutons_categories[0].place(x=100, y=250)
        boutons_categories[0].config(state=tk.NORMAL)
        boutons_categories[1].place(x=675, y=250)
        boutons_categories[2].place(x=100, y=400)
        boutons_categories[3].place(x=675, y=400)

    def afficher_interface(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Blind Test")
        self.fenetre.geometry("1200x690")
        self.fenetre.wm_iconbitmap('./assets/images/logo.ico')
        self.fenetre.resizable(0, 0)

        image_fond = tk.PhotoImage(file='./assets/images/background.png')
        label_fond = tk.Label(self.fenetre, image=image_fond)
        label_fond.place(relwidth=1, relheight=1)

        image_demarrer = tk.PhotoImage(file="./assets/images/bouton_start.png")

        bouton_demarrer = tk.Button(
            self.fenetre,
            image=image_demarrer,
            relief=tk.FLAT,
            background="#2148c0",
            border=0
        )
        bouton_demarrer.pack(pady=300)
        bouton_demarrer.config(command=lambda: self.lanceur.lancer_jeu(bouton_demarrer, self.choisir_categorie))

        self.fenetre.mainloop()
        pygame.quit()

start_game = BlindTest()