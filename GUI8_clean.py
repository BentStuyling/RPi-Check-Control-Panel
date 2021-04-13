# Digital HUD check panel for BMW E30 based on Raspberry Pi

import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.figure as figure
from tkinter.font import Font
import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        # Initialize fullscreen (window resolution)
        self.attributes('-fullscreen', True)
        # Fonts
        global TitleFont
        TitleFont = Font(family="bmw-helvetica-bold", size=18, weight = 'bold')
        global LabelFont
        LabelFont = Font(family="Helvetica", size=16)
        global Labelcolor
        Labelcolor = 'white'
        global ValueFont
        ValueFont = Font(family="DS-Digital", size=29, weight='bold')
        global Valuecolor
        Valuecolor = '#E14500'
        global UnitFont
        UnitFont = Font(family="DS-Digital", size=18, weight='bold')
        global Unitcolor
        Unitcolor = '#E14500'
        global Graphcolor
        Graphcolor = '#E14500'

        global StatusFont
        StatusFont = Font(family='Helvetica', size=12, weight='bold')
        global StatusLabelcolor
        StatusLabelcolor = 'white'
        global StatusValuecolor
        StatusValuecolor = '#E14500'

        # Creat key binds
      
        self.bind('<F11>', self.fullscreen)
        self.bind('<F10>', self.smallwindow)

        # Configre window
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(240, 320))
        self.config(cursor='none')
        # self.overrideredirect(1) # Uncomment to remove title bar

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        page_name = PageOne.__name__
        frame = PageOne(parent=container, controller=self)
        frame.config(bg="black")
        self.frames[page_name] = frame
        # Put al frames in same loation
        frame.grid(row=0, column=0, sticky="nsew")
        # Start with this page:
        self.show_frame("PageOne")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def fullscreen(self, event):
        self.attributes('-fullscreen', True)

    def smallwindow(self, event):
        self.attributes('-fullscreen', False)
        self.geometry('{}x{}'.format(240, 320))


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Crate frames for labels and values to display
        # Title frame
        frame_lable_Title = tk.Frame(self, width=240, height=30, bg='black')
        frame_lable_Title.grid(row=0)
        frame_lable_Title.grid_propagate(0)
        # Line canvas
        linecanvas_1 = tk.Canvas(self, width=240, height=2, bg='black', highlightthickness=0)
        linecanvas_1.grid(row=1)
        linecanvas_1.grid_propagate(0)
        # First row frames for lables and values
        frame_lable_row_1 = tk.Frame(self, width=240, height=30, bg='black')
        frame_lable_row_1.grid(row=2)
        frame_lable_row_1.grid_propagate(0)
        frame_value_row_1 = tk.Frame(self, width=240, height=35, bg='black')
        frame_value_row_1.grid(row=3)
        frame_value_row_1.grid_propagate(0)
        # Secon rowd frames for lables and values
        frame_lable_row_2 = tk.Frame(self, width=240, height=30, bg='black')
        frame_lable_row_2.grid(row=4)
        frame_lable_row_2.grid_propagate(0)
        frame_value_row_2 = tk.Frame(self, width=240, height=35, bg='black')
        frame_value_row_2.grid(row=5)
        frame_value_row_2.grid_propagate(0)
        # Line canvas
        linecanvas_2 = tk.Canvas(self, width=240, height=10, bg='black', highlightthickness=0)
        linecanvas_2.grid(row=6)
        linecanvas_2.grid_propagate(0)
        # Plot frame
        Plotframe = tk.Frame(self, width=240, height=148, bg='black')
        Plotframe.grid(row=7)
        Plotframe.grid_propagate(0)

        # oil temperature
        oiltemp = Signal('oil_temp')
        oiltemp.interval = 3000
        oiltemp.title_pos = {
            'frame':frame_lable_row_1,
            'x':5,
            'y':4,
            'anchor':None
        }
        oiltemp.value_pos = {
            'frame':frame_value_row_1,
            'x':70,
            'y':15,
            'anchor':'e'
        }
        oiltemp.unit_pos = {
            'frame':frame_value_row_1,
            'x':70,
            'y':19,
            'anchor':'w'
        }
      
        # oil temp
        oilpress = Signal('oil_pressure')
        oilpress.title_pos = {
            'frame':frame_lable_row_1,
            'x':235,
            'y':17,
            'anchor':'e'
        }
        oilpress.value_pos = {
            'frame':frame_value_row_1,
            'x':190,
            'y':15,
            'anchor':'e'
        }
        oilpress.unit_pos = {
            'frame':frame_value_row_1,
            'x':190,
            'y':19,
            'anchor':'w'
        }

        # coolant temp
        clnt_temp = Signal('coolant_temp')
        clnt_temp.interval = 3000
        clnt_temp.title_pos = {
            'frame':frame_lable_row_2,
            'x':5,
            'y':4,
            'anchor':None
        }
        clnt_temp.value_pos = {
            'frame':frame_value_row_2,
            'x':70,
            'y':15,
            'anchor':'e'
        }
        clnt_temp.unit_pos = {
            'frame':frame_value_row_2,
            'x':70,
            'y':19,
            'anchor':'w'
        }

        # rpm
        rpm = Signal('rpm')
        rpm.title_pos = {
            'frame':frame_lable_row_2,
            'x':235,
            'y':17,
            'anchor':'e'
        }
        rpm.value_pos = {
            'frame':frame_value_row_2,
            'x':190,
            'y':15,
            'anchor':'e'
        }
        rpm.unit_pos = {
            'frame':frame_value_row_2,
            'x':190,
            'y':19,
            'anchor':'w'
        }        
        # start readings
        oiltemp.start()
        oilpress.start()
        clnt_temp.start()
        rpm.start()

        # put your widgets here
        # screen title
        tk.Label(frame_lable_Title, font=TitleFont, fg=Labelcolor,
                 bg='black', text='MOTOR').place(relx=.5, rely=0.5, anchor='center')
        # white line in first canvas
        linecanvas_1.create_line(0, 1, 240, 1, fill='white', width=2)

        # white line in first canvas
        linecanvas_2.create_line(0, 4, 240, 4, fill='white', width=2)

        # GRAPHS
        # Variables for graph plotting
        # Time (ms) between polling/animation updates
        self.update_interval = 2000
        self.graph_duration = 600  # Time (s) of grap length

        # Parameters
        # Number of points to display
        self.x_len = int(
            round(((self.graph_duration*1000)/self.update_interval), 0))
        # Range of possible Y values to display left axis
        self.y1_range = [78, 107]
        # Range of possible Y values to display right axis
        self.y2_range = [78, 107]
        # Create graph fiugre
        self.fig = figure.Figure(facecolor='black', figsize=(3.25, 2), dpi=75)
        self.ax1 = self.fig.add_subplot(1, 1, 1, facecolor='black')
        self.fig.subplots_adjust(left=0.12, right=0.95, bottom=0.25, top=0.95)
        # Create a Tk Canvas widget out of figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=Plotframe)
        # Instantiate a new set of axes that shares the same x-axis
        #self.ax2 = self.ax1.twinx()

        # Layout of  axes
        # Axis one (left)
        # self.ax1.set_ylabel('TEMP. [C]', color=color, weight = 'bold', fontsize= 13)
        self.ax1.tick_params(axis='y', labelcolor=Graphcolor,
                             pad=1, length=0,  labelsize=14,)
        self.ax1.set_yticks([80, 85, 90, 95, 100, 105])
        self.ax1.grid(linewidth=2, axis='y')
        self.ax1.tick_params(
            axis='x', labelcolor=Graphcolor, pad=1, labelsize=14)
        self.ax1.set_xlabel('ZEIT [s]', color='white',
                            labelpad=0, weight='bold', fontsize=13)
        self.ax1.set_ylim(self.y1_range)
        self.ys1 = [0] * self.x_len
        self.xs = list(range(0, self.x_len))
        self.ax1.set_xticks([0, self.x_len/4, self.x_len/2,
                             self.x_len/1.333, self.x_len])
        self.ax1.set_xticklabels([int(self.graph_duration), round(int(
            self.graph_duration)/1.3333), round(int(self.graph_duration)/2), round(int(self.graph_duration)/4), 0])
        self.fig.text(0.03, 0.05, 'KUHLW', color='tab:blue',
                      fontsize=13, weight='bold')
        self.fig.text(0.87, 0.05, 'ÖL', color='tab:orange',
                      fontsize=13, weight='bold')
        # Axis 2 (right)
        # color = 'tab:orange'
        # self.ax2.set_ylabel('ÖLTEMP. [C]', color=color, weight = 'bold',fontsize= 13)
        # self.ax2.tick_params(axis='y', labelcolor=color, pad = 1, length = 0, labelsize=10)
        # self.ax2.tick_params(axis='x', labelcolor=color, pad = 0,labelsize=10)
        # self.ax2.set_ylim(self.y2_range)
        self.ys2 = [0] * self.x_len
        # PLot lines
        color = 'tab:blue'
        self.line1, = self.ax1.plot(
            self.xs, self.ys1, linewidth=3, color=color)
        color = 'tab:orange'
        self.line2, = self.ax1.plot(
            self.xs, self.ys2, linewidth=3, color=color)

        # Add all elements to frame
        for w in Plotframe.winfo_children():
            w.grid(padx=0, pady=0)

        # Call animate() function periodically
        self.ani = animation.FuncAnimation(self.fig,
                                           self.animate,
                                           fargs=(
                                               self.ys1, self.ys2, self.x_len, self.line1, self.line2),
                                           interval=self.update_interval,
                                           blit=True)

    # This function is called periodically from FuncAnimation
    def animate(self, i, ys1, ys2, x_len, line1, line2):
        # Append new sensor value to line plot list.
        Temp1 = ClntTemp()
        Temp2 = OilTemp()

        if Temp1 == "--":
            ys1.append(0)
        else:
            ys1.append(Temp1)

        if Temp2 == "--":
            ys2.append(0)
        else:
            ys2.append(Temp2)

        # Limit y list to set number of items
        ys1 = ys1[-self.x_len:]
        ys2 = ys2[-self.x_len:]
        # Update line with new Y values
        line1.set_ydata(ys1)
        line2.set_ydata(ys2)
        return line1, line2,


