from algorithm import Graph, Node
from tkinter import *
import numpy as np

class repEdges:

    def __init__(self, node1, node2, weight, can):
        self.node1  = node1
        self.node2  = node2
        self.weight = weight

        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y
        self.avi    = can.create_line( x1,y1, x2,y2, fill="blue", width = 1.5)
    
        self.xa = 0.5*(x1 + x2)
        self.ya = 0.5*(y1 + y2)

        self.text   = can.create_text(self.xa , self.ya, text=self.weight, fill = "blue")
        self.can    = can

    def draw(self, App):
        App.edges.append(self)
        return(self.avi, self.text)
    
    def highdraw(self):
        self.can.itemconfig(self.text, fill = "green")
        self.can.itemconfig(self.avi , fill = "green")
        #return(self.avi, self.text)
    
    def unhighdraw(self):
        self.can.itemconfig(self.text, fill = "blue")
        self.can.itemconfig(self.avi , fill = "blue")
        #return(self.avi, self.text)
    
    def delete(self, can, App):
        can.delete(self.avi)
        can.delete(self.text)
        App.edges.remove(self)


class DijkApp:

    def __init__(self, window):
        self.drnb   = Button(window, text = "Draw Node", command = self.draw_node)
        self.denb   = Button(window, text = "Delete Node", command = self.delete_node)
        self.drne   = Button(window, text = "Draw Edge", command = self.draw_edge)
        self.dene   = Button(window, text = "Delete Edge", command = self.delete_edge)
        self.canbut = Button(window, text = "Cancel", command = self.cancel_command)
        self.delall = Button(window, text = "Delete All", command = self.delete_all)
        self.perf   = Button(window, text = "Find Paths", command = self.find_paths)
        self.canvas = Canvas(window, width = 600, height = 500, bg = "black")
        self.action = 0
        self.graph  = Graph("MyGraph", [])
        self.edges  = []
        self.window = window
        self.counter = 0
        self.sel     = None
        self.don     = None
        self.upwidge = []
    

    def highlight_path(self):
        t = self.t - 1

        for edge in self.edges:
            edge.unhighdraw()

        for i in range(len(self.paths[t]) - 1):
            for edge in self.edges:
                if (edge.node1 == self.paths[t][i]) and (edge.node2 == self.paths[t][i+1]):
                    edge.highdraw()
                    break
                elif (edge.node2 == self.paths[t][i]) and (edge.node1 == self.paths[t][i+1]):
                    edge.highdraw()
                    break

    
    def cycle_paths(self):
        num = len(self.paths)
        self.t = (self.t % num) + 1
        self.highlight_path()

    def clear_widge(self):
        for item in self.upwidge:
            item.grid_forget()

        self.upwidge = []

        for edge in self.edges:
            edge.unhighdraw()

    def user_action(self, event):

        self.clear_widge()
        
        if self.action == 0:
            pass
        
        elif self.action == 1:

            x = event.x
            y = event.y

            in_name = StringVar()

            in_name_label = Label(self.window, text = "Node Name:", fg = "red")
            in_name_label.grid(row = 2, column = 5)
            self.upwidge.append(in_name_label)

            in_name_entry = Entry(self.window)
            in_name_entry.grid(row = 3, column = 5)
            self.upwidge.append(in_name_entry)

            in_name_button = Button(self.window, text = "Submit", command = lambda: in_name.set( in_name_entry.get() ) )
            in_name_button.grid(row = 4, column = 5)
            self.upwidge.append(in_name_button)
            in_name_button.wait_variable(in_name)

            globals()["node{}".format(self.counter)] = Node( in_name.get() )
            globals()["node{}".format(self.counter)].draw(self.canvas, x, y)
            self.graph.nodes.append( globals()["node{}".format(self.counter)] )
            self.counter += 1

            self.clear_widge()
            self.action = 0
        
        elif self.action == 2:
            
            x = event.x
            y = event.y

            for node in self.graph.nodes:

                if (abs(x - node.x) <= 10) and (abs(y - node.y) <= 10):
                    node.delete(self.canvas)
                    self.graph.delete_node( node )
                    
                    break

            self.clear_widge()
            self.action = 0
        
        elif self.action == 3:

            x = event.x
            y = event.y

            cancel_ = True
            for node in self.graph.nodes:
                if (abs(x - node.x) <= 10) and (abs(y - node.y) <= 10):                    
                    self.sel = node
                    cancel_ = False                   
                    break

            if cancel_:
                self.action = 0
                self.clear_widge()

            else:
                self.action = 3.5
                notice_label_2 = Label(self.window, font = ("Helvetica", 12), text = "Select second node:", fg = "blue", bg = "black")          
                notice_label_2.grid(row = 3, column = 5)
                self.upwidge.append(notice_label_2)
        
        elif self.action == 3.5:

            x = event.x
            y = event.y 

            cancel_ = True
            for node in self.graph.nodes:
                if (abs(x - node.x) <= 10) and (abs(y - node.y) <= 10):                    
                    self.don = node
                    cancel_ = False                   
                    break

            if cancel_:
                self.action = 0
                self.clear_widge()
                return (None)
            else:
                self.action = 3.5
                notice_label_2 = Label(self.window, font = ("Helvetica", 12), text = "Select second node:", fg = "blue", bg = "black")          
                notice_label_2.grid(row = 3, column = 5)
                self.upwidge.append(notice_label_2)
            
            self.clear_widge()

            in_weight = StringVar()

            in_weight_label = Label(self.window, text = "Connection weight:", font = ("Helvetica", 12), fg = "blue", bg = "black")
            in_weight_label.grid(row = 2, column = 5)
            self.upwidge.append(in_weight_label)

            in_weight_entry = Entry(self.window)
            in_weight_entry.grid(row = 3, column = 5)
            self.upwidge.append(in_weight_entry)

            in_weight_button = Button(self.window, text = "Submit", command = lambda: in_weight.set( in_weight_entry.get() ) )
            in_weight_button.grid(row = 4, column = 5)
            self.upwidge.append(in_weight_button)
                      
            while True:

                in_weight_button.wait_variable(in_weight) 
                in_weight_label.grid_forget() 
                con_weight = in_weight.get()

                try:
                    con_weight = float(con_weight)
                    self.clear_widge()
                    break
                except:
                    in_weight_label = Label(self.window, text = "Please enter a valid number", font = ("Helvetica", 15), fg = "blue", bg = "black")
                    in_weight_label.grid(row = 2, column = 5)
                    self.upwidge.append(in_weight_label)

            self.graph.form_connection(self.don, self.sel, con_weight)

            globals()["edge{}".format(self.counter)] = repEdges( self.don, self.sel, con_weight, self.canvas )
            globals()["edge{}".format(self.counter)].draw(self)
            self.counter += 1

            
            self.action = 0

            self.don = None
            self.sel = None
            self.clear_widge()
        
        elif self.action == 4:

            x = event.x
            y = event.y

            for edge in self.edges:

                if (abs(x - edge.xa) <= 10) and (abs(y - edge.ya) <= 10):
                    
                    self.graph.delete_connection(edge.node1, edge.node2)
                    edge.delete(self.canvas, self)
                            
                    break

            self.clear_widge()
            self.action = 0
        
        elif self.action == 5:

            x = event.x
            y = event.y

            cancel_ = True
            for node in self.graph.nodes:
                if (abs(x - node.x) <= 10) and (abs(y - node.y) <= 10):                    
                    self.sel = node
                    cancel_ = False                   
                    break

            if cancel_:
                self.action = 0
                self.clear_widge()

            else:
                self.action = 5.5
                notice_label_2 = Label(self.window, font = ("Helvetica", 12), text = "Select second node:", fg = "green", bg = "black")          
                notice_label_2.grid(row = 3, column = 5)
                self.upwidge.append(notice_label_2)

        elif self.action == 5.5:

            x = event.x
            y = event.y 

            cancel_ = True
            for node in self.graph.nodes:
                if (abs(x - node.x) <= 10) and (abs(y - node.y) <= 10):                    
                    self.don = node
                    cancel_ = False                   
                    break

            if cancel_:
                self.action = 0
                self.clear_widge()
                return (None)
            else:
                self.action = 3.5
                notice_label_2 = Label(self.window, font = ("Helvetica", 12), text = "Select second node:", fg = "light blue", bg = "black")          
                notice_label_2.grid(row = 3, column = 5)
                self.upwidge.append(notice_label_2)
            
            self.clear_widge()
        
            leng = self.graph.dijkstras(self.sel, self.don)[0]

            if leng == None:
                leng_lab = Label(self.window, font = ("Helvetica", 15), text = "No paths found!", fg = "green", bg = "black")
                leng_lab.grid(row = 3, column = 5)
                self.upwidge.append(leng_lab)
                return (None)

            leng_lab = Label(self.window, font = ("Helvetica", 15), text = "Path length = {}".format(leng), fg = "green", bg = "black")
            leng_lab.grid(row = 3, column = 5)
            self.upwidge.append(leng_lab)

            self.paths = self.graph.dijkstras(self.sel, self.don)[1]
            print(self.paths)
            self.t = 0

            self.highlight_path()
            
            next_path_button =  Button(self.window, text = "Next Path", command = self.cycle_paths)
            next_path_button.grid(row = 8, column = 5)
            self.upwidge.append(next_path_button)

        #############


    def build(self):
        self.drnb.grid(row = 2, column = 1)
        self.denb.grid(row = 3, column = 1)
        self.drne.grid(row = 4, column = 1)
        self.dene.grid(row = 5, column = 1)

        self.canbut.grid(row = 2, column = 8)
        self.delall.grid(row = 3, column = 8)
        self.perf.grid(row = 4, column = 8, rowspan = 2)

        self.drnb.config(width = 10)
        self.denb.config(width = 10)
        self.drne.config(width = 10)
        self.dene.config(width = 10)

        self.perf.config(width = 10)
        self.perf.config(height = 2)
        self.canbut.config(width = 10)
        self.delall.config(width = 10)
        
        self.canvas.bind("<Button-1>", self.user_action)
        self.canvas.config(highlightbackground = "white", highlightthickness = 5)
        self.canvas.grid(row = 6, column = 5)

    def draw_node(self):
        self.clear_widge()
        self.action = 1
    
    def delete_node(self):
        self.clear_widge()
        self.action = 2
    
    def draw_edge(self):
        self.clear_widge()
        self.action = 3

        notice_label = Label(self.window,font = ("Helvetica", 15), text = "Select first node:", fg = "blue", bg = "black")          
        notice_label.grid(row = 3, column = 5)
        self.upwidge.append(notice_label)

    def delete_edge(self):
        self.clear_widge()
        self.action = 4
    
    def find_paths(self):
        self.clear_widge()
        self.action = 5

        notice_label = Label(self.window,font = ("Helvetica", 15), text = "Select first node:", fg = "green", bg = "black")          
        notice_label.grid(row = 3, column = 5)
        self.upwidge.append(notice_label)
    
    def cancel_command(self):
        self.sel = None
        self.don = None
        self.action = 0
        self.clear_widge()
    
    def delete_all(self):
        print(self.graph)
        pass

def open_window():

    window = Tk()
    window.title("Graphical Dijkstra's Algorithm")
    window.configure(background = "black")
    window.geometry("850x800")
    
    for row in range(60):
        window.grid_rowconfigure(row, minsize = 10)
    for col in range(60):
        window.grid_columnconfigure(col, minsize = 10)

    title = Label(window, text = "Dijkstra's Algorithm by Puria Radmard", font = ("Helvetica", 20), bg = "black", fg = "red")
    title.grid(row = 1, column = 5)

    run = DijkApp(window)
    run.build()

    window.mainloop()

open_window()