import customtkinter as ctk
import tkinter.filedialog as filedialog
from PIL import Image
import pillow_heif
import os
import threading
from tkinter import messagebox

class HeicConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("HEIC to JPG Converter")
        self.geometry("600x400")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="HEIC to JPG Converter", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Input directory selection
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.input_label = ctk.CTkLabel(self.input_frame, text="Input Folder:")
        self.input_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.input_entry = ctk.CTkEntry(self.input_frame)
        self.input_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.input_button = ctk.CTkButton(
            self.input_frame, 
            text="Browse", 
            command=self.select_input_directory,
            width=100
        )
        self.input_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Output directory selection
        self.output_frame = ctk.CTkFrame(self.main_frame)
        self.output_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.output_frame.grid_columnconfigure(1, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Output Folder:")
        self.output_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.output_entry = ctk.CTkEntry(self.output_frame)
        self.output_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.output_button = ctk.CTkButton(
            self.output_frame, 
            text="Browse", 
            command=self.select_output_directory,
            width=100
        )
        self.output_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        # Status label
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready")
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 10))

        # Convert button
        self.convert_button = ctk.CTkButton(
            self.main_frame,
            text="Convert",
            command=self.start_conversion,
            height=40
        )
        self.convert_button.grid(row=5, column=0, padx=20, pady=(0, 20))

    def select_input_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, directory)

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, directory)

    def convert_images(self):
        input_dir = self.input_entry.get()
        output_dir = self.output_entry.get()

        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Please select both input and output directories")
            return

        heic_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.heic')]
        total_files = len(heic_files)

        if total_files == 0:
            messagebox.showinfo("Info", "No HEIC files found in the input directory")
            return

        for i, file in enumerate(heic_files, 1):
            try:
                input_path = os.path.join(input_dir, file)
                output_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.jpg')

                heif_file = pillow_heif.read_heif(input_path)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                )

                image.save(output_path, format="JPEG")

                progress = i / total_files
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Converting: {i}/{total_files}")
                self.update()

            except Exception as e:
                messagebox.showerror("Error", f"Error converting {file}: {str(e)}")

        self.status_label.configure(text="Conversion Complete!")
        messagebox.showinfo("Success", "All files have been converted!")
        self.progress_bar.set(0)

    def start_conversion(self):
        self.convert_button.configure(state="disabled")
        threading.Thread(target=self.convert_images, daemon=True).start()
        self.convert_button.configure(state="normal")

if __name__ == "__main__":
    app = HeicConverterApp()
    app.mainloop()
