import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import re
from MongoDBChecker import MongoDBChecker



def save_data():
    # جمع‌آوری داده‌ها از فیلدها
    action = action_type_var.get()
    selector = selector_entry.get()
    value = value_entry.get()
    invalid_values = invalid_values_entry.get().split(',')  # ورود مقادیر نامعتبر، جدا شده با کاما
    max_length = max_length_entry.get()
    contains_digits = contains_digits_var.get()
    allowed_characters = allowed_characters_entry.get()
    expected_error_selector = expected_error_selector_entry.get()

    db_checker = MongoDBChecker(db_name="combined_project_db5", collection_name="interactive_elements")

    # بررسی پر بودن تمامی فیلدهای ضروری
    if not action or not selector or not value or not expected_error_selector or not max_length or not invalid_values or not allowed_characters :
        messagebox.showwarning("Warning", "All fields must be filled out.")
        return

    # بررسی وجود کاراکتر فارسی در مقادیر
    if any(re.search(r'[آ-ی]', field) for field in [selector, value, expected_error_selector]):
        messagebox.showwarning("Warning", "Persian characters are not allowed.")
        return
        # بررسی مقادیر در پایگاه داده

    if db_checker.check_values(action, selector):
        messagebox.showinfo("Database Check", "The combination of action type and selector exists in the database.")
    else:
        messagebox.showinfo("Database Check", "The combination of action type and selector does NOT exist in the database.")
        return

    # ساخت دیکشنری برای قوانین (اگر وجود دارند)
    rules = {}
    if max_length:
        try:
            rules["max_length"] = int(max_length)
        except ValueError:
            messagebox.showwarning("Warning", "Max Length must be an integer.")
            return
    if contains_digits:
        rules["contains_digits"] = bool(contains_digits)
    if allowed_characters:
        rules["allowed_characters"] = allowed_characters

    # ساخت داده برای عمل
    data = {
        "action": action,
        "selector": selector,
        "value": value,
        "invalid_values": invalid_values,
        "expected_error_selector": expected_error_selector,
    }
    if rules:  # اگر قوانین موجود بود، به داده اضافه می‌شود
        data["rules"] = rules

    # افزودن به لیست اقدامات
    actions.append(data)
    messagebox.showinfo("Data Saved", "Action has been saved successfully!")
    update_action_list()

def update_action_list():
    # نمایش لیست اقدامات ثبت شده
    action_list.delete(0, tk.END)
    for i, action in enumerate(actions):
        action_list.insert(tk.END, f"Action {i+1}: {action}")

def delete_action():
    # حذف اقدام انتخاب شده
    selected_index = action_list.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select an action to delete.")
        return
    actions.pop(selected_index[0])
    update_action_list()
    messagebox.showinfo("Action Deleted", "The selected action has been deleted.")

def export_to_json():
    # پرسیدن نام فایل از کاربر
    file_name = simpledialog.askstring("Save As", "Enter the name of the file (without extension):")
    if not file_name:
        messagebox.showwarning("Warning", "File name cannot be empty.")
        return

    # ذخیره داده‌ها به فرمت JSON در یک فایل
    url = url_entry.get()
    data = {
        "url": url,
        "actions": actions
    }
    with open(f"{file_name}.json", "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Export Complete", f"Data exported to {file_name}.json")

# تنظیمات GUI
root = tk.Tk()
root.title("JSON Input GUI")

actions = []  # لیست برای ذخیره اقدامات

# بخش URL
tk.Label(root, text="URL").grid(row=0, column=0)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2)

# نوع عمل
tk.Label(root, text="Action Type").grid(row=1, column=0)
action_type_var = tk.StringVar()
ttk.Combobox(root, textvariable=action_type_var, values=["input", "click"]).grid(row=1, column=1)

# سلکتور
tk.Label(root, text="Selector").grid(row=2, column=0)
selector_entry = tk.Entry(root, width=30)
selector_entry.grid(row=2, column=1)

# مقدار
tk.Label(root, text="Value").grid(row=3, column=0)
value_entry = tk.Entry(root, width=30)
value_entry.grid(row=3, column=1)

# سلکتور خطای مورد انتظار
tk.Label(root, text="Expected Error Selector").grid(row=4, column=0)
expected_error_selector_entry = tk.Entry(root, width=30)
expected_error_selector_entry.grid(row=4, column=1)

# مقادیر نامعتبر
tk.Label(root, text="Invalid Values (comma-separated)").grid(row=5, column=0)
invalid_values_entry = tk.Entry(root, width=30)
invalid_values_entry.grid(row=5, column=1)

# قوانین اعتبارسنجی
tk.Label(root, text="Rules (Optional)").grid(row=6, column=0, columnspan=2)

tk.Label(root, text="Max Length").grid(row=7, column=0)
max_length_entry = tk.Entry(root)
max_length_entry.grid(row=7, column=1)

tk.Label(root, text="Contains Digits").grid(row=8, column=0)
contains_digits_var = tk.BooleanVar()
tk.Checkbutton(root, variable=contains_digits_var).grid(row=8, column=1)

tk.Label(root, text="Allowed Characters (Regex)").grid(row=9, column=0)
allowed_characters_entry = tk.Entry(root)
allowed_characters_entry.grid(row=9, column=1)

# دکمه‌ها
tk.Button(root, text="Save Action", command=save_data).grid(row=10, column=0, columnspan=2)
tk.Button(root, text="Delete Action", command=delete_action).grid(row=11, column=0, columnspan=2)
tk.Button(root, text="Export to JSON", command=export_to_json).grid(row=12, column=0, columnspan=2)

# لیست اقدامات
tk.Label(root, text="Actions List").grid(row=13, column=0, columnspan=2)
action_list = tk.Listbox(root, width=80, height=10)
action_list.grid(row=14, column=0, columnspan=3)

root.mainloop()
