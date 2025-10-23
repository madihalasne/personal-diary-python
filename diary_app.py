import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from tkinter import ttk
import datetime

# ---------- PASSWORD SETUP ---------- #
PASSWORD = "mypassword"

def ask_password():
    pwd = simpledialog.askstring("Password", "Enter your diary password:", show="*")
    if pwd != PASSWORD:
        messagebox.showerror("Access Denied", "Wrong Password! ❌")
        return False
    return True

# ---------- GLOBAL VARIABLES ----------
theme_colors = {
    "Light": {"bg": "#fff0f5", "text_bg": "#fffaf0", "fg": "#3c096c"},
    "Dark": {"bg": "#2e2e2e", "text_bg": "#3c3c3c", "fg": "#e0e0e0"}
}

current_theme = "Light"
window = None
text_area = None
stats_label = None
date_entry = None
mood_var = None

# ---------- THEME SWITCH FUNCTION ----------
def switch_theme():
    global current_theme
    current_theme = theme_var.get()
    colors = theme_colors[current_theme]
    window.config(bg=colors["bg"])
    text_area.config(bg=colors["text_bg"], fg=colors["fg"])
    stats_label.config(bg=colors["bg"], fg=colors["fg"])

# ---------- STATS ----------
def update_stats():
    try:
        with open("diary.txt", "r", encoding="utf-8") as f:
            content = f.read()
            entries = content.split("-"*50)
            total_entries = len([e for e in entries if e.strip() != ""])
            total_words = len(content.split())
            stats_label.config(text=f"📖 Entries: {total_entries} | 📝 Words: {total_words}")
    except FileNotFoundError:
        stats_label.config(text="📖 Entries: 0 | 📝 Words: 0")

# ---------- SAVE ENTRY ----------
def save_entry():
    entry_text = text_area.get("1.0", tk.END).strip()
    if entry_text == "":
        messagebox.showwarning("Empty Entry", "Write something before saving!")
        return
    mood = mood_var.get()
    date = date_entry.get().strip()
    if not date:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
    with open("diary.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{date}] [{mood}]\n{entry_text}\n{'-'*50}\n")
    text_area.delete("1.0", tk.END)
    messagebox.showinfo("Saved", "✨ Entry saved successfully! ✨")
    update_stats()

