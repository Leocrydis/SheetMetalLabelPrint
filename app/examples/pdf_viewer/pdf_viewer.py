# Importing necessary modules
from tkinter import *
from tkinter import ttk, filedialog as fd
import os
from miner import PDFMiner  # Assuming miner.py exists


class PDFViewer:
    def __init__(self, master):
        # Initialize PDF properties
        self.path = None
        self.file_is_open = False
        self.current_page = 0
        self.num_pages = 0
        self.miner = None

        # Main window configuration
        self.master = master
        self.master.title("PDF Viewer")
        self.master.geometry("580x520+440+180")
        self.master.resizable(width=0, height=0)  # Fixed window size

        # Create menu and submenus
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_separator()  # Adds separator line
        self.file_menu.add_command(label="Exit", command=self.master.destroy)

        # Top frame for canvas and scrollbars
        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)
        self.top_frame.update()

        # Bottom frame for navigation buttons and page info
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)

        # Scrollbars for the canvas
        self.scroll_y = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scroll_y.grid(row=0, column=1, sticky=(N, S))
        self.scroll_x = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scroll_x.grid(row=1, column=0, sticky=(W, E))

        # Canvas to display the PDF content (images of pages)
        self.canvas = Canvas(
            self.top_frame, bg="#ECE8F3", width=560, height=435,
            yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set
        )
        self.canvas.grid(row=0, column=0)
        # Configure scrollbars with canvas
        self.scroll_y.config(command=self.canvas.yview)
        self.scroll_x.config(command=self.canvas.xview)

        # Buttons for page navigation with temporary text placeholders
        self.up_button = ttk.Button(self.bottom_frame, text="Up", command=self.previous_page)
        self.up_button.grid(row=0, column=1, padx=(270, 5), pady=8)
        self.down_button = ttk.Button(self.bottom_frame, text="Down", command=self.next_page)
        self.down_button.grid(row=0, column=3, pady=8)

        # Label for displaying the current page
        self.page_label = ttk.Label(self.bottom_frame, text="Page 0 of 0")
        self.page_label.grid(row=0, column=4, padx=5)

    def open_file(self):
        # Open file dialog and load a PDF file
        filepath = fd.askopenfilename(
            title="Select a PDF file", initialdir=os.getcwd(),
            filetypes=(("PDF Files", "*.pdf"),)
        )

        if filepath:
            # Initialize PDFMiner with the selected file
            self.path = filepath
            self.miner = PDFMiner(filepath)
            metadata, self.num_pages = self.miner.get_metadata()
            self.file_is_open = True
            self.current_page = 0

            # Set window title to the PDF name
            self.master.title(metadata.get("title", os.path.basename(filepath)[:-4]))
            # Update the display page
            self.display_page()

    def display_page(self):
        if self.file_is_open and 0 <= self.current_page < self.num_pages:
            # Get the current page as an image
            img_file = self.miner.get_page(self.current_page)
            self.canvas.delete("all")  # Clear the canvas
            self.canvas.create_image(0, 0, anchor="nw", image=img_file)
            self.canvas.image = img_file  # Keep a reference to avoid garbage collection
            # Update the scrollable region
            self.canvas.config(scrollregion=self.canvas.bbox(ALL))
            # Update the page label
            self.page_label.config(text=f"Page {self.current_page + 1} of {self.num_pages}")

    def next_page(self):
        if self.file_is_open and self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.file_is_open and self.current_page > 0:
            self.current_page -= 1
            self.display_page()


# Create and run the application
if __name__ == "__main__":
    root = Tk()
    app = PDFViewer(root)
    root.mainloop()
