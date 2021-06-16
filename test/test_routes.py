import unittest
from piro.route import SynthesisRoutes


class RoutesTest(unittest.TestCase):
    def test_basic_route(self):
        # BaTiO3 example
        route = SynthesisRoutes("mp-5020")
        route.recommend_routes(temperature=298)


if __name__ == '__main__':
    unittest.main()
