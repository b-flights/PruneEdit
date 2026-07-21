import sys
import unittest
import wx
import json

sys.path.append("../src")
from main import appModel


class TestTreeOperations(unittest.TestCase):
    def test_traversal(self):
        model = appModel()
        model.root.add_new_ver("Test", "Node A")
        model.root.add_new_ver("Test", "Node B")
        model.root.add_new_ver("Test", "Node C")
        model.root.children[0].add_new_ver("Test", "Node D")

        self.assertEqual(len(model.root.traverse()), 5)

    def test_proportion(self):
        model = appModel()
        model.root.add_new_ver("Test", "Node A")
        model.root.add_new_ver("Test", "Node B")
        model.root.add_new_ver("Test", "Node C")
        model.root.children[0].add_new_ver("Test", "Node D")
        model.root.children[0].add_new_ver("Test", "Node E")
        model.root.distribute_proportion()

        self.assertAlmostEqual(model.root.children[0].proportion, 1/3)
        self.assertAlmostEqual(model.root.children[0].children[0].proportion, 1/6)

    def test_start_pos(self):
        model = appModel()
        model.root.add_new_ver("Test", "Node A")
        model.root.add_new_ver("Test", "Node B")
        model.root.add_new_ver("Test", "Node C")
        model.root.children[0].add_new_ver("Test", "Node D")
        model.root.children[0].add_new_ver("Test", "Node E")
        model.update_tree_attributes()

        self.assertAlmostEqual(model.root.children[0].start, 0)
        self.assertAlmostEqual(model.root.children[1].start, 1/3)
        self.assertAlmostEqual(model.root.children[0].children[1].proportion, 1/6)

    def test_load(self):
        model = appModel()
        json_tree = {}
        with open("test_tree.json", 'r') as treeFile:
            json_tree = json.loads(treeFile.read())

        model.root.load_tree_dict(json_tree)

        self.assertEqual(len(model.root.children), 2)
        self.assertEqual(len(model.root.children[1].children), 3)

    def test_update(self):
        model = appModel()
        model.root.update_content("Test content", "Test description")

        self.assertEqual(model.root.content, "Test content")
        self.assertEqual(model.root.desc, "Test description")


if __name__ == '__main__':
    unittest.main()
