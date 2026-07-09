from doc_node import doc_node
from typing import *
import wx  # type: ignore
from interface import appFrame

NODE_RADIUS = 15
root: doc_node = doc_node("", "", None)
curr_node: doc_node = root
active_node: Optional[doc_node] = None
node_list: list = []
panelSize = None
max_depth: int = 0


# Set the horizontal start positions of each node's visual strip
def update_start_positions():
    root.distribute_proportion()
    node_queue = [root]
    curr_queue_node = root
    node_proportion = 0

    while not len(node_queue) == 0:
        node_proportion = 0
        curr_queue_node = node_queue.pop(0)
        for node in curr_queue_node.children:
            node_queue.append(node)
            node.start = node.parent.start + node_proportion
            node.y = node.depth / max_depth
            node_proportion += node.proportion


node_list = root.traverse()
max_depth = root.get_max_depth()


class appFrameInst(appFrame):
    def onUpdate(self, event):
        curr_node.update_content(
            self.editCtrl.GetValue(), self.descCtrl.GetValue()
        )
        self.Refresh()
        self.Update()

    def onSaveRev(self, event):
        global curr_node
        global max_depth
        global node_list
        new_node = curr_node.add_new_ver(
            self.editCtrl.GetValue(), self.descCtrl.GetValue()
        )
        curr_node = new_node
        node_list = root.traverse()
        max_depth = root.get_max_depth()
        update_start_positions()
        self.Refresh()

    def onDelete(self, event):
        global curr_node
        global max_depth
        global node_list
        if curr_node.parent is not None:
            parent_node = curr_node.parent

            for index, node in enumerate(parent_node.children):
                if node == curr_node:
                    parent_node.children.pop(index)

            curr_node = parent_node

        node_list = root.traverse()
        max_depth = root.get_max_depth()
        update_start_positions()
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
        global active_node
        new_node = None
        for node in node_list:
            if (
                (((node.start + node.proportion / 2) * panelSize[0]) - event.GetX()) ** 2
                + (((node.depth + 1) / (max_depth + 2) * panelSize[1]) - event.GetY()) ** 2
            ) < NODE_RADIUS ** 2:
                new_node = node

        if active_node != new_node:
            active_node = new_node
            self.Refresh()

    def onTreeClick(self, event):
        global curr_node
        if active_node is not None:
            curr_node = active_node
            self.editCtrl.SetValue(active_node.content)
            self.descCtrl.SetValue(active_node.desc)

        self.Refresh()

    def onPaint(self, event):
        global panelSize
        dc = wx.PaintDC(self.treePanel)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255)))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 5))
        panelSize = dc.GetSize()
        max_depth = root.get_max_depth()
        node_queue = [root]
        curr_queue_node = root

        while not len(node_queue) == 0:
            curr_queue_node = node_queue.pop(0)
            for node in curr_queue_node.children:
                node_queue.append(node)
                dc.SetPen(wx.Pen(wx.BLACK, 3))
                dc.DrawLine(
                    int((curr_queue_node.start + curr_queue_node.proportion / 2)
                        * panelSize[0]),
                    int((curr_queue_node.depth + 1) / (max_depth + 2)
                        * panelSize[1]),

                    int((node.start + node.proportion / 2) * panelSize[0]),
                    int((node.depth + 1) / (max_depth + 2) * panelSize[1]),
                )
            dc.SetPen(wx.Pen(wx.BLACK, 4))

            # Colour selected node
            if curr_queue_node == curr_node:
                dc.SetPen(wx.Pen(wx.RED, 4))

            # Colour active node, takes priority if selected and active nodes are the same
            if curr_queue_node == active_node:
                dc.SetPen(wx.Pen(wx.BLUE, 4))

            dc.DrawCircle(
                int((curr_queue_node.start + curr_queue_node.proportion / 2)
                    * panelSize[0]),
                int((curr_queue_node.depth + 1) / (max_depth + 2)
                    * panelSize[1]),
                NODE_RADIUS
            )


if __name__ == '__main__':
    mainApp = wx.App()
    mainFrame = appFrameInst(parent=None)
    mainFrame.Show()
    mainApp.MainLoop()
