import wx
import os
import wxmpl
import matplotlib
import matplotlib.cm as cm
from pylab import *
class PlotPanel (wx.Panel):
    """The PlotPanel has a Figure and a Canvas. OnSize events simply set a 
flag, and the actual resizing of the figure is triggered by an Idle event."""
    def __init__( self, parent, color=None, dpi=None, **kwargs ):
        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
        from matplotlib.figure import Figure

        # initialize Panel
        if 'id' not in kwargs.keys():
            kwargs['id'] = wx.ID_ANY
        if 'style' not in kwargs.keys():
            kwargs['style'] = wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Panel.__init__( self, parent, **kwargs )

        # initialize matplotlib stuff
        self.figure = Figure( None, dpi )
        self.axes = self.figure.gca()
        self.canvas = FigureCanvasWxAgg( self, -1, self.figure )
        self.SetColor( color )

        self._SetSize()
        self.draw()
        self.axes.set_xlabel('T (s)')
        self.axes.set_ylabel('Alfa_max (g)')
        self.axes.set_title("wave curve")
        self.axes.grid(True)
        self._resizeflag = False

        self.Bind(wx.EVT_IDLE, self._onIdle)
        self.Bind(wx.EVT_SIZE, self._onSize)

    def SetColor( self, rgbtuple=None ):
        """Set figure and canvas colours to be the same."""
        if rgbtuple is None:
            rgbtuple = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ).Get()
        clr = [c/255. for c in rgbtuple]
        self.figure.set_facecolor( clr )
        self.figure.set_edgecolor( clr )
        self.canvas.SetBackgroundColour( wx.Colour( *rgbtuple ) )

    def _onSize( self, event ):
        self._resizeflag = True

    def _onIdle( self, evt ):
        if self._resizeflag:
            self._resizeflag = False
            self._SetSize()

    def _SetSize( self ):
        pixels = tuple( self.parent.GetClientSize() )
        self.SetSize( pixels )
        self.canvas.SetSize( pixels )
        self.figure.set_size_inches( float( pixels[0] )/self.figure.get_dpi(),
                                     float( pixels[1] )/self.figure.get_dpi() )

    def draw(self): pass # abstract, to be overridden by child classes

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'plot a wave')
        p = wx.Panel(self)
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        open = menu.Append(-1,'Open spe file to plot','open txt')
        menu.AppendSeparator()
        exit = menu.Append(-1,'Exit')
        self.Bind(wx.EVT_MENU,self.OnOpen,open)
        self.Bind(wx.EVT_MENU,self.OnExit,exit)
        menuBar.Append(menu, 'File')
        self.SetMenuBar(menuBar)
        self.workdir=os.getcwd()
    def OnOpen(self,event):
        wildcard = "Wave file (*.txt)|*.txt|" \
          "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file", self.workdir,
          "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            infile = dialog.GetPath()
            p,f = os.path.split(infile)
            self.workdir = p
        dialog.Destroy()
        f=open(infile,'rb')
        x=[]
        y=[]
        z=[]
        colx=0
        coly=1
        colz=4
        str=f.readline()
        str=f.readline()
        while str!="":
            items = str.split()
            x.append(float(items[colx]))
            y.append(float(items[coly]))
            #z.append(float(items[colz]))
            str=f.readline()
        f.close()
        frame = wxmpl.PlotFrame(None, -1, title=infile, size=(6.0,3.7),dpi=96)
        fig=frame.get_figure()
        axes = fig.gca()
        axes.plot(x, y, linewidth=1.0)
        #axes.plot(x, z, linewidth=1.0)
        axes.set_xlabel('T (s)')
        axes.set_ylabel('Alfa_max (g)')
        axes.set_title('spectrum vs. time')
        axes.grid(True)
        frame.draw()
        frame.Show()
    def OnExit(self,event):
        self.Close()
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
