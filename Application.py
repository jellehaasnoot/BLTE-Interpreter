import wx as wx

class Main:
    def application(self):
        '''In this function a visualized version of the application will be created. In this application, the user
        can upload, review and save files which were created in the previous scripts'''

        # The creation of the pop-up frame:
        visualized_app = wx.App(self)
        visualized_frame = wx.Frame(None, title="Hello world")

        # The showing of the frame:
        visualized_frame.Show(self)
        # Create a panel in the frame:
        visualized_panel = wx.Panel(self)

        # Start the event loop:
        visualized_app.MainLoop(self)


Main.application()



