import wx as wx

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
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        
        file_menu = wx.Menu()
        
        file_menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        
        menuBar = wx.MenuBar()
        menuBar.Append(file_menu, "&File")
        self.SetMenuBar(menuBar)          
        
        self.Show(True)
        


Application = wx.App(False)
frame = MyFrame(None, 'Small editor')
Application.MainLoop()