class Signal:
    def __init__(self, _type):
        self.output = tk.IntVar()
        self.type = _type
        self.title_pos = {}
        self.value_pos = {}
        self.unit_pos = {}
        self.interval = 250
        if _type == 'oil_temp':
            self.title = 'ÖLTEMP'
            self.unit = 'C'
            self.get = OilTemp
        if _type == 'oil_pressure':
            self.title = 'ÖLDRUCK'
            self.unit = 'BAR'
            self.get = OilPress
        if _type == 'coolant_temp':
            self.title = 'KUHLW.'
            self.unit = 'C'
            self.get = ClntTemp
        if _type == 'rpm':
            self.title = 'UMW.'
            self.unit = 'RPM'
            self.get = RPM           

    def _to_GUI(self):
        positions = [self.title_pos, self.value_pos, self.unit_pos]
        fonts = [LabelFont, ValueFont, UnitFont]
        colors = [Labelcolor, Valuecolor, Unitcolor]
        texts = [self.title, self.output, self.unit]

        for pos, font, color, text in zip(positions, fonts, colors, texts):
            tk.Label(
                master=pos['frame'],
                font=font,
                fg=color,
                bg='black',
                text=text,
                textvariable=text
            ).place(
                x=pos['x'],
                y=pos['y'],
                anchor=pos['anchor']
            )
    
    def start(self):
        self._to_GUI()
        self._run()

    def _run(self):
        value = self.get()
        if value == "--":
            self.output.set(value)
        else:
            self.output.set(round(value))
        tk.Frame().after(self.interval, self._run)


