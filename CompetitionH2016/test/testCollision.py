from util import Collision
from RULEngine.Util.Position import Position


def test_init():
    l = [Position(0, 0), Position(100, 200)]
    c = Collision(l)
    assert c.field_objects == l


def test_collision():
    l = [Position(0, 0), Position(100, 200)]
    c = Collision(l)
    for i in c.field_objects:
        print(type(i))
        print(i)
    assert c.collision(Position(0, 0)) == True
    assert c.collision(Position(700, 300)) == False
