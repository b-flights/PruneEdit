from doc_node import doc_node
from interface import *
from platformdirs import user_config_dir
from typing import *
import json
import os
import wx  # type: ignore


class appModel():
    # Preferences
    node_radius: int
    node_thickness: int
    auto_update: bool
    update_behaviour: int

    root: doc_node
    curr_node: doc_node
    hover_node: Optional[doc_node]
    node_list: list
    panelSize: "wx.Point"
    max_depth: int

    def __init__(self):
        self.node_radius = 15
        self.node_thickness = 4
        self.auto_update = False
        self.update_behaviour = 0
        self.root = doc_node("", "", None)
        self.curr_node = self.root
        self.hover_node = None
        self.node_list = [self.root]
        self.panelSize = None
        self.max_depth = 0

    # Set the horizontal start positions of each node's visual strip
    def update_start_positions(self):
        self.root.distribute_proportion()
        node_queue = [self.root]
        curr_queue_node = self.root
        node_proportion = 0

        while not len(node_queue) == 0:
            node_proportion = 0
            curr_queue_node = node_queue.pop(0)
            for node in curr_queue_node.children:
                node_queue.append(node)
                node.start = node.parent.start + node_proportion
                node.y = node.depth / self.max_depth
                node_proportion += node.proportion

    # Update the layout attributes (depth, start, proportion) of all nodes
    def update_tree_attributes(self):
        self.node_list = self.root.traverse()
        self.max_depth = self.root.get_max_depth()
        self.update_start_positions()


