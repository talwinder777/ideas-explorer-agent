from __future__ import annotations

import unittest

from app.opportunity_analysis.analyzer import rank_opportunities


class TestAnalyzer(unittest.TestCase):
    def test_rank_opportunities_passthrough(self):
        payload = [{"id": 1}, {"id": 2}]
        result = rank_opportunities(payload)
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()
