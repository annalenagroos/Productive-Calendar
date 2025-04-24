import unittest
from database import add_event, get_events

class TestDatabase(unittest.TestCase):
    def test_add_event(self):
        event = {"title": "Test", "date": "2025-01-01"}  # 'category' entfernt
        add_event(**event)
        events = get_events()
        self.assertTrue(any(e["title"] == "Test" for e in events))

if __name__ == "__main__":
    unittest.main()