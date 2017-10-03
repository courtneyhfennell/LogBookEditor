import tkinter as tk
from tkinter.constants import TOP
from idlelib.searchengine import get_selection


LARGE_FONT= ("Verdana", 12)

plane_list_btn = []
n_list =[]
global mi 
      
class Logbook_Editor(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        mi= tk.PhotoImage(file="C:\\Users\\courtney.fennell\\Documents\\GitHub\\LogBookEditor\\1.png")
        
  
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Planes_Page, N_Page, Mech_Tac_Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Planes_Page)

    def show_frame(self, page_name):

        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

     
class Planes_Page(tk.Frame):
    from LogBook_Utilities.LB_Util import get_plane_types, set_plane_type
    
    def execute_things(self, index, plane, controller):
        # This line would be where you insert the letter in the textbox
        
        #disables the one plane type that was selected
        for i in range(len(plane_list_btn)):
            plane_list_btn[i].config(state="normal")
        plane_list_btn[index].config(state="disabled")
        print(plane)
        self.set_plane_type(plane)
        
        #show next page
        controller.show_frame(N_Page)
        
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
    
        self.bind("<<ShowFrame>>", self.on_show_frame(controller))
    
    
    #loop through all of the plane types and add the buttons to the screen
    def on_show_frame(self, controller):
        #mi= tk.PhotoImage(file="C:\\Users\\courtney.fennell\\Documents\\GitHub\\LogBookEditor\\1.png")
        
  
        print("planes_page")
        #pull all of the planes from the directories
        all_planes = self.get_plane_types()
        
        for index in range(len(all_planes)): 
            
            n=all_planes[index]
        
            btn = tk.Button(self, text=all_planes[index],
                            command=lambda index=index, n=n: self.execute_things(index, n, controller) )
        
            # Add the button to the window
            #btn.config(image=mi, compound=TOP)
            #btn.image = mi
            btn.grid(column = index+1, 
                     row = 1, 
                     padx = 5, 
                     pady=5, 
                     ipadx = 5,
                     ipady = 5,
                     sticky=tk.E+tk.W+tk.S+tk.N)
        
            # Add a reference to the button to 'buttons'
            plane_list_btn.append(btn)
            
        
        label = tk.Label(self, text="Select a plane", font=LARGE_FONT)
        
        #this centers the label no matter how many plane options there are
        x = round(len(plane_list_btn)/2)
        if(x <=-1):
            x=1
            
        if(len(plane_list_btn)%2 == 0): #if x is even  
            label.grid(row = 0,  column=x,  columnspan=2, pady=10,padx=10)
        else:
            label.grid(row = 0,  column=x,  columnspan=3, pady=10,padx=10)


class N_Page(tk.Frame):
    from LogBook_Utilities.LB_Util import collect_planes_n, set_plane_n, roll_back_plane_type
    
    def next_page(self, index, n, n_list, controller):
        # This line would be where you insert the letter in the textbox
        
        for i in range(len(n_list)):
            n_list[i].config(state="normal")
        n_list[index].config(state="disabled")
        
        self.set_plane_n(n)
        
        #show next frame
        controller.show_frame(Mech_Tac_Page)
        
    def previous_page(self, controller):  
            self.roll_back_plane_type() 
            controller.show_frame(Planes_Page)
               
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="N Page", font=LARGE_FONT)
        label.grid(row = 0,  column=2, columnspan=2, sticky=tk.E, pady=10,padx=10)

        
        self.bind("<<ShowFrame>>", lambda _: self.on_show_frame(controller))

    def on_show_frame(self, controller):
        
        
        for widget in tk.Frame.winfo_children(self):
            widget.destroy()
            n_list = []
        

        
       
        all_planes = self.collect_planes_n()
       
        #loop through all of the planes and add the buttons to the screen
        for index in range(len(all_planes)): 
            n=all_planes[index]
            
            button = tk.Button(self, text=all_planes[index],
                            command=lambda index=index, n=n: self.next_page(index, n, n_list, controller)) 
        
            # Add the button to the window
            button.grid(column = index+1, 
                     row = 1, 
                     padx = 5, 
                     pady=5, 
                     ipadx = 5,
                     ipady = 5,
                     sticky=tk.E+tk.W+tk.S+tk.N)
        
            # Add a reference to the button to 'buttons'
            n_list.insert(index, button)
        
        prev_btn = tk.Button(self, text="Prev",
                            command=lambda: self.previous_page(controller))
        prev_btn.grid(row = 2,  column=0, 
                      padx = 5, pady=5, 
                      ipadx = 5, ipady = 5,
                      sticky=tk.W)
        n_list.insert(len(all_planes) +1, prev_btn)
        
        label = tk.Label(self, text="N Page", font=LARGE_FONT)
        x = round(len(n_list)/2)-1
        print(x)
        if(x <=-1):
            x=1
            
        label.grid(row = 0,  column=x, columnspan=2, pady=10,padx=10)