class prefWindowInst(prefWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def onThicknessChange(self, event):
        self.parent.model.node_thickness = self.nodeThicknessSlider.GetValue()
        self.parent.Refresh()

    def onRadiusChange(self, event):
        self.parent.model.node_radius = self.nodeRadiusSlider.GetValue()
        self.parent.Refresh()

    def onAutoUpdateCheck(self, event):
        self.parent.model.auto_update = self.updateCheckBox.GetValue()

    def onUpdateChoice(self, event):
        self.parent.model.update_behaviour = self.updateChoiceBox.GetSelection()

    def onSavePref(self, event):
        app_settings = json.dumps({
            "node_thickness": self.parent.model.node_thickness,
            "node_radius": self.parent.model.node_radius,
            "auto_update": self.parent.model.auto_update,
            "update_behaviour": self.parent.model.update_behaviour
        })
        config_path = user_config_dir("PruneEdit")

        if not os.path.isdir(config_path):
            os.makedirs(config_path)

        with open(os.path.join(config_path, "config.json"), "w") as settings_file:
            settings_file.write(app_settings)

    def onWindowClose(self, event):
        self.Hide()


class appFrameInst(appFrame):
    model: appModel

    def __init__(self, parent):
        super().__init__(parent)
        self.model = appModel()
        self.settings = prefWindowInst(parent=self)

        config_path = os.path.join(user_config_dir("PruneEdit"), "config.json")

        if os.path.isfile(config_path):
            with open(config_path, "r") as settings_file:
                app_settings = json.loads(settings_file.read())
                self.model.node_thickness = app_settings["node_thickness"]
                self.model.node_radius = app_settings["node_radius"]
                self.model.auto_update = app_settings["auto_update"]
                self.model.update_behaviour = app_settings["update_behaviour"]

                self.settings.nodeThicknessSlider.SetValue(self.model.node_thickness)
                self.settings.nodeRadiusSlider.SetValue(self.model.node_radius)
                self.settings.updateCheckBox.SetValue(self.model.auto_update)
                self.settings.updateChoiceBox.SetSelection(self.model.update_behaviour)

    def onUpdate(self, event):
        # If the current node is an internal node, prompt
        if len(self.model.curr_node.children) != 0:
            with wx.MessageDialog(
                self,
                "The version being updated has child versions.",
                "Notice",
                wx.YES_NO
            ) as dialog:
                dialog.SetYesNoLabels("Discard Child Versions", "Save as New Version")
                option = dialog.ShowModal()

                if option == wx.ID_NO:
                    new_node = self.model.curr_node.add_new_ver(
                        self.editCtrl.GetValue(), self.descCtrl.GetValue()
                    )
                    self.model.curr_node = new_node

                elif option == wx.ID_YES:
                    self.model.curr_node.children = []

                self.model.update_tree_attributes()

        self.model.curr_node.update_content(
            self.editCtrl.GetValue(), self.descCtrl.GetValue()
        )
        self.Refresh()
        self.Update()

    def onSaveRev(self, event):
        new_node = self.model.curr_node.add_new_ver(
            self.editCtrl.GetValue(), self.descCtrl.GetValue()
        )
        self.model.curr_node = new_node
        self.model.update_tree_attributes()
        self.Refresh()

    def onNewBlank(self, event):
        new_node = self.model.curr_node.add_new_ver("", "")
        self.model.curr_node = new_node
        self.model.update_tree_attributes()

        self.editCtrl.ChangeValue(self.model.curr_node.content)
        self.descCtrl.ChangeValue(self.model.curr_node.desc)

        self.Refresh()

    def onSetMain(self, event):
        self.model.root = self.model.curr_node
        self.model.root.proportion = 1.0
        self.model.root.start = 0.0
        self.model.root.depth = 0
        self.model.root.parent = None
        self.model.update_tree_attributes()
        self.Refresh()

    def onDelete(self, event):
        if self.model.curr_node.parent is not None:
            parent_node = self.model.curr_node.parent

            for index, node in enumerate(parent_node.children):
                if node == self.model.curr_node:
                    parent_node.children.pop(index)

            self.model.curr_node = parent_node

        self.editCtrl.ChangeValue(self.model.curr_node.content)
        self.descCtrl.ChangeValue(self.model.curr_node.desc)

        self.model.update_tree_attributes()
        self.Refresh()

    def onDelChange(self, event):
        self.model.curr_node.children = []
        self.model.update_tree_attributes()
        self.Refresh()

    def onTreeToggle(self, event):
        if self.treePanel.IsShown():
            self.treePanel.Hide()
            self.toggleButton.SetLabel("Show\nTree")
        else:
            self.treePanel.Show()
            self.toggleButton.SetLabel("Hide\nTree")
        self.Layout()

    def onResizePanel(self, event):
        self.Refresh()

    def onMouseMove(self, event):
        new_node = None
        for node in self.model.node_list:
            x_pos = ((node.start + node.proportion / 2) * self.model.panelSize[0])
            y_pos = ((node.depth + 1) / (self.model.max_depth + 2) * self.model.panelSize[1])
            if (
                (x_pos - event.GetX()) ** 2 + (y_pos - event.GetY()) ** 2
            ) < self.model.node_radius ** 2:
                new_node = node

        if self.model.hover_node != new_node:
            self.model.hover_node = new_node
            self.Refresh()

    def onTreeClick(self, event):
        if self.model.hover_node is not None:
            self.model.curr_node = self.model.hover_node
            self.editCtrl.ChangeValue(self.model.hover_node.content)
            self.descCtrl.ChangeValue(self.model.hover_node.desc)

        self.Refresh()

    def onNewTree(self, event):
        with wx.MessageDialog(
            self,
            "Your current tree will be erased. Continue?",
            "Notice",
            wx.YES_NO
        ) as dialog:
            if dialog.ShowModal() != wx.ID_YES:
                return

        self.model.root = doc_node("", "", None)
        self.model.curr_node = self.model.root
        self.editCtrl.ChangeValue("")
        self.descCtrl.ChangeValue("")

        self.model.update_tree_attributes()
        self.Refresh()

    def onOpenDoc(self, event):
        with wx.FileDialog(
            self, "Select .txt file", wildcard="Text files (*.txt)|*.txt",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as docOpenPrompt:
            if docOpenPrompt.ShowModal() == wx.ID_CANCEL:
                return

            with wx.MessageDialog(
                self,
                "Your current tree will be erased. Continue?",
                "Notice",
                wx.YES_NO
            ) as dialog:
                if dialog.ShowModal() != wx.ID_YES:
                    return

            path = docOpenPrompt.GetPath()
            with open(path, 'r') as docFile:
                doc_content = docFile.read()
                self.model.root = doc_node(doc_content, "", None)
                self.editCtrl.ChangeValue(self.model.root.content)
                self.descCtrl.ChangeValue(self.model.root.desc)
                self.model.curr_node = self.model.root
                self.Refresh()

    def onSaveDoc(self, event):
        with wx.FileDialog(
            self, "Save .txt file", wildcard="Text files (*.txt)|*.txt",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as saveDocPrompt:
            if saveDocPrompt.ShowModal() == wx.ID_CANCEL:
                return

            path = saveDocPrompt.GetPath()
            with open(path, 'w') as treeFile:
                treeFile.write(self.model.curr_node.content)

    def onSaveTree(self, event):
        with wx.FileDialog(
            self, "Save tree file", wildcard="JSON files (*.json)|*.json",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as saveTreePrompt:
            if saveTreePrompt.ShowModal() == wx.ID_CANCEL:
                return

            path = saveTreePrompt.GetPath()
            with open(path, 'w') as treeFile:
                json_tree = json.dumps(self.model.root.create_tree_dict())
                treeFile.write(json_tree)

    def onOpenTree(self, event):
        with wx.FileDialog(
            self, "Select tree file", wildcard="JSON files (*.json)|*.json",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as openTreePrompt:
            if openTreePrompt.ShowModal() == wx.ID_CANCEL:
                return

            json_tree = {}
            path = openTreePrompt.GetPath()
            with open(path, 'r') as treeFile:
                json_tree = json.loads(treeFile.read())
                if json_tree is None:
                    with wx.MessageDialog(
                        self,
                        "The selected tree file is invalid.",
                        "Error"
                    ) as dialog:
                        dialog.ShowModal()
                        return

            with wx.MessageDialog(
                self,
                "Your current tree will be erased. Continue?",
                "Notice",
                wx.YES_NO
            ) as dialog:
                if dialog.ShowModal() != wx.ID_YES:
                    return

            self.model.root = doc_node("", "", None)
            self.model.root.load_tree_dict(json_tree)

        self.model.curr_node = self.model.root
        self.model.update_tree_attributes()

        self.editCtrl.ChangeValue(self.model.curr_node.content)
        self.descCtrl.ChangeValue(self.model.curr_node.desc)

        self.Refresh()

    def onOpenPrefs(self, event):
        self.settings.Show()

    def onOpenHelp(self, event):
        self.help = helpWindow(parent=self)
        self.help.Show()

    def handleUpdate(self):
        if self.model.auto_update:
            if len(self.model.curr_node.children) > 0:
                match self.model.update_behaviour:
                    # None
                    case 0:
                        return
                    # Save as New Version
                    case 1:
                        new_node = self.model.curr_node.add_new_ver(
                            self.editCtrl.GetValue(), self.descCtrl.GetValue()
                        )
                        self.model.curr_node = new_node
                    # Discard Child Versions
                    case 2:
                        self.model.curr_node.children = []

        else:
            return

        self.model.curr_node.update_content(
            self.editCtrl.GetValue(), self.descCtrl.GetValue()
        )
        self.model.update_tree_attributes()

        self.Refresh()
        self.Update()

    def onContentEdit(self, event):
        self.handleUpdate()

    def onDescEdit(self, event):
        self.handleUpdate()

    def onPaint(self, event):
        dc = wx.PaintDC(self.treePanel)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255)))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 5))
        self.model.panelSize = dc.GetSize()
        self.model.max_depth = self.model.root.get_max_depth()
        node_queue = [self.model.root]
        curr_queue_node = self.model.root

        # In-order traversal
        while not len(node_queue) == 0:
            curr_queue_node = node_queue.pop(0)

            # Draw lines between curr_queue_node and each child
            for node in curr_queue_node.children:
                node_queue.append(node)
                dc.SetPen(wx.Pen(wx.BLACK, int(self.model.node_thickness * 0.75)))
                dc.DrawLine(
                    int((curr_queue_node.start + curr_queue_node.proportion / 2)
                        * self.model.panelSize[0]),
                    int((curr_queue_node.depth + 1) / (self.model.max_depth + 2)
                        * self.model.panelSize[1]),

                    int((node.start + node.proportion / 2) * self.model.panelSize[0]),
                    int((node.depth + 1) / (self.model.max_depth + 2) * self.model.panelSize[1]),
                )
            dc.SetPen(wx.Pen(wx.BLACK, self.model.node_thickness))

            # Colour selected node
            if curr_queue_node == self.model.curr_node:
                dc.SetPen(wx.Pen(wx.RED, self.model.node_thickness))

            # Colour hover node, takes priority if selected and hover nodes are the same
            if curr_queue_node == self.model.hover_node:
                dc.SetPen(wx.Pen(wx.BLUE, self.model.node_thickness))

            # Draw current node in queue
            dc.DrawCircle(
                int((curr_queue_node.start + curr_queue_node.proportion / 2)
                    * self.model.panelSize[0]),
                int((curr_queue_node.depth + 1) / (self.model.max_depth + 2)
                    * self.model.panelSize[1]),
                self.model.node_radius
            )

        if self.model.hover_node is not None:
            dc.DrawText(self.model.hover_node.desc, 0, 0)


if __name__ == '__main__':
    mainApp = wx.App()
    mainFrame = appFrameInst(parent=None)
    mainFrame.Show()
    mainApp.MainLoop()
