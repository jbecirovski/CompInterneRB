#!/usr/bin/python
import socket
from . import grSim_Packet_pb2 as grSim_Packet
from .grSim_Commands_pb2 import grSim_Robot_Command
from .grSim_Replacement_pb2 import grSim_RobotReplacement
from .grSim_Replacement_pb2 import grSim_BallReplacement
from .grSim_Replacement_pb2 import grSim_Replacement
import math


class grSimRemote():

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection_info = (host, port)
        self.server.connect(self.connection_info)
        self.packet = None

    def send_command(self, command):
        packet = grSim_Packet.grSim_Packet()
        #grSimCommand = grSim_Robot_Command()
        packet.commands.isteamyellow = command.team.is_team_yellow
        packet.commands.timestamp = 0
        grSimCommand = packet.commands.robot_commands.add()
        grSimCommand.id = command.player.id
        grSimCommand.wheelsspeed = False
        grSimCommand.veltangent = command.pose.position.x
        grSimCommand.velnormal = command.pose.position.y
        grSimCommand.velangular = command.pose.orientation * math.pi / 180
        grSimCommand.spinner = command.kick
        grSimCommand.kickspeedx = command.kick_speed
        grSimCommand.kickspeedz = 0

        #packet.commands.robot_commands.append(grSimCommand)

    def place_player(self, robot_id, is_team_yellow, x, y, theta=0):
        if self.packet:
            batched = True
            robot = self.packet.replacement.robots.add()
        else:
            batched = False
            packet = grSim_Packet.grSim_Packet()
            robot = packet.replacement.robots.add()

        robot.x = x
        robot.y = y
        robot.dir = theta
        robot.yellowteam = is_team_yellow
        robot.id = robot_id

        if not batched:
            self._send_packet(packet)

    def place_ball(self, x, y, vx=0, vy=0):
        if self.packet:
            batched = True
            ball = self.packet.replacement.ball
        else:
            batched = False
            packet = grSim_Packet.grSim_Packet()
            ball = packet.replacement.ball

        ball.x = x
        ball.y = y
        ball.vx = vx
        ball.vy = vy

        if not batched:
            self._send_packet(packet)

    def start_batch(self):
        self.packet = grSim_Packet.grSim_Packet()

    def end_batch(self):
        self._send_packet(self.packet)
        self.packet = None

    def abandon_batch(self):
        self.packet = None

    def _send_packet(self, packet):
        self.server.send(packet.SerializeToString())
