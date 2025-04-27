import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
from tkinter import filedialog
from TESTING_FINAL import *

def choose_csv():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    
    if file_paths:
        print(f"Selected files: {file_paths}")
        
        # Update the button text based on selected files
        if len(file_paths) == 1:
            file_name = file_paths[0].split("/")[-1]
            if len(file_name) > 30:
                file_name = file_name[:27] + "..."
            choose_button.config(text=file_name)
        else:
            choose_button.config(text=f"{len(file_paths)} files selected")
        
        # Ask for the directory where to save the files
        save_dir = "DataUse"
        
        if save_dir:
            # Loop through the files and copy them to the selected directory
            for file in file_paths:
                shutil.copy(file, save_dir)
            print(f"Files saved to: {save_dir}")


def show_main_menu():
    # Clear the card first
    for widget in card.winfo_children():
        widget.destroy()

    # Title
    title_label = tk.Label(card, text="Insider Trading Detector", font=("Helvetica", 32, "bold"), bg="#1e293b", fg="#e2e8f0")
    title_label.pack(pady=(30, 20))

    # Info Link
    info_label = tk.Label(card, text="info", font=("Helvetica", 18, "underline"), bg="#1e293b", fg="#38bdf8", cursor="hand2")
    info_label.pack(pady=(0, 30))
    info_label.bind("<Button-1>", lambda e: show_info())

    # CSV Upload
    csv_label = tk.Label(card, text="Upload CSV Files", font=("Helvetica", 18), bg="#1e293b", fg="#94a3b8", anchor="w")
    csv_label.pack(pady=(10, 10))

    global choose_button
    choose_button = tk.Button(
        card,
        text="Choose Files",
        command=choose_csv,
        font=("Helvetica", 16, "bold"),
        bg="#38bdf8",
        fg="#0f172a",
        activebackground="#0ea5e9",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2"
    )
    choose_button.pack(pady=10)

    # Analyze Button
    analyze_button = tk.Button(
        card,
        text="ANALYZE",
        command=analyze_clicked,
        font=("Helvetica", 20, "bold"),
        bg="#22c55e",
        fg="#0f172a",
        activebackground="#16a34a",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=15,
        cursor="hand2"
    )
    analyze_button.pack(pady=40)

def show_info():
    # Clear the card
    for widget in card.winfo_children():
        widget.destroy()

    # Header Title
    header_label = tk.Label(card, text="Information", font=("Helvetica", 32, "bold"), bg="#1e293b", fg="#e2e8f0")
    header_label.pack(pady=(30, 20))

    # Info Text
    info_text = (
        "Insider Trading Detector helps identify unusual insider trading activity across the stock market.\n\n"
        "Built for ease of use, the app focuses on making insider activity monitoring accessible and efficient.\n\n"
        "By highlighting abnormal patterns in insider trades, the app empowers users to spot potential red flags early.\n\n"
        "Developed by: Ashley Benjamin, Amogh Shrivastava, and Karan Bindal\n\n"
        "Team Name: Nernst Equation\n\n"
        "Presented at DragonHacks 2025"
    )

    info_label = tk.Label(card, text=info_text, font=("Helvetica", 16), bg="#1e293b", fg="#e2e8f0", justify="center", wraplength=700)
    info_label.pack(padx=30, pady=20)

    # Back Button
    back_button = tk.Button(
        card,
        text="Back",
        command=show_main_menu,
        font=("Helvetica", 16, "bold"),
        bg="#38bdf8",
        fg="#0f172a",
        activebackground="#0ea5e9",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2"
    )
    back_button.pack(pady=(30, 30))


    
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

def analyze_clicked():
    print("Analyze button clicked! (Backend will be connected here.)")
    try:
        # Create a new top-level window for the text
        new_window = tk.Toplevel(window)
        new_window.title("Analysis Results")
        new_window.configure(bg="#0f172a")
        new_window.geometry("600x400")

        # Add a nice background to the new window (optional)
        background_image = Image.open("image.png")  # Use a different image if you like
        background_image = background_image.resize((600, 400))
        bg_photo = ImageTk.PhotoImage(background_image)

        background_label = tk.Label(new_window, image=bg_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a scrolled text widget to make the text box scrollable
        text_widget = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=70, height=20, font=("Arial", 12), bd=2)
        text_widget.pack(padx=10, pady=10, expand=True)

        # Fetch the text (replace with your actual function)
        text = Test_From_data()  # This should return the text you want to display
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)  # Make it read-only
    except Exception as e:
        print(f"Error: {e}")

def exit_fullscreen(event):
    window.attributes("-fullscreen", False)

# Main Window
window = tk.Tk()
window.title("Insider Trading Detector")
window.configure(bg="#0f172a")

# Fullscreen
window.attributes("-fullscreen", True)
window.bind("<Escape>", exit_fullscreen)

# Background
background_image = Image.open("image.png")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
background_image = background_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(window, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Card Frame
card = tk.Frame(window, bg="#1e293b", bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

# Show Main Menu first
show_main_menu()

# Keep reference
window.bg_photo = bg_photo

window.mainloop()


def exit_fullscreen(event):
    window.attributes("-fullscreen", False)

# Main Window
window = tk.Tk()
window.title("Insider Trading Detector")
window.configure(bg="#0f172a")

# Fullscreen
window.attributes("-fullscreen", True)
window.bind("<Escape>", exit_fullscreen)

# Background
background_image = Image.open("image.png")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
background_image = background_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(window, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Card Frame
card = tk.Frame(window, bg="#1e293b", bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

# Show Main Menu first
show_main_menu()

# Keep reference
window.bg_photo = bg_photo

window.mainloop()
