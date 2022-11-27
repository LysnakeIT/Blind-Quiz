from launcher import *
from tkinter import*
import random
import pygame
import json
import unidecode

class BlindTest:

	arrayQuestion = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
	index = random.randint(0,13)
	score = 0
	questionsLength = 1
	tact = 0

	def __init__(self):

		pygame.init()

		self.fileConfig = open('./config/data.json')
		self.data = json.load(self.fileConfig)

		self.launcher = Launcher()

		self.display()

	def displayResultat(self, score, laQuestion, rep1, rep2, rep3, rep4):
		laQuestion.destroy()
		rep1.destroy()
		rep2.destroy()
		rep3.destroy()
		rep4.destroy()

		self.leScore = Label(
			self.window,
			font = ("Consolas", 30),
			fg="#333333")

		self.leScore.pack(pady=(300, 90))

		self.leScore.configure(text="Score :"+ str(score) + "/14 !")

		self.boutonRestart = Button(
			self.window,
			text = "Essayer une autre catégorie",
			relief = FLAT,
			font = ("Times", 20),
			command = lambda : self.launcher.restart(self.leScore, self.boutonRestart, self.choix_categories),
			background = "#F5F5F5",
			fg="#333333")
		self.boutonRestart.pack()


	def choice_answer(self, ret, choice, laQuestion, rep1, rep2, rep3, rep4) :
		index = ret
		leChoix = choice.get()
		choice.set(-1)
		if self.questionsLength > 1 or self.questionsLength <= 13:
			if (leChoix == self.reponses[self.tact]):
				self.score = self.score + 1
		else :
			if (leChoix == self.reponses[index]):
				self.score = self.score + 1

		while self.arrayQuestion[index] == True and self.questionsLength <= 13:
			index = random.randint(0,13)

		if self.questionsLength <= 13:
			pygame.mixer.stop()
			self.son = pygame.mixer.Sound(self.audio[index])
			self.son.play()
			laQuestion.config(text= self.questions[index])
			rep1['text'] = self.choix_reponses[index][0]
			rep2['text'] = self.choix_reponses[index][1]
			rep3['text'] = self.choix_reponses[index][2]
			rep4['text'] = self.choix_reponses[index][3]
			self.questionsLength += 1
			self.arrayQuestion[index] = True
			self.tact = index
		else:
			self.son.stop()
			self.displayResultat(self.score, laQuestion, rep1, rep2, rep3, rep4)

	def start_blindtest(self):
		self.arrayQuestion[self.index] = True

		laQuestion = Label(
			self.window,
			text = self.questions[self.index],
			font = ("Consolas", 20, "bold"),
			width = 500,
			justify = "center",
			wraplength = 600,
			fg="#333333")

		leSon = pygame.mixer.Sound (self.audio[self.index])
		leSon.play()
		laQuestion.pack(pady=(100, 80))

		choice = IntVar()
		choice.set(-1)

		rep1 = Radiobutton(
			self.window,
			text = self.choix_reponses[self.index][0],
			font = ("Consolas", 25),
			value = 0,
			variable = choice,
			anchor=CENTER,
			background = "#0000FF",
			foreground = "#F5F5F5",
			relief= RAISED)
		rep1.pack(pady=13)

		rep2 = Radiobutton(
			self.window,
			text = self.choix_reponses[self.index][1],
			font = ("Consolas", 25),
			value = 1,
			variable = choice,
			anchor=CENTER,
			background = "#0000FF",
			foreground = "#F5F5F5",
			relief= RAISED)
		rep2.pack(pady=13)

		rep3 = Radiobutton(
			self.window,
			text = self.choix_reponses[self.index][2],
			font = ("Consolas", 25),
			value = 2,
			variable = choice,
			anchor=CENTER,
			background = "#0000FF",
			foreground = "#F5F5F5",
			relief= RAISED)
		rep3.pack(pady=13)

		rep4 = Radiobutton(
			self.window,
			text = self.choix_reponses[self.index][3],
			font = ("Consolas", 25),
			value = 3,
			variable = choice,
			anchor=CENTER,
			background = "#0000FF",
			foreground = "#F5F5F5",
			relief= RAISED)
		rep4.pack(pady=13)

		rep1.config(command = lambda : self.choice_answer(self.index, choice, laQuestion, rep1, rep2, rep3, rep4))
		rep2.config(command = lambda : self.choice_answer(self.index, choice, laQuestion, rep1, rep2, rep3, rep4))
		rep3.config(command = lambda : self.choice_answer(self.index, choice, laQuestion, rep1, rep2, rep3, rep4))
		rep4.config(command = lambda : self.choice_answer(self.index, choice, laQuestion, rep1, rep2, rep3, rep4))	

	def lancer_categorie(self, listeBoutonCategorie, labelCategorie, nomCategorie):
		for i in listeBoutonCategorie:
			i.destroy()
		labelCategorie.destroy()
		self.arrayQuestion = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
		self.index = random.randint(0,13)
		self.score = 0
		self.questionsLength = 1
		self.tact = 0
		self.questions = self.data.get(nomCategorie).get('questions')
		self.choix_reponses = self.data.get(nomCategorie).get('reponsesPossible')
		self.audio = self.data.get(nomCategorie).get("audio")
		self.reponses = self.data.get(nomCategorie).get('reponses')
		self.start_blindtest()

	def choix_categories(self):
		labelCategorie = Label(
			self.window,
			text = "Choisis une catégorie",
			font = ("Times", "35", "bold italic"),
			bg ="#F5F5F5",
			foreground = "#333333",
			width = 20)
		labelCategorie.pack(pady=70)

		listeCategorie = ["Musique", "Cinéma", "Séries", "VideoGames"]
		listeBoutonCategorie = []

		for i in listeCategorie:
			name = i
			i = Button(
				self.window,
				text = i,
				font = ("Broadway 20"),
				bg ="#F5F5F5",
				foreground = "#333333",
				width = 20,
				height = 1,
				state = DISABLED,
				command = lambda name = unidecode.unidecode(name.lower()): self.lancer_categorie(listeBoutonCategorie, labelCategorie, name))
			i.pack(pady=10)
			listeBoutonCategorie.append(i)
		listeBoutonCategorie[0].place(x=100, y=250)
		listeBoutonCategorie[0].config(state = NORMAL)
		listeBoutonCategorie[1].place(x=675, y=250)
		listeBoutonCategorie[2].place(x=100, y=400)
		listeBoutonCategorie[3].place(x=675, y=400)

	def display (self):
		self.window = Tk()
		self.window.title("Blind Test")
		self.window.geometry("1200x690")
		self.window.wm_iconbitmap('./assets/images/logo.ico')
		self.window.resizable(0,0)

		background_image = PhotoImage(file='./assets/images/background.png')
		background_label = Label(self.window, image=background_image)
		background_label.place(relwidth=1, relheight=1)

		imageStart = PhotoImage(file="./assets/images/bouton_start.png")

		boutonStart = Button(
			self.window,
			image = imageStart,
			relief = FLAT,
			background = "#2148c0",
			border = 0)
		boutonStart.pack(pady=300)
		boutonStart.config(command = lambda : self.launcher.lancer_game(boutonStart, self.choix_categories))

		self.window.mainloop()
		pygame.quit()

startGame = BlindTest()