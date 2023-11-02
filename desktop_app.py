from entity_linking_system import EntityLinkingSystem
import wx
import wx.html2 as html2

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        EL = EntityLinkingSystem()
        EL.select_ner(0)
        EL.select_ned(0)
        EL.load_text("text1.txt")
        EL.save_html("siem.html")
        EL.ner()
        EL.save_html("siem.html")

        path_to_file = "siem.html"

        splitter = wx.SplitterWindow(self)
        leftPannel = wx.Panel(splitter)
        rightPannel = wx.Panel(splitter)
        self.browser = html2.WebView.New(rightPannel)
        with open(path_to_file, "r", encoding="utf-8") as file:
            html_content = file.read()
        self.browser.SetPage(html_content, "")

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.browser, 1, wx.EXPAND)
        rightPannel.SetSizer(sizer2)


        splitter.SplitVertically(leftPannel, rightPannel, int(self.Size[1]/2))  # Set the initial split position

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)



    def on_close(self, event):
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="HTML Viewer", size=(800, 600))
        frame.Show(True)
        return True
    
class InsertText():
    def OnInit(self):

        return True
    
class GenerateNerNed():
    def OnInit(self):

        return True


app = MyApp(False)
app.MainLoop()