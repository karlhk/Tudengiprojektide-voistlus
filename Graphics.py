import tkinter as tk


class GUI(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.size = "1350x650"
        self.title = "Koostame graafikut"
        self.icon_path = "images/icon.png"
        self.icon = tk.PhotoImage(file=self.icon_path)

        self.root = root
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.iconphoto(False, self.icon)

        self.state = "opening"
        self.open_file_image = tk.PhotoImage(file="images/opening.png")
        self.image_container = tk.Label(self.root, image=self.open_file_image)
        self.image_container.place(x=0, y=0, relwidth=1, relheight=1)

        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Button-1>', self.mouseclick_on_button)

    def set_image(self, image_path):
        image = tk.PhotoImage(file=image_path)
        self.image_container.configure(image=image)
        self.image_container.image = image

    def motion(self, event):
        x, y = event.x, event.y
        if 125 < x < 400 and 480 < y < 535:
            self.set_image("images/" + self.state + "_hover.png")
        else:
            self.set_image("images/" + self.state + ".png")

    def mouseclick_on_button(self, event):
        x, y = event.x, event.y
        if 125 < x < 400 and 480 < y < 535:
            if self.state == "opening":
                self.change_state("saving")
                self.set_image("images/" + self.state + ".png")
            else:
                self.root.destroy()

    def change_state(self, new_state):
        self.state = new_state


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