# ---------- VIEW ENTRIES ----------
def view_entries():
    try:
        with open("diary.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        messagebox.showinfo("No Entries", "No diary entries yet!")
        return
    show_entries_window(content, "💌 My Diary Entries 💌")

# ---------- SEARCH ----------
def search_entries():
    keyword = simpledialog.askstring("Search", "Enter a keyword to search:")
    if not keyword:
        return
    try:
        with open("diary.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        messagebox.showinfo("No Entries", "No diary entries yet!")
        return
    results = ""
    for entry in content.split("-"*50):
        if keyword.lower() in entry.lower():
            results += entry.strip() + "\n" + "-"*50 + "\n"
    if results == "":
        messagebox.showinfo("No Results", f"No entries found with '{keyword}'.")
        return
    show_entries_window(results, f"Search Results for '{keyword}'")

# ---------- SHOW ENTRIES WITH EDIT/DELETE ----------
def show_entries_window(content, title):
    win = tk.Toplevel(window)
    win.title(title)
    win.geometry("600x500")
    colors = theme_colors[current_theme]
    win.config(bg=colors["bg"])

    text_display = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Helvetica", 12),
                                             bg=colors["text_bg"], fg=colors["fg"])
    text_display.insert(tk.END, content)
    text_display.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

    def edit_entry():
        try:
            selected_text = text_display.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showwarning("Select Text", "Select an entry to edit.")
            return
        new_text = simpledialog.askstring("Edit Entry", "Modify your entry:", initialvalue=selected_text)
        if new_text:
            full_content = text_display.get("1.0", tk.END)
            updated_content = full_content.replace(selected_text, new_text)
            with open("diary.txt", "w", encoding="utf-8") as f:
                f.write(updated_content)
            text_display.delete("1.0", tk.END)
            text_display.insert(tk.END, updated_content)
            update_stats()
            messagebox.showinfo("Updated", "Entry updated successfully!")

    def delete_entry():
        try:
            selected_text = text_display.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showwarning("Select Text", "Select an entry to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
            full_content = text_display.get("1.0", tk.END)
            updated_content = full_content.replace(selected_text, "")
            with open("diary.txt", "w", encoding="utf-8") as f:
                f.write(updated_content)
            text_display.delete("1.0", tk.END)
            text_display.insert(tk.END, updated_content)
            update_stats()
            messagebox.showinfo("Deleted", "Entry deleted successfully!")

    btn_frame = tk.Frame(win, bg=colors["bg"])
    btn_frame.pack(pady=10)
    button_style = {"font": ("Helvetica", 12, "bold"), "width": 15, "bd": 0, "relief": "ridge", "activebackground": "#ffcad4"}

    tk.Button(btn_frame, text="✏️ Edit Entry", command=edit_entry, bg="#ffd6a5", fg="#4b2e83", **button_style).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="🗑️ Delete Entry", command=delete_entry, bg="#ffadad", fg="#4b2e83", **button_style).grid(row=0, column=1, padx=10)

# ---------- MAIN WINDOW ----------
def start_diary():
    global window, text_area, stats_label, date_entry, mood_var
    window = tk.Tk()
    window.title("🌸 Personal Diary 🌸")
    window.geometry("600x700")
    colors = theme_colors[current_theme]
    window.config(bg=colors["bg"])

    # Title
    tk.Label(window, text="💖 My Personal Diary 💖", font=("Comic Sans MS", 22, "bold"),
             bg=colors["bg"], fg="#e75480").pack(pady=10)

    # Theme selector
    global theme_var
    theme_var = tk.StringVar(value=current_theme)
    theme_menu = ttk.Combobox(window, textvariable=theme_var, values=["Light", "Dark"], state="readonly", width=10)
    theme_menu.pack(pady=5)
    theme_menu.bind("<<ComboboxSelected>>", lambda e: switch_theme())

    # Date selector
    tk.Label(window, text="Date (YYYY-MM-DD, optional):", bg=colors["bg"], fg=colors["fg"]).pack()
    date_entry = tk.Entry(window, width=15)
    date_entry.pack(pady=5)

    # Mood selector
    tk.Label(window, text="Mood:", bg=colors["bg"], fg=colors["fg"]).pack()
    mood_var = tk.StringVar(value="😊")
    moods = ["😊 Happy", "😢 Sad", "😡 Angry", "😎 Cool", "❤️ Love"]
    mood_menu = ttk.Combobox(window, textvariable=mood_var, values=moods, state="readonly", width=10)
    mood_menu.pack(pady=5)

    # Text area
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=65, height=20,
                                          font=("Arial", 13), bg=colors["text_bg"], fg=colors["fg"],
                                          bd=5, relief=tk.RIDGE)
    text_area.pack(padx=15, pady=10)

    # Stats
    stats_label = tk.Label(window, text="", font=("Arial", 12), bg=colors["bg"], fg=colors["fg"])
    stats_label.pack()
    update_stats()

    # Buttons
    btn_frame = tk.Frame(window, bg=colors["bg"])
    btn_frame.pack(pady=15)
    button_style = {"font": ("Helvetica", 12, "bold"), "width": 15, "bd": 0, "relief": "ridge", "activebackground": "#ffcad4"}

    tk.Button(btn_frame, text="💾 Save Entry", command=save_entry, bg="#ffadad", fg="#4b2e83", **button_style).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="📖 View Entries", command=view_entries, bg="#ffd6a5", fg="#4b2e83", **button_style).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="🔍 Search Entries", command=search_entries, bg="#caffbf", fg="#4b2e83", **button_style).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(btn_frame, text="❌ Exit", command=window.destroy, bg="#f5a3a3", fg="#4b2e83", **button_style).grid(row=1, column=1, padx=10, pady=10)

    window.mainloop()

# ---------- RUN ----------
if ask_password():
    start_diary()
