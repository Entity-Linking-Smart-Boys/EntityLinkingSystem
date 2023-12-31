from entity_linking_system import EntityLinkingSystem
# Example: Replace 'path/to/your/file.html' with the actual path to your HTML file

import wx
import wx.html2 as html2
import ntpath
from htmldom import htmldom

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.path = None
        '''A path to the file to perform nerd on'''

        self.text = None
        '''Text'''

        self.selectedNER = 0
        '''Selected NER Algorithm, default is 0'''

        self.selectedNED = 0
        '''Selected NED Algorithm, default is 0'''

        self.nerAlgorithms = ['one', 'two', 'threeeeee']
        '''NER Algorithms'''

        self.nedAlgorithms = ['four', 'five', 'six']
        '''NED Algorithms'''

        tfile = open(f"./file/template.xhtml", mode= "r" , encoding="utf-8")
        template = tfile.read()
        tfile.close()
        self.dom = htmldom.HtmlDom().createDom(template)
        '''Template'''

        self.html_content = None
        '''HTML text'''

        self.EL = EntityLinkingSystem()
        '''System creation'''



        self.nerAlgorithms = self.EL.get_ners()
        '''NER Algorithms'''

        self.nedAlgorithms = self.EL.get_neds()
        '''NED Algorithms'''



        splitter = wx.SplitterWindow(self)
        leftPannel = wx.Panel(splitter)
        rightPannel = wx.Panel(splitter)

        #--------------MANAGING LEFT PANEL--------------#
        '''Load text button'''
        self.buttonLoad = wx.Button(leftPannel, label="load text file", pos = (50, 50))
        self.buttonLoad.Bind(wx.EVT_BUTTON, self.on_open)

        '''Choice component (ner and ned choice)'''
        wx.StaticText(leftPannel, -1, "Select NER:", (10, 115))
        self.nerChoice = wx.Choice(leftPannel, -1, pos = (80, 110), size = (100, -1), choices=self.nerAlgorithms)
        self.nerChoice.Bind(wx.EVT_BUTTON, self.on_select_ner)

        wx.StaticText(leftPannel, -1, "Select NED:", (10, 145))
        self.nedChoice = wx.Choice(leftPannel, -1, pos = (80, 140), size = (100, -1), choices=self.nedAlgorithms)
        self.nedChoice.Bind(wx.EVT_BUTTON, self.on_select_ned)

        '''Start button'''
        self.buttonStart = wx.Button(leftPannel, label="start", pos = (50, 200))
        self.buttonStart.Bind(wx.EVT_BUTTON, self.on_start)

        '''Save button'''
        self.buttonSave = wx.Button(leftPannel, label="save html", pos = (200, 200))
        self.buttonSave.Bind(wx.EVT_BUTTON, self.on_save)

        #--------------MANAGING RIGHT PANEL--------------#
        '''load html content'''
        self.browser = html2.WebView.New(rightPannel)
        #self.load_html_content(file_path)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.browser, 1, wx.EXPAND)
        rightPannel.SetSizer(sizer2)

        #print(int(self.Size[1]/2))

        splitter.SplitVertically(leftPannel, rightPannel, int(self.Size[1]/2))  # Set the initial split position

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_save(self, e):
        with wx.FileDialog(self, "Save HTML file", wildcard="HTML files (*.html)|*.html",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding="utf-8") as file:
                    file.write(self.html_content)
                    file.close()
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)
            
        

    def on_start(self, e):
        self.EL.select_ner(self.selectedNER)
        self.EL.select_ned(self.selectedNED)
        self.EL.load_text(self.path)
        
        fileName = ntpath.basename(self.path)
        self.EL.ner()
        self.EL.ned()
        self.display_html_content()

    def on_select_ner(self, event):
        # item = event.GetSelection() items id, we set it to 0 to default
        item = 0
        self.selectedNER = item

    def on_select_ned(self, event):
        # item = event.GetSelection() items id, we set it to 0 to default
        item = 0
        self.selectedNED = item

    def display_html_content(self):#, file_path):
        self.dom.find("div[id=content]").text(self.EL.text.get_html_text())
        self.html_content = "<!DOCTYPE html>"+self.dom.referenceToRootElement.html() # = file.read()
        self.browser.SetPage(self.html_content, "")


    #--------------ON CLICK EVENT--------------#
    def on_click(self, e):
        self.display_html_content()


    #--------------FILE EXPLORER--------------#
    def on_open(self, event):
        # ask the user what new file to open
        with wx.FileDialog(self, "Open txt file", wildcard="txt/json files (*.txt;*.json)|*.txt;*.json",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            self.path = fileDialog.GetPath()
            if self.path:
                self.select_file()
                self.EL.load_text(self.path)
                self.display_html_content()

    def generate_text_name(self, text):
        splits = text.split(".")
        return splits[0]


    def select_file(self):
        # self.EL.select_ner(self.selectedNER)
        # self.EL.select_ned(self.selectedNED)
        # self.EL.load_text(self.path)
        # text = ntpath.basename(self.path)
        # print(ntpath.basename(self.path))
        # #fileName = self.generate_text_name(ntpath.basename(self.path))
        fileName = ntpath.basename(self.path)
        # self.EL.save_html(fileName + '.html')
        # self.EL.ner()
        # self.EL.save_html(fileName + '.html')
        self.buttonLoad.Label = fileName
        
        # # its pretty primitive, just adding .html instead of deleting previous extension
        # self.path += '.html'

        # self.load_html_content()#self.path)

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
