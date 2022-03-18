from tkinterweb import HtmlFrame
import tkinter as tk

root = tk.Tk() #create the tkinter window
frame = HtmlFrame(root) #create HTML browser


frame.load_website("http://localhost/project/hr_system") #load a website
frame.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
root.mainloop()