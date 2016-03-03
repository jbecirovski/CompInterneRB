#!/usr/bin/python
import game_launcher
from game_launcher import Defi
from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position
from RULEngine.Game.Player import Player

class Defi1(Defi):


    def initialiser(self, coach, terrain, etats, equipe_bleu, equipe_jaune):
        self.etat = self.passer

    def passer(self, coach, terrain, etats, equipe_bleu, equipe_jaune):
        #coach.bouger(0, terrain.ball)  #bouger vers la balle en conservant l'orientation de depart
        #coach.bouger(0, terrain.ball, cible=terrain.ball)  #bouger vers la balle en visant la balle
        #coach.bouger(0, Position(), cible=terrain.ball)    #bouger vers le centre en visant la balle
        #coach.chercher_balle(1)
        #coach.lancer(2, Position(-3000,0))
        coach.bouger(0, Position(0,0))
        self.prochain_etat(self.passer2)

    def passer2(self, coach, terrain, etats, equipe_bleu, equipe_jaune):
        coach.bouger(1, Position(-3000, -1000))
        self.prochain_etat(self.termine)

    def termine(self, coach, terrain, etats, equipe_bleu, equipe_jaune):
        pass

game_launcher.start_game(Defi1())
