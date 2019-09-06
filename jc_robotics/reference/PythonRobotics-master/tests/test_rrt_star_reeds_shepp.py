from unittest import TestCase

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))
                + "/../PathPlanning/RRTStarReedsShepp/")
sys.path.append(os.path.dirname(os.path.abspath(__file__))
                + "/../PathPlanning/ReedsSheppPath/")

try:
    import rrt_star_reeds_shepp as m
except:
    raise


print(__file__)


class Test(TestCase):

    def test1(self):
        m.show_animation = False
        m.main(maxIter=5)


if __name__ == '__main__':  # pragma: no cover
    test = Test()
    test.test1()
