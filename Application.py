import wx as wx
import os
import NRFbluetoothlogfileconverter
import LogReader
import ValueConverter
import PopUp


class Main(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX), size=(500, 1080))
        self.CreateStatusBar()

        # Create the file menu
        file_menu = wx.Menu()

        menu_about = file_menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        file_menu.AppendSeparator()
        menu_file_open = file_menu.Append(wx.ID_FILE, "&Open file...", "Open a text file with this program")
        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Create panels
        top_panel = wx.Panel(self)

        line_count_panel = wx.Panel(top_panel, -1, style=wx.SUNKEN_BORDER, size=(460, 20), pos=(10, 10))
        self.line_count_display = wx.StaticText(line_count_panel, label="DE LINECOUNT:",
                                                pos=(0, 0))  # TODO: Het aantal regels toevoegen
        average_power_panel = wx.Panel(top_panel, -1, style=wx.SUNKEN_BORDER, size=(460, 20), pos=(10, 40))
        self.average_power_display = wx.StaticText(average_power_panel, label="HET GEMIDDELD VERMOGEN:", pos=(0, 0))  # TODO: Het gemiddelde vermogen toevoegen

        filtered_data_panel = wx.Panel(top_panel, -1, style=wx.SUNKEN_BORDER, size=(460, 460), pos=(10, 70))
        self.filtered_data_display = wx.StaticText(filtered_data_panel, label="DE DATA:" + Main.on_open.data,
                                                   pos=(0, 0))  # TODO: De data correct toevoegen

        # Create the menu bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

        # Set events
        self.Bind(wx.EVT_MENU, self.on_open, menu_file_open)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)

        self.Show(True)

    def on_open(self, e):
        """"Open a file"""
        self.directory_name = ""
        prompted_dialog = wx.FileDialog(self, "Choose a log-file (*.txt)", self.directory_name, "", "*.txt", wx.FD_OPEN)
        if prompted_dialog.ShowModal() == wx.ID_OK:
            self.file_name = prompted_dialog.GetFilename()
            self.directory_name = prompted_dialog.GetDirectory()
            file_to_open = open(os.path.join(self.directory_name, self.file_name))
            data = NRFbluetoothlogfileconverter.Main(self.file_name)
            file_to_open.close()
        prompted_dialog.Destroy()
        return data

    def on_about(self, e):
        """"Message box with OK button"""
        prompted_dialog = wx.MessageDialog(self, "A file which converts BLTE-data into numerical data and graphs",
                                           "About BLTE-Interpreter", wx.OK)
        prompted_dialog.ShowModal()
        prompted_dialog.Destroy()

    def on_exit(self, e):
        self.Close(True)


if __name__ == '__main__':
    Application = wx.App(False)
    frame = Main(None, 'BLTE-Interpreter')
    Application.MainLoop()
