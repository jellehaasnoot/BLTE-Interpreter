import wx as wx
import os

# class Main:
#     """In this function a visualized version of the application will be created. In this application, the user
#     can upload, review and save files which were created in the previous scripts"""
#
#
#     #def __init__(self):
#
#
#     # def application(self):
#     #
#     #     # The creation of the pop-up frame:
#     #     visualized_app = wx.App(self)
#     #     visualized_frame = wx.Frame(None, stringtitle="Hello world")
#     #
#     #     # The showing of the frame:
#     #     visualized_frame.Show(self)
#     #     # Create a panel in the frame:
#     #     visualized_panel = wx.Panel(self)
#     #
#     #     # Start the event loop:
#     #     visualized_app.MainLoop()

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 300))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        # Create the file menu
        file_menu = wx.Menu()
        
        menu_about = file_menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        file_menu.AppendSeparator()
        menu_file_open = file_menu.Append(wx.ID_FILE, "&Open file...", "Open a text file with this program")
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Create the menu bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

        # Set events
        self.Bind(wx.EVT_MENU, self.OnOpen, menu_file_open)
        self.Bind(wx.EVT_MENU, self.OnAbout, menu_about)

        self.Show(True)

    def OnOpen(self, e):
        """"Open a file"""
        self.directory_name = ""
        prompted_dialog = wx.FileDialog(self, "Choose a log-file (*.txt)", self.directory_name, "", "*.txt", wx.FD_OPEN)
        if prompted_dialog.ShowModal() == wx.ID_OK:
            self.file_name = prompted_dialog.GetFilename()
            self.directory_name = prompted_dialog.GetDirectory()
            file_to_open = open(os.path.join(self.directory_name, self.file_name, 'r'))
            file_to_open.close()
        prompted_dialog.Destroy()

    def OnAbout(self, e):
        """"Message box with OK button"""
        prompted_dialog = wx.MessageDialog(self, "A file which converts BLTE-data into numerical data and graphs", "About BLTE-Interpreter", wx.OK)
        prompted_dialog.ShowModal()
        prompted_dialog.Destroy()

    def OnExit(self, e):
        self.Close(True)


Application = wx.App(False)
frame = MyFrame(None, 'Small editor')
Application.MainLoop()




