from doc_node import doc_node
from typing import *
import wx  # type: ignore
from interface import appFrame


class appModel():
    NODE_RADIUS: int
    root: doc_node
    curr_node: doc_node
    active_node: Optional[doc_node]
    node_list: list
    panelSize: "wx.Point"
    max_depth: int

    def __init__(self):
        self.NODE_RADIUS = 15
        self.root = doc_node("", "", None)
        self.curr_node = self.root
        self.active_node = None
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


class appFrameInst(appFrame):
    model: appModel

    def __init__(self, parent):
        super().__init__(parent)
        self.model = appModel()

    def onUpdate(self, event):
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
        self.model.node_list = self.model.root.traverse()
        self.model.max_depth = self.model.root.get_max_depth()
        self.model.update_start_positions()
        self.Refresh()

    def onDelete(self, event):
        if self.model.curr_node.parent is not None:
            parent_node = self.model.curr_node.parent

            for index, node in enumerate(parent_node.children):
                if node == self.model.curr_node:
                    parent_node.children.pop(index)

            self.model.curr_node = parent_node

        self.model.node_list = self.model.root.traverse()
        self.model.max_depth = self.model.root.get_max_depth()
        self.model.update_start_positions()
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
            ) < self.model.NODE_RADIUS ** 2:
                new_node = node

        if self.model.active_node != new_node:
            self.model.active_node = new_node
            self.Refresh()

    def onTreeClick(self, event):
        if self.model.active_node is not None:
            self.model.curr_node = self.model.active_node
            self.editCtrl.SetValue(self.model.active_node.content)
            self.descCtrl.SetValue(self.model.active_node.desc)

        self.Refresh()

    def onOpenDoc(self, event):
        with wx.FileDialog(
            self, "Select .txt file", wildcard="Text files (*.txt)|*.txt",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as docOpenPrompt:
            if docOpenPrompt.ShowModal() == wx.ID_CANCEL:
                return

            path = docOpenPrompt.GetPath()
            with open(path, 'r') as docFile:
                doc_content = docFile.read()
                self.model.root = doc_node(doc_content, "", None)
                self.editCtrl.SetValue(self.model.root.content)
                self.descCtrl.SetValue(self.model.root.desc)
                self.model.curr_node = self.model.root
                self.Refresh()

    def onPaint(self, event):
        dc = wx.PaintDC(self.treePanel)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255)))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 5))
        self.model.panelSize = dc.GetSize()
        self.model.max_depth = self.model.root.get_max_depth()
        node_queue = [self.model.root]
        curr_queue_node = self.model.root

        while not len(node_queue) == 0:
            curr_queue_node = node_queue.pop(0)
            for node in curr_queue_node.children:
                node_queue.append(node)
                dc.SetPen(wx.Pen(wx.BLACK, 3))
                dc.DrawLine(
                    int((curr_queue_node.start + curr_queue_node.proportion / 2)
                        * self.model.panelSize[0]),
                    int((curr_queue_node.depth + 1) / (self.model.max_depth + 2)
                        * self.model.panelSize[1]),

                    int((node.start + node.proportion / 2) * self.model.panelSize[0]),
                    int((node.depth + 1) / (self.model.max_depth + 2) * self.model.panelSize[1]),
                )
            dc.SetPen(wx.Pen(wx.BLACK, 4))

            # Colour selected node
            if curr_queue_node == self.model.curr_node:
                dc.SetPen(wx.Pen(wx.RED, 4))

            # Colour active node, takes priority if selected and active nodes are the same
            if curr_queue_node == self.model.active_node:
                dc.SetPen(wx.Pen(wx.BLUE, 4))

            dc.DrawCircle(
                int((curr_queue_node.start + curr_queue_node.proportion / 2)
                    * self.model.panelSize[0]),
                int((curr_queue_node.depth + 1) / (self.model.max_depth + 2)
                    * self.model.panelSize[1]),
                self.model.NODE_RADIUS
            )


if __name__ == '__main__':
    mainApp = wx.App()
    mainFrame = appFrameInst(parent=None)
    mainFrame.Show()
    mainApp.MainLoop()