class Mech_Tac_Page(tk.Frame):
    from LogBook_Utilities.LB_Util import roll_back_plane, get_aplist, submit
    
    def submit_quit(self, selected_mech):
        self.submit(selected_mech)
        app.quit()
        
    def previous_page(self, controller):  
        self.roll_back_plane() 
        controller.show_frame(N_Page)
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) 
        Mech_list = self.get_aplist()
        
        self.bind("<<ShowFrame>>",lambda _: self.on_show_frame(controller, Mech_list))

    def on_show_frame(self, controller, Mech_list):
        for widget in tk.Frame.winfo_children(self):
            widget.destroy()
            n_list = []
            
        
        '''
        label = tk.Label(self, text="Mech Page", font=LARGE_FONT)
        label.grid(column = 1, 
                     row = 1, 
                     padx = 5, 
                     pady=5, 
                     ipadx = 5,
                     ipady = 5,
                     sticky=tk.E+tk.W+tk.S+tk.N)
        '''
        
        optionList = []
        for key in Mech_list: 
            optionList.append(key)
        self.dropVar=tk.StringVar()
        self.dropVar.set(optionList[0]) # default choice
        self.dropMenu1 = tk.OptionMenu(self, self.dropVar, *optionList)  
        self.dropMenu1.grid(column = 1, 
                            columnspan=2,
                            row = 0, 
                            padx = 5, 
                            pady = 5, 
                            ipadx = 5,
                            ipady = 5,
                            sticky=tk.E+tk.W+tk.S+tk.N)
        
        self.TacLbl = tk.Label(self, text="Tach time: ")
        self.TacLbl.grid(column = 0, 
                         row = 1, 
                         padx = 5, 
                         pady=5, 
                         ipadx = 5,
                         ipady = 5,
                         sticky=tk.E+tk.W+tk.S+tk.N)
        self.input = tk.Entry(self, bd=5)
        self.input.grid(column = 1, 
                        columnspan=2,
                        row = 1, 
                        padx = 5, 
                        pady=5, 
                        ipadx = 5,
                        ipady = 5,
                        sticky=tk.E+tk.W+tk.S+tk.N)
        
        
        #previous button
        prev_btn = tk.Button(self, text="Prev",
                            command=lambda: self.previous_page(controller))
        prev_btn.grid(  column = 0,  
                        row = 2, 
                        padx = 5, 
                        pady=5, 
                        ipadx = 5,
                        ipady = 5,
                        sticky=tk.E+tk.W+tk.S+tk.N)   
        
        #submit button
        submit_btn = tk.Button(self, text="Submit",
                            command=lambda: self.submit_quit(self.dropVar.get()))
        
        submit_btn.grid(column = 2, 
                        row = 2, 
                        padx = 5, 
                        pady=5, 
                        ipadx = 5,
                        ipady = 5,
                        sticky=tk.E+tk.W+tk.S+tk.N)
        
    
app = Logbook_Editor()
app.mainloop()
