from RULEngine.Strategy.Strategy import Strategy
from RULEngine.Command import Command
from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position
from RULEngine.Util.geometry import intercept
import sys, time

__author__ = 'jbecirovski'

class ChallengeStrategy(Strategy):
    def __init__(self, field, referee, team, opponent_team, is_team_yellow=False):
        Strategy.__init__(self, field, referee, team, opponent_team)

        self.team.is_team_yellow = is_team_yellow
        self.on_start = self.halt

    def set_mode(self, value):
        self.on_start = getattr(self, value, self.halt)

    def halt(self):
        pass

    def center(self):
        self._send_command(Command.MoveTo(self.team.players[0], self.team, Position(0,0)))

    def goaler(self):
        player = self.team.players[0]
        balle = self.field.ball.position
        couvrir = Position(4500, 0)
        threshold = 500

        position = intercept(player, balle, couvrir, threshold)
        self._send_command(Command.MoveTo(self.team.players[0], self.team, position))

    def on_halt(self):
        pass

    def on_stop(self):
        pass
