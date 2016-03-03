#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from challenge import load_challenges
from communication.grSimRemote import grSimRemote
from RULEngine.Framework import Framework
from ChallengeStrategy import ChallengeStrategy
from RULEngine.Game.Referee import Command as RefCommand


class CompetitionGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.remote = grSimRemote("127.0.0.1", 20011)

        self.framework = Framework(is_team_yellow = True)
        self.framework.start_game(ChallengeStrategy, async=True)
        self.strategie = self.framework.strategy

        loadUi("roboul_main.ui", self)

        self.challenges = load_challenges("challenges.xml")

        self.defis_comboBox.currentIndexChanged.connect(self.change_challenge)
        for challenge in self.challenges:
            self.defis_comboBox.addItem(challenge.name, challenge)

        self.resetButton.clicked.connect(self.reset)
        self.startButton.toggled.connect(self.startstop)

        self.show()

    def reset(self):
        self.change_challenge(self.defis_comboBox.currentIndex())

    def startstop(self, start):
        if start:
            command = "NORMAL_START"
        else:
            command = "HALT"

        self.framework.game.referee.command = RefCommand(command)

    def change_challenge(self, challenge_index):

        challenge = self.defis_comboBox.itemData(challenge_index)
        challenge.reload()

        self.remote.start_batch()

        for robot_id, robot in challenge.blue.items():
            self.remote.place_player(robot.id, False,
                                     robot.x, robot.y, robot.theta)

        for robot_id, robot in challenge.yellow.items():
            self.remote.place_player(robot.id, True,
                                     robot.x, robot.y, robot.theta)


        ball = challenge.ball
        self.remote.place_ball(ball.x, ball.y, ball.vx, ball.vy)

        self.remote.end_batch()

        self.description_label.setText(challenge.description)

        self.strategie.set_mode(challenge.strategy)

    def closeEvent(self,event):
        self.framework.stop_game()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    roboul_main = CompetitionGUI()
    sys.exit(app.exec_())
