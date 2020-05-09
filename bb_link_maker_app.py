#!/usr/bin/env python

#logic by itself in module

import wx
from wx import xrc


#import txt_database
import bb_utils
import pyperclip
import copy

#https://drive.google.com/file/d/1zzY_zN6DJMCZtohuMc0lgB8gzxOE01u5/view?usp=sharing
#https://drive.google.com/open?id=1zzY_zN6DJMCZtohuMc0lgB8gzxOE01u5
#https://drive.google.com/file/d/1y-jRZIgiafMChmB25F3qwg7_Y_qv0v1J/view?usp=sharing

def krauss_to_ascii(textin):
    """My attempt to convert a wx textctrl output to ascii intelligently.
       Note that u'\xa0' is an unbreakable space."""
    replist = [('“','"'), \
               ('”','"'), \
               (u'\xa0',' ')
               ]
    textout = copy.copy(textin)
    for f, r in replist:
        textout = textout.replace(f,r)

    print('\n')
    try:
        textout.encode('ascii')
        print('ascii conversion successful # <----')
    except:
        print('ascii conversion FAILED # !?!?!?!?')
    print('\n')
    return textout

    
class MyApp(wx.App):
    def on_file_open(self, evt):
        print("hello from on_file_open")
        openFileDialog = wx.FileDialog(self.frame, "Open", "", "", 
                                       "pdf files (*.pdf)|*.pdf|" + \
                                       "Python Files|*.py;*.ipynb|" + \
                                       "All files (*.*)|*.*", \
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            fp = openFileDialog.GetPath()
            print(fp)
            self.file_path_text_ctrl.SetValue(fp)
            
        openFileDialog.Destroy()


    def clear(self):
        self.title_textctrl.SetValue("")
        
        
    def OnInit(self):
        self.res = xrc.XmlResource('/Users/kraussry/git/wx_bb_link_maker/bb_link_xrc.xrc')
        self.init_frame()
        return True


    def set_out(self, textout):
        self.output_textctrl.SetValue(textout)
        pyperclip.copy(textout)
        print("copied to clipboard:")
        print('\n')
        print(textout)
        

    def OnText(self, evt):
        textin = self.title_textctrl.GetValue()
        print('textin = ')
        print(textin)
        #if wx.TheClipboard.Open():
        if textin.find("https://youtu.be") == 0:
            # this is a YouTube link
            textout = bb_utils.youtube_link(textin)
        else:
            textout = bb_utils.pdf_link_download_maker_no_print(textin)
        print('textout = ')
        print(textout)
        self.set_out(textout)
        #wx.TheClipboard.SetData(wx.TextDataObject(textout))
        #wx.TheClipboard.Close()
        #else:
        #    print("failed to open clipboard")


    def OnCopy(self, evt):
        textout = self.output_textctrl.GetValue()
        ascii_text = krauss_to_ascii(textout)
        pyperclip.copy(ascii_text)
        print("copied to clipboard:")
        print('\n')
        print(textout)


    def on_download_only(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.pdf_link_download_only_no_print(textin)
        self.set_out(textout)        


    def on_gslides_download(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.download_for_gslides(textin)
        self.set_out(textout)        

        

    def on_open_only(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.link_open_only_no_print(textin)
        self.set_out(textout)        


    def on_open_link_only(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.link_open_link_only(textin)
        self.set_out(textout)        


    def on_pure_link(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.link_pure_open_no_print(textin)
        self.set_out(textout)


    def on_markdown_juptyer_download(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.markdown_jupyter_download_link(textin)
        self.set_out(textout)
        

    def on_markdown_pdf_open(self, event):
        textin = self.title_textctrl.GetValue()
        #if wx.TheClipboard.Open():
        textout = bb_utils.markdown_pdf_open_link(textin)
        self.set_out(textout)
        
        
    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frame')
        self.menuBar = self.res.LoadMenuBar("frame_menubar")
        self.frame.Bind(wx.EVT_MENU, self.on_file_open, id=xrc.XRCID("file_open_menu"))
        #self.frame.Bind(wx.EVT_MENU, self.on_file_save, id=xrc.XRCID("file_save_menu"))
        self.frame.Bind(wx.EVT_BUTTON, self.on_file_open, id=xrc.XRCID("file_path_button"))
        self.frame.Bind(wx.EVT_MENU, self.on_download_only, \
                        id=xrc.XRCID("process_download_only_menu"))
        self.frame.Bind(wx.EVT_MENU, self.on_open_only, \
                        id=xrc.XRCID("process_open_only_menu"))
        self.frame.Bind(wx.EVT_MENU, self.on_open_link_only, \
                        id=xrc.XRCID("process_open_link_only_menu"))        
        self.frame.Bind(wx.EVT_MENU, self.OnText, \
                        id=xrc.XRCID("process_normal_menu"))
        self.frame.Bind(wx.EVT_MENU, self.on_pure_link, \
                        id=xrc.XRCID("process_pure_link_menu"))
        self.frame.Bind(wx.EVT_MENU, self.on_markdown_juptyer_download, \
                        id=xrc.XRCID("process_markdown_jupyter_download_menu"))
        self.frame.Bind(wx.EVT_MENU, self.on_markdown_pdf_open, \
                        id=xrc.XRCID("process_markdown_pdf_open_menu"))
        self.frame.Bind(wx.EVT_MENU, self.on_gslides_download, \
                id=xrc.XRCID("process_gslides_download_menu"))


                        
        self.frame.Bind(wx.EVT_MENU, self.OnCopy, \
                        id=xrc.XRCID("copy_menu"))
        self.frame.SetMenuBar(self.menuBar)
        self.panel = xrc.XRCCTRL(self.frame, 'panel_1')
        #self.frame.Bind(wx.EVT_BUTTON, self.OnSubmit, id=xrc.XRCID('button'))

        self.title_textctrl = xrc.XRCCTRL(self.panel, "title_textctrl")

        self.title_textctrl.Bind( wx.EVT_TEXT, self.OnText )

        self.output_textctrl = xrc.XRCCTRL(self.panel, "output_box")
        
        # set up accelerators
        accelEntries = []
        #accelEntries.append((wx.ACCEL_CTRL, ord('O'), xrc.XRCID("file_open_menu")))
        #accelEntries.append((wx.ACCEL_CTRL, ord('S'), xrc.XRCID("file_save_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('d'), xrc.XRCID("process_download_only_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('n'), xrc.XRCID("process_normal_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('o'), xrc.XRCID("process_open_only_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('l'), xrc.XRCID("process_pure_link_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('j'), xrc.XRCID("process_markdown_jupyter_download_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('m'), xrc.XRCID("process_markdown_jupyter_download_menu"))) 
        accelEntries.append((wx.ACCEL_CTRL, ord('p'), xrc.XRCID("process_markdown_pdf_open_menu")))
        accelEntries.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('c'), xrc.XRCID("copy_menu")))
        accelEntries.append((wx.ACCEL_CTRL, ord('g'), xrc.XRCID("process_gslides_download_menu")))
        
        

        accelTable  = wx.AcceleratorTable(accelEntries)
        self.frame.SetAcceleratorTable(accelTable)

        self.frame.Show()

    def OnSubmit(self, evt):
        wx.MessageBox('Your name is %s %s!' %
            (self.text1.GetValue(), self.text2.GetValue()), 'Feedback')


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
