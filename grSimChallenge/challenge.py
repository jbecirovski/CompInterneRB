#!/usr/bin/python

import xml.etree.ElementTree as ET
from collections import namedtuple
import re
import random

Robot = namedtuple('Robot', ['id', 'x', 'y', 'theta'])
Ball = namedtuple('Ball', ['x', 'y', 'vx', 'vy'])

range_re = re.compile('\[(.*?),(.*?)\]')

class Challenge:

    def __init__(self, node):
        self.node = node
        self.reload()

    def reload(self):
        node = self.node
        self.name = node.find('Name').text
        self.description = node.find('Description').text
        self.yellow = self._loadTeam(node.find('Robots').find('TeamYellow'))
        self.blue = self._loadTeam(node.find('Robots').find('TeamBlue'))
        self.ball = self._loadBall(node.find('Ball'))
        try:
            self.strategy = node.find('Strategy').text
        except AttributeError:
            self.strategy = 'halt'

    def _loadBall(self, ball_node):

        x = float(ball_node.attrib['x'])
        y = float(ball_node.attrib['y'])
        try:
            vx = float(ball_node.attrib['vy'])
        except KeyError:
            vx = 0
        try:
            vy = float(ball_node.attrib['vy'])
        except KeyError:
            vy = 0

        return Ball(x, y, vx, vy)

    def _loadTeam(self, team_node):
        team = {}

        def getRandomPosition(range_x, range_y):
            while True:
                x = random.uniform(*range_x)
                y = random.uniform(*range_y)

                this_team_collision = any(((robot.x-x)**2 + (robot.y-y)**2) < 0.16 for robot in team.values())
                other_team_collision = False
                try:
                    other_team_collision = other_team_collision or any(((robot.x-x)**2 + (robot.y-y)**2) < 0.16 for robot in self.blue.values())
                except AttributeError:
                    pass
                try:
                    other_team_collision = other_team_collision or any(((robot.x-x)**2 + (robot.y-y)**2) < 0.16 for robot in self.yellow.values())
                except AttributeError:
                    pass

                if not (this_team_collision or other_team_collision):
                    break

            return (x,y)


        for robot in team_node.findall('Robot'):
            id = self._readNumber(robot.attrib['id'])
            x = self._readNumber(robot.attrib['x'])
            y = self._readNumber(robot.attrib['y'])
            try:
                theta = float(robot.attrib['theta'])
            except KeyError:
                theta = 0

            def getRobot(id):
                if isinstance(x, tuple):
                    rx, ry = getRandomPosition(x, y)
                else:
                    rx = x
                    ry = y
                return Robot(int(id), rx, ry, theta)


            if isinstance(id, tuple):
                for i in range(int(id[0]), int(id[1]+1)):
                    team[i] = getRobot(i)
            else:
                team[id] = getRobot(id)

        return team

    def _readNumber(self, attr):
        match = range_re.match(attr)
        if match:
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            return (num1, num2)
        else:
            return float(attr)



def load_challenges(path):
        tree = ET.parse(path)
        root = tree.getroot()
        return [Challenge(node) for node in root.iter('Challenge')]
