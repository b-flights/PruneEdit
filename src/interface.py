import wx  # type: ignore


class appFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="PruneEdit",
            pos=wx.DefaultPosition,
            size=wx.Size(960, 540),
            style=wx.DEFAULT_FRAME_STYLE
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        editSizer = wx.BoxSizer(wx.VERTICAL)
        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer = wx.BoxSizer(wx.VERTICAL)
        optSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.editCtrl = wx.TextCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE
        )

        editSizer.Add(self.editCtrl, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(editSizer, 1, wx.EXPAND, 5)

        labelSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)
        self.descLabel = wx.StaticText(
            self, wx.ID_ANY, "Description", wx.DefaultPosition, wx.DefaultSize, 0
        )
        labelSizer.Add(self.descLabel, 0, wx.ALL, 5)
        labelSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        descSizer.Add(labelSizer, 0, wx.EXPAND, 5)
        self.descCtrl = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0
        )
        descSizer.Add(self.descCtrl, 1, wx.ALL, 5)
        editSizer.Add(descSizer, 0, wx.EXPAND, 5)

        self.toggleButton = wx.Button(
            self, wx.ID_ANY, "Show\nTree", wx.DefaultPosition, wx.Size(45, 40), 0
        )
        optSizer.Add(self.toggleButton, 0, wx.ALL | wx.EXPAND, 5)

        self.updateButton = wx.Button(
            self, wx.ID_ANY, "Update", wx.DefaultPosition, wx.Size(-1, 40), 0
        )
        optSizer.Add(self.updateButton, 1, wx.ALL, 5)

        self.newRevButton = wx.Button(
            self, wx.ID_ANY, "Save as New", wx.DefaultPosition, wx.Size(-1, 40), 0
        )
        optSizer.Add(self.newRevButton, 1, wx.ALL, 5)
        
        self.setMainButton = wx.Button(
            self, wx.ID_ANY, "Set as Main", wx.DefaultPosition, wx.Size(-1, 40), 0
        )
        optSizer.Add(self.setMainButton, 1, wx.ALL, 5)

        self.deleteButton = wx.Button(
            self, wx.ID_ANY, "Delete", wx.DefaultPosition, wx.Size(-1, 40), 0
        )
        optSizer.Add(self.deleteButton, 1, wx.ALL, 5)

        editSizer.Add(optSizer, 0, wx.EXPAND, 5)

        self.divLine = wx.StaticLine(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL
        )
        mainSizer.Add(self.divLine, 0, wx.EXPAND | wx.ALL, 5)

        self.treePanel = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.treePanel.Bind(wx.EVT_PAINT, self.onPaint)
        self.treePanel.Hide()
        mainSizer.Add(self.treePanel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(mainSizer)
        self.Layout()
        self.menuBar = wx.MenuBar(0)
        self.fileMenu = wx.Menu()
        self.fileMenu_open = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Open Document", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.fileMenu.Append(self.fileMenu_open)

        self.menuBar.Append(self.fileMenu, "File")

        self.SetMenuBar(self.menuBar)

        self.Centre(wx.BOTH)

        self.updateButton.Bind(wx.EVT_BUTTON, self.onUpdate)
        self.newRevButton.Bind(wx.EVT_BUTTON, self.onSaveRev)
        self.setMainButton.Bind(wx.EVT_BUTTON, self.onSetMain)
        self.deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        self.toggleButton.Bind(wx.EVT_BUTTON, self.onTreeToggle)
        self.treePanel.Bind(wx.EVT_SIZE, self.onResizePanel)
        self.treePanel.Bind(wx.EVT_MOTION, self.onMouseMove)
        self.treePanel.Bind(wx.EVT_LEFT_DOWN, self.onTreeClick)
        self.Bind(wx.EVT_MENU, self.onOpenDoc, id=self.fileMenu_open.GetId())

    def onUpdate(self, event):
        event.Skip()

    def onSaveRev(self, event):
        event.Skip()
        
    def onSetMain(self, event):
        event.Skip()

    def onDelete(self, event):
        event.Skip()

    def onTreeToggle(self, event):
        event.Skip()

    def onPaint(self, event):
        event.Skip()

    def onResizePanel(self, event):
        event.Skip()

    def onMouseMove(self, event):
        event.Skip()

    def onTreeClick(self, event):
        event.Skip()
        
    def onOpenDoc(self, event):
        event.Skip()
