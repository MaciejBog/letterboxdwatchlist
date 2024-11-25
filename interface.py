from tkinter import *
from tkinter.ttk import Progressbar

from soup import SoupMaker
import random
import webbrowser
from PIL import ImageTk, Image
import os

def callback(url):
    webbrowser.open_new_tab(url)


class Interface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Letterboxd Random Film Chooser")
        self.window.config(padx=50, pady=50)

        self.title_text = Label(text="Choose a random film from a Letterboxd list")
        self.title_text.grid(column=1,row=0)

        self.provide_text = Label(text="Provide URL here:")
        self.provide_text.grid(column=1, row=1)

        self.link_here = Entry()
        self.link_here.grid(column=0, row=2, columnspan=2)

        self.submit_url_button = Button(text="Submit URL", command=self.create_soup)
        self.submit_url_button.grid(column=2, row=2)

        self.window.bind('<Return>', self.create_soup)

        self.film_title = Label(text="")
        self.film_title.grid(column=1,row=3)

        self.image = ImageTk.PhotoImage(Image.open("placeholder-movieimage.png"))
        self.poster = Button(image=self.image)
        self.poster.grid(column=1, row=4)

        self.window.protocol("WM_DELETE_WINDOW", self._quit)

        self.window.mainloop()



    def create_soup(self,event=None):
        new_window = Toplevel(self.window)
        new_window.title("Progress bar")
        new_window.geometry("200x200")
        new_window_text = Label(new_window,
          text ="Please wait, getting film data!")
        new_window_text.grid(column=1, row=0)

        self.window.update()

        html = self.link_here.get()
        if html[-1] != "/":
            html += "/"
        soup = SoupMaker(html)
        random_choice = random.choice(soup.title_list)
        random_link = "https://" + soup.link_list[soup.title_list.index(random_choice)]
        soup.find_poster_image(random_link)
        self.film_title.config(text=f"The film for today is:\n{random_choice}")
        self.image = ImageTk.PhotoImage(Image.open("pic1.jpg"))
        self.poster.config(image=self.image, command= lambda: callback(random_link))
        new_window.destroy()


    def _quit(self):
        if os.path.exists("pic1.jpg"):
            os.remove("pic1.jpg")
        else:
            pass
        self.window.quit()
        self.window.destroy()
