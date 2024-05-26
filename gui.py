import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import csv

class ChequeExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Cheque Extraction System")

        self.label = tk.Label(root, text="Upload Cheque Image")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Browse", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.extract_button = tk.Button(root, text="Extract Data", command=self.extract_data)
        self.extract_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.data_text = tk.Text(root, height=10, width=50)
        self.data_text.pack(pady=10)

        self.cheque_data = {}

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.img = ImageTk.PhotoImage(self.image)
            self.image_label.configure(image=self.img)
            self.image_label.image = self.img
            self.file_path = file_path
            self.save_button.config(state=tk.DISABLED)

    def extract_data(self):
        if hasattr(self, 'file_path'):
            text = pytesseract.image_to_string(self.image)
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, text)
            self.parse_data(text)
            self.save_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("No Image", "Please upload an image first")

    def parse_data(self, text):
        lines = text.split('\n')
        self.cheque_data = {
            "Cheque Number": lines[0] if len(lines) > 0 else "",
            "Date": lines[1] if len(lines) > 1 else "",
            "Amount": lines[2] if len(lines) > 2 else ""
        }

    def save_to_csv(self):
        if self.cheque_data:
            with open('cheque_data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(self.cheque_data.keys())
                writer.writerow(self.cheque_data.values())
            messagebox.showinfo("Saved", "Data saved to cheque_data.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChequeExtractorApp(root)
    root.mainloop()

