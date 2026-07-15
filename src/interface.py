import wx  # type: ignore
import wx.html  # type: ignore


class appFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="PruneEdit",
            pos=wx.DefaultPosition,
            size=wx.Size(1090, 625),
            style=wx.DEFAULT_FRAME_STYLE
        )

        self.SetClientSize(self.GetSize())
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        self.panel = wx.Panel(self)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        editSizer = wx.BoxSizer(wx.VERTICAL)
        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelSizer = wx.BoxSizer(wx.VERTICAL)
        optSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.editCtrl = wx.TextCtrl(
            self.panel,
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
            self.panel, wx.ID_ANY, "Description", wx.DefaultPosition, wx.DefaultSize, 0
        )
        labelSizer.Add(self.descLabel, 0, wx.ALL, 5)
        labelSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        descSizer.Add(labelSizer, 0, wx.EXPAND, 5)
        self.descCtrl = wx.TextCtrl(
            self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0
        )
        descSizer.Add(self.descCtrl, 1, wx.ALL, 5)
        editSizer.Add(descSizer, 0, wx.EXPAND, 5)

        self.toggleButton = wx.Button(
            self.panel, wx.ID_ANY, "Show\nTree", wx.DefaultPosition, wx.Size(45, -1), 0
        )
        self.toggleButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.toggleButton.SetBackgroundColour(wx.NullColour)
        optSizer.Add(self.toggleButton, 0, wx.ALL | wx.EXPAND, 3)

        optSizerGrid = wx.GridSizer(2, 3, 0, 0)

        self.updateButton = wx.Button(
            self.panel, wx.ID_ANY, "Update", wx.DefaultPosition, wx.Size(-1, 30), 0
        )
        self.updateButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.updateButton.SetBackgroundColour(wx.NullColour)
        optSizerGrid.Add(self.updateButton, 1, wx.ALL | wx.EXPAND, 3)

        self.newRevButton = wx.Button(
            self.panel, wx.ID_ANY, "Save as New", wx.DefaultPosition, wx.Size(-1, 30), 0
        )
        self.newRevButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.newRevButton.SetBackgroundColour(wx.NullColour)
        optSizerGrid.Add(self.newRevButton, 1, wx.ALL | wx.EXPAND, 3)

        self.newBlankButton = wx.Button(
            self.panel, wx.ID_ANY, "New Blank Version", wx.DefaultPosition, wx.Size(-1, 30), 0
        )
        self.newBlankButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.newBlankButton.SetBackgroundColour(wx.NullColour)
        optSizerGrid.Add(self.newBlankButton, 1, wx.ALL | wx.EXPAND, 3)

        self.setMainButton = wx.Button(
            self.panel, wx.ID_ANY, "Set as Main", wx.DefaultPosition, wx.Size(-1, 30), 0
        )
        self.setMainButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.setMainButton.SetBackgroundColour(wx.NullColour)
        optSizerGrid.Add(self.setMainButton, 1, wx.ALL | wx.EXPAND, 3)

        self.deleteButton = wx.Button(
            self.panel, wx.ID_ANY, "Delete", wx.DefaultPosition, wx.Size(-1, 30), 0
        )
        self.deleteButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.deleteButton.SetBackgroundColour(wx.NullColour)
        optSizerGrid.Add(self.deleteButton, 1, wx.ALL | wx.EXPAND, 3)

        self.delChangeButton = wx.Button(
            self.panel, wx.ID_ANY, "Delete Changes", wx.DefaultPosition, wx.Size(-1, 30), 0
        )
        self.delChangeButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.delChangeButton.SetBackgroundColour(wx.NullColour)
        optSizerGrid.Add(self.delChangeButton, 1, wx.ALL | wx.EXPAND, 3)

        optSizer.Add(optSizerGrid, 1, wx.EXPAND, 5)
        editSizer.Add(optSizer, 0, wx.EXPAND, 5)

        self.divLine = wx.StaticLine(
            self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL
        )
        mainSizer.Add(self.divLine, 0, wx.EXPAND | wx.ALL, 5)

        self.treePanel = wx.Panel(
            self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.treePanel.Bind(wx.EVT_PAINT, self.onPaint)
        self.treePanel.Hide()
        mainSizer.Add(self.treePanel, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(mainSizer)
        self.Layout()
        self.menuBar = wx.MenuBar(0)

        # File menu
        self.fileMenu = wx.Menu()

        self.fileMenu_new = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "New", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.fileMenu.Append(self.fileMenu_new)

        self.fileMenu.AppendSeparator()

        self.fileMenu_open = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Open Document", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.fileMenu.Append(self.fileMenu_open)

        self.fileMenu_save = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Save Document", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.fileMenu.Append(self.fileMenu_save)

        self.fileMenu.AppendSeparator()

        self.fileMenu_openTree = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Open Tree", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.fileMenu.Append(self.fileMenu_openTree)

        self.fileMenu_saveTree = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Save Tree", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.fileMenu.Append(self.fileMenu_saveTree)

        self.menuBar.Append(self.fileMenu, "File")

        # Options menu
        self.optionsMenu = wx.Menu()
        self.optionsMenu_prefs = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Preferences", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.optionsMenu.Append(self.optionsMenu_prefs)

        self.menuBar.Append(self.optionsMenu, "Options")

        # Help menu
        self.helpMenu = wx.Menu()
        self.helpMenu_help = wx.MenuItem(
            self.fileMenu, wx.ID_ANY, "Help", wx.EmptyString, wx.ITEM_NORMAL
        )
        self.helpMenu.Append(self.helpMenu_help)

        self.menuBar.Append(self.helpMenu, "Help")

        self.SetMenuBar(self.menuBar)

        self.Centre(wx.BOTH)

        # Bind button handlers
        self.updateButton.Bind(wx.EVT_BUTTON, self.onUpdate)
        self.newRevButton.Bind(wx.EVT_BUTTON, self.onSaveRev)
        self.newBlankButton.Bind(wx.EVT_BUTTON, self.onNewBlank)
        self.setMainButton.Bind(wx.EVT_BUTTON, self.onSetMain)
        self.deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        self.delChangeButton.Bind(wx.EVT_BUTTON, self.onDelChange)
        self.toggleButton.Bind(wx.EVT_BUTTON, self.onTreeToggle)

        # Bind panel event handlers
        self.treePanel.Bind(wx.EVT_SIZE, self.onResizePanel)
        self.treePanel.Bind(wx.EVT_MOTION, self.onMouseMove)
        self.treePanel.Bind(wx.EVT_LEFT_DOWN, self.onTreeClick)

        # Bind menu item handlers
        self.Bind(wx.EVT_MENU, self.onNewTree, id=self.fileMenu_new.GetId())
        self.Bind(wx.EVT_MENU, self.onOpenDoc, id=self.fileMenu_open.GetId())
        self.Bind(wx.EVT_MENU, self.onSaveDoc, id=self.fileMenu_save.GetId())
        self.Bind(wx.EVT_MENU, self.onOpenTree, id=self.fileMenu_openTree.GetId())
        self.Bind(wx.EVT_MENU, self.onSaveTree, id=self.fileMenu_saveTree.GetId())
        self.Bind(wx.EVT_MENU, self.onOpenPrefs, id=self.optionsMenu_prefs.GetId())
        self.Bind(wx.EVT_MENU, self.onOpenHelp, id=self.helpMenu_help.GetId())

        # Bind edit handlers
        self.editCtrl.Bind(wx.EVT_TEXT, self.onContentEdit)
        self.descCtrl.Bind(wx.EVT_TEXT, self.onDescEdit)

    def onUpdate(self, event): event.Skip()

    def onSaveRev(self, event): event.Skip()

    def onNewBlank(self, event): event.Skip()

    def onSetMain(self, event): event.Skip()

    def onDelete(self, event): event.Skip()

    def onDelChange(self, event): event.Skip()

    def onTreeToggle(self, event): event.Skip()

    def onPaint(self, event): event.Skip()

    def onResizePanel(self, event): event.Skip()

    def onMouseMove(self, event): event.Skip()

    def onTreeClick(self, event): event.Skip()

    def onNewTree(self, event): event.Skip()

    def onOpenDoc(self, event): event.Skip()

    def onSaveDoc(self, event): event.Skip()

    def onOpenTree(self, event): event.Skip()

    def onSaveTree(self, event): event.Skip()

    def onOpenPrefs(self, event): event.Skip()

    def onOpenHelp(self, event): event.Skip()

    def onContentEdit(self, event): event.Skip()

    def onDescEdit(self, event): event.Skip()


class prefWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="Preferences",
            pos=wx.DefaultPosition,
            style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        panel = wx.Panel(self)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        optSizer = wx.BoxSizer(wx.VERTICAL)
        optSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        self.nodeThicknessLabel = wx.StaticText(
            panel, wx.ID_ANY, "Node Thickness", wx.DefaultPosition, wx.DefaultSize, 0
        )
        optSizer.Add(self.nodeThicknessLabel, 0, wx.ALL, 5)

        self.nodeThicknessSlider = wx.Slider(
            panel, wx.ID_ANY, 4, 1, 20, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL
        )
        optSizer.Add(self.nodeThicknessSlider, 0, wx.ALL | wx.EXPAND, 5)

        self.nodeRadiusLabel = wx.StaticText(
            panel, wx.ID_ANY, "Node Radius", wx.DefaultPosition, wx.DefaultSize, 0
        )
        optSizer.Add(self.nodeRadiusLabel, 0, wx.ALL, 5)

        self.nodeRadiusSlider = wx.Slider(
            panel, wx.ID_ANY, 15, 3, 50, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL
        )
        optSizer.Add(self.nodeRadiusSlider, 0, wx.ALL | wx.EXPAND, 5)

        self.propRadiusLabel = wx.StaticText(
            panel, wx.ID_ANY, "Proportional Radius", wx.DefaultPosition, wx.DefaultSize, 0
        )
        optSizer.Add(self.propRadiusLabel, 0, wx.ALL, 5)

        self.propRadiusSlider = wx.Slider(
            panel, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL
        )
        optSizer.Add(self.propRadiusSlider, 0, wx.ALL | wx.EXPAND, 5)

        self.sysColourCheckBox = wx.CheckBox(
            panel, wx.ID_ANY, "Use System Colours", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.sysColourCheckBox.SetValue(True)
        optSizer.Add(self.sysColourCheckBox, 0, wx.ALL, 5)

        self.fontSizeLabel = wx.StaticText(
            panel, wx.ID_ANY, "Font Size", wx.DefaultPosition, wx.DefaultSize, 0
        )
        optSizer.Add(self.fontSizeLabel, 0, wx.ALL, 5)

        self.fontSizeSelect = wx.SpinCtrl(
            panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 5, 48, 11
        )
        optSizer.Add(self.fontSizeSelect, 0, wx.ALL, 5)

        self.divLine1 = wx.StaticLine(
            panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL
        )
        optSizer.Add(self.divLine1, 0, wx.EXPAND | wx.ALL, 5)

        self.updateCheckBox = wx.CheckBox(
            panel, wx.ID_ANY, "Auto Update", wx.DefaultPosition, wx.DefaultSize, 0
        )
        optSizer.Add(self.updateCheckBox, 0, wx.ALL, 5)

        self.updateChoiceLabel = wx.StaticText(
            panel, wx.ID_ANY,
            "Auto Update behaviour for internal versions",
            wx.DefaultPosition, wx.DefaultSize,
            0
        )
        optSizer.Add(self.updateChoiceLabel, 0, wx.ALL, 5)

        self.updateChoiceBox = wx.Choice(
            panel,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            [
                "None",
                "Save as New Version",
                "Discard Child Versions"
            ],
            0
        )
        self.updateChoiceBox.SetSelection(0)
        optSizer.Add(self.updateChoiceBox, 0, wx.ALL, 5)

        self.divLine2 = wx.StaticLine(
            panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL
        )
        optSizer.Add(self.divLine2, 0, wx.EXPAND | wx.ALL, 5)

        self.savePrefButton = wx.Button(
            panel, wx.ID_ANY, "Save Preferences", wx.DefaultPosition, wx.Size(130, 40), 0
        )
        self.savePrefButton.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        )
        self.savePrefButton.SetBackgroundColour(wx.NullColour)
        optSizer.Add(self.savePrefButton, 0, wx.ALL, 5)

        optSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        mainSizer.Add(optSizer, 12, wx.EXPAND, 5)

        mainSizer.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        panel.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.nodeThicknessSlider.Bind(wx.EVT_SCROLL, self.onThicknessChange)
        self.nodeRadiusSlider.Bind(wx.EVT_SCROLL, self.onRadiusChange)
        self.propRadiusSlider.Bind(wx.EVT_SCROLL, self.onPropRadChange)
        self.updateCheckBox.Bind(wx.EVT_CHECKBOX, self.onAutoUpdateCheck)
        self.savePrefButton.Bind(wx.EVT_BUTTON, self.onSavePref)
        self.updateChoiceBox.Bind(wx.EVT_CHOICE, self.onUpdateChoice)
        self.sysColourCheckBox.Bind(wx.EVT_CHECKBOX, self.onSysColourCheck)
        self.fontSizeSelect.Bind(wx.EVT_SPINCTRL, self.onFontSizeChange)
        self.Bind(wx.EVT_CLOSE, self.onWindowClose)

    def onThicknessChange(self, event): event.Skip()

    def onRadiusChange(self, event): event.Skip()

    def onPropRadChange(self, event): event.Skip()

    def onAutoUpdateCheck(self, event): event.Skip()

    def onSavePref(self, event): event.Skip()

    def onUpdateChoice(self, event): event.Skip()

    def onSysColourCheck(self, event): event.Skip()

    def onFontSizeChange(self, event): event.Skip()

    def onWindowClose(self, event): event.Skip()


class helpWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="Help",
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_FRAME_STYLE
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.helpText = wx.html.HtmlWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.html.HW_SCROLLBAR_AUTO
        )
        self.helpText.LoadFile("help_window.html")
        mainSizer.Add(self.helpText, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)