def OilTemp():
    U = random.uniform(3,5)
    Vin = 5.25
    #U = (4.096/32768)*adc_1.read_adc(1, gain=1)
    R = 330*((Vin/U)-1)
    if 1 < R < 24000:
        temp = (480608.65298) / \
            (1 + (R/(2.876073*10**-17))**0.1812132) - 96.85298
        value = round(temp, 2)
        if value > 80:
            global Warning
            Warning = 'High Oiltemp'
        return value
    else:
        return "--"

def OilPress():
    value = round(random.uniform(0,80)/10,1)
    #value = (((4.096/32768)*adc_1.read_adc(0, gain=1)-0.475)/4)*9
    if value <= 0.1:
        value = 0
    return value

def ClntTemp():
    U = random.uniform(3,4)
    Vin = 5.25
    #U = (4.096/32768)*adc_1.read_adc(2, gain=1)
    R = 330*((Vin/U)-1)
    if 1 < R < 24000:
        temp = (211749.2077) / \
            (1 + (R/(1.274787*10**-14))**0.185661) - 113.7
        value = round(temp, 2)
        return value
    else:
        value = "--"
        return value

def RPM():
    value = random.uniform(0,6000)
    #value = RPM_signl.frequency()*20
    if value <= 150:
        value = 0
    return value


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
