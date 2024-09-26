import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES  # Import the correct class from tkinterdnd2


# Main Application Class
class FileRenumberApp(TkinterDnD.Tk):  # Inherit from TkinterDnD.Tk, not tk.Tk
    def __init__(self):
        super().__init__()
        self.title("File Renumbering Tool")
        self.geometry("600x500")

        # Scrollable frame setup
        self.canvas = tk.Canvas(self, height=200, bg="lightgray")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="lightgray")

        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Create a window in the canvas to hold the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Place the canvas and scrollbar on the screen
        self.canvas.pack(side="left", fill="both", expand=True, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Bind drag-and-drop functionality
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.process_files)

        # Store the file paths in a list
        self.file_list = []
        self.file_labels = []

        # Directory Label
        self.directory_label = tk.Label(self, text="No Output Directory Selected", fg="red")
        self.directory_label.pack(pady=5)

        # Start Number Entry
        self.start_number_label = tk.Label(self, text="Starting Number:")
        self.start_number_label.pack(pady=5)

        self.start_number_var = tk.StringVar()
        self.start_number_entry = tk.Entry(self, textvariable=self.start_number_var, width=10)
        self.start_number_entry.pack(pady=5)
        self.start_number_var.set("1")  # Default starting number is 1

        # Buttons
        self.rename_button = tk.Button(self, text="Rename Files (by Drop Order)", command=self.rename_by_order)
        self.rename_button.pack(pady=10)

        self.rename_button_date = tk.Button(self, text="Rename Files (by Creation Date)", command=self.rename_by_date)
        self.rename_button_date.pack(pady=10)

        self.output_dir_button = tk.Button(self, text="Select Output Directory", command=self.select_output_dir)
        self.output_dir_button.pack(pady=10)

        self.clear_button = tk.Button(self, text="Clear Dropbox", command=self.clear_dropbox)
        self.clear_button.pack(pady=10)

        self.output_dir = None

        # Adding the GitHub label at the bottom-right corner
        self.github_label = tk.Label(self, text="By: Newton667 (Github)", fg="blue", cursor="hand2")
        self.github_label.pack(side="bottom", anchor="se", padx=10, pady=10)

        # Make the label a clickable link to your GitHub profile
        self.github_label.bind("<Button-1>", lambda e: self.open_github())

    def process_files(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file):
                self.file_list.append(file)
        self.update_dropbox_label()

    def update_dropbox_label(self):
        # Clear existing labels
        for label in self.file_labels:
            label.destroy()
        self.file_labels.clear()

        # Add a label for each file
        if self.file_list:
            for file in self.file_list:
                label = tk.Label(self.scrollable_frame, text=os.path.basename(file), anchor="w", bg="lightgray")
                label.pack(fill="x", pady=1)
                self.file_labels.append(label)
        else:
            # If there are no files, display the default message
            label = tk.Label(self.scrollable_frame, text="Drag and Drop Files Here", bg="lightgray")
            label.pack(fill="x", pady=1)
            self.file_labels.append(label)

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.directory_label.config(text=f"Output Directory: {self.output_dir}", fg="green")
        else:
            self.directory_label.config(text="No Output Directory Selected", fg="red")

    def clear_dropbox(self):
        """Clears the dropbox list and updates the UI"""
        self.file_list = []
        self.update_dropbox_label()

    def rename_by_order(self):
        if not self.file_list:
            messagebox.showwarning("No Files", "Please drop some files to rename.")
            return
        if not self.output_dir:
            messagebox.showwarning("No Output Directory", "Please select an output directory.")
            return
        try:
            start_number = int(self.start_number_var.get())
        except ValueError:
            messagebox.showwarning("Invalid Start Number", "Please enter a valid number.")
            return

        for index, file in enumerate(self.file_list, start=start_number):
            self.rename_file(file, f"{index}")

        messagebox.showinfo("Renaming Complete", "Files have been renamed in order.")

    def rename_by_date(self):
        if not self.file_list:
            messagebox.showwarning("No Files", "Please drop some files to rename.")
            return
        if not self.output_dir:
            messagebox.showwarning("No Output Directory", "Please select an output directory.")
            return
        try:
            start_number = int(self.start_number_var.get())
        except ValueError:
            messagebox.showwarning("Invalid Start Number", "Please enter a valid number.")
            return

        # Sort files by creation time
        sorted_files = sorted(self.file_list, key=lambda f: os.path.getctime(f))

        for index, file in enumerate(sorted_files, start=start_number):
            self.rename_file(file, f"{index}")

        messagebox.showinfo("Renaming Complete", "Files have been renamed by creation date.")

    def rename_file(self, file_path, new_name):
        file_extension = os.path.splitext(file_path)[1]
        new_file_name = f"{new_name}{file_extension}"
        new_file_path = os.path.join(self.output_dir, new_file_name)

        try:
            shutil.copy(file_path, new_file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error renaming file: {file_path}\n{e}")

    def open_github(self):
        """Open the GitHub profile in a web browser."""
        import webbrowser
        webbrowser.open("https://github.com/Newton667")


if __name__ == "__main__":
    app = FileRenumberApp()
    app.mainloop()
