import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import requests
import json
import html
import time

# Constants
DEFAULT_THEME_COLOR = "#2c2c2c"
DEFAULT_WINDOW_SIZE = "800x600"

def make_request():
    """
    Send an HTTP request and display the response in the GUI.
    """
    url = url_entry.get()
    method = method_var.get()
    headers_text_input = headers_text.get("1.0", tk.END).strip()
    data_text_input = data_text.get("1.0", tk.END).strip()

    try:
        headers_dict = parse_headers(headers_text_input)
        data = data_text_input if method in ["POST", "PUT"] else None

        response = send_request(url, method, headers_dict, data)

        status_code_text.delete("1.0", tk.END)
        status_code_text.insert(tk.END, f"Status Code: {response.status_code}")

        headers_output_text.delete("1.0", tk.END)
        headers_output_text.insert(tk.END, "Response Headers:\n")
        for key, value in response.headers.items():
            headers_output_text.insert(tk.END, f"{key}: {value}\n")

        response_text = get_response_text(response)
        escaped_response_text = html.escape(response_text)  # Escape HTML entities

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Response Content:\n{escaped_response_text}")

        request_history.insert(tk.END, f"{method} {url}\n{headers_text_input}\n{data_text_input}\n\n")
        generate_code(url, method, headers_dict, data_text_input)
    except Exception as e:
        result_text.insert(tk.END, f"An error occurred: {e}\n")

def parse_headers(headers_text):
    """
    Parse the headers text input into a dictionary.
    """
    headers_dict = {}
    if headers_text:
        headers_list = headers_text.split("\n")
        for header in headers_list:
            try:
                key, value = header.split(":", 1)
                headers_dict[key.strip()] = value.strip()
            except ValueError:
                pass  # Skip invalid header lines
    return headers_dict

def send_request(url, method, headers, data):
    """
    Send an HTTP request using the requests library.
    """
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=data)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Invalid HTTP method: {method}")

    response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response

def get_response_text(response):
    """
    Get the response content as text, handling different content types.
    """
    try:
        response_json = response.json()
        response_text = json.dumps(response_json, indent=4)
    except ValueError:
        response_text = response.text
    return response_text

def save_request():
    """
    Save the current request to a file.
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(url_entry.get() + "\n")
            f.write(method_var.get() + "\n")
            f.write(headers_text.get("1.0", tk.END))
            f.write(data_text.get("1.0", tk.END))

def load_request():
    """
    Load a request from a file.
    """
    file_path = filedialog.askopenfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "r") as f:
            lines = f.readlines()
            url_entry.delete(0, tk.END)
            url_entry.insert(0, lines[0].strip())
            method_var.set(lines[1].strip())
            headers_text.delete("1.0", tk.END)
            headers_text.insert("1.0", "".join(lines[2:]))
            data_text.delete("1.0", tk.END)
            data_text.insert("1.0", "".join(lines[3:]))

def generate_code(url, method, headers, data):
    """
    Generate Python code for the current request.
    """
    python_code = "import requests\n\n"
    python_code += f"url = '{url}'\n"
    python_code += f"headers = {headers}\n"
    python_code += f"data = '{data}'\n\n"

    if method == 'GET':
        python_code += "response = requests.get(url, headers=headers)\n"
    elif method == 'POST':
        python_code += "response = requests.post(url, headers=headers, data=data)\n"
    elif method == 'PUT':
        python_code += "response = requests.put(url, headers=headers, data=data)\n"
    elif method == 'DELETE':
        python_code += "response = requests.delete(url, headers=headers)\n"

    python_code += "\nprint(response.status_code)\n"
    python_code += "print(response.headers)\n"
    python_code += "print(response.text)\n"

    code_text.delete("1.0", tk.END)
    code_text.insert(tk.END, python_code)

def change_theme(new_color=None):
    """
    Change the theme of the application.
    """
    if new_color is None:
        new_color = DEFAULT_THEME_COLOR

    style = ttk.Style()
    style.theme_use("default")

    # Configure window background
    window.configure(bg=new_color)

    # Configure notebook
    style.configure("TNotebook", background=new_color)
    style.map("TNotebook.Tab", background=[("selected", new_color), ("active", new_color)])

    # Configure notebook tabs
    tab_style = ttk.Style()
    tab_style.configure("Custom.TNotebook.Tab", background=new_color, foreground="white")
    notebook.configure(style="Custom.TNotebook")

    # Configure buttons
    button_color = DEFAULT_THEME_COLOR
    button_fg = "white"

    # Configure other widgets
    for widget in window.winfo_children():
        if isinstance(widget, ttk.Notebook):
            continue  # Skip the notebook widget
        if isinstance(widget, tk.Button):
            widget.configure(bg=button_color, fg=button_fg, activebackground=button_color, activeforeground=button_fg)
        else:
            widget.configure(bg=new_color, fg="white")

def choose_theme():
    """
    Open a color chooser dialog to select a new theme color.
    """
    new_color = colorchooser.askcolor(title="Select Theme Color")
    if new_color and new_color[1]:
        change_theme(new_color[1])

def show_info():
    info_window = tk.Toplevel(window)
    info_window.title("About API Testing Tool by Evil Bane")
    info_window.geometry("500x400")
    info_window.configure(bg=DEFAULT_THEME_COLOR)

    info_label = tk.Label(info_window, text="API Testing Tool", fg="white", bg=DEFAULT_THEME_COLOR, font=("Arial", 16, "bold"))
    info_label.pack(pady=10)
    description_text = tk.Text(info_window, height=15, width=50, bg=DEFAULT_THEME_COLOR, fg="white", font=("Arial", 12))
    description_text.insert(tk.END, "This tool allows you to easily test APIs by sending HTTP requests and inspecting the responses. You can set the URL, HTTP method, headers, and request data, and the tool will display the response status code, headers, and content. \n\nCreator: Evil Bane")
    description_text.configure(state="disabled")
    description_text.pack(pady=10)

def animate_window():
    window.overrideredirect(True)  # Remove window decorations
    window.attributes('-alpha', 0.0)  # Set transparency to 0 (fully transparent)
    window.geometry("+{}+{}".format(window.winfo_screenwidth() // 2, window.winfo_screenheight() // 2))  # Center the window

    for alpha in range(0, 11):
        alpha_value = alpha / 10
        window.attributes('-alpha', alpha_value)  # Gradually increase transparency
        time.sleep(0.03)  # Pause for a short duration

    window.overrideredirect(False)  # Restore window decorations

# Create the main window
window = tk.Tk()
window.title("API Testing Tool")
window.geometry(DEFAULT_WINDOW_SIZE)

# Add menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create Info menu
info_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Info", menu=info_menu)
info_menu.add_command(label="About", command=show_info)

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

# Create tabs
request_tab = ttk.Frame(notebook)
response_tab = ttk.Frame(notebook)
history_tab = ttk.Frame(notebook)
code_tab = ttk.Frame(notebook)
notebook.add(request_tab, text="Request")
notebook.add(response_tab, text="Response")
notebook.add(history_tab, text="Request History")
notebook.add(code_tab, text="Code Generation")

# Request tab
# URL input
url_label = tk.Label(request_tab, text="API URL:")
url_label.pack()
url_entry = tk.Entry(request_tab, width=100)
url_entry.pack()

# HTTP method selection
method_var = tk.StringVar(value="GET")
method_label = tk.Label(request_tab, text="HTTP Method:")
method_label.pack()
method_frame = tk.Frame(request_tab)
method_frame.pack()
tk.Radiobutton(method_frame, text="GET", variable=method_var, value="GET").pack(side=tk.LEFT)
tk.Radiobutton(method_frame, text="POST", variable=method_var, value="POST").pack(side=tk.LEFT)
tk.Radiobutton(method_frame, text="PUT", variable=method_var, value="PUT").pack(side=tk.LEFT)
tk.Radiobutton(method_frame, text="DELETE", variable=method_var, value="DELETE").pack(side=tk.LEFT)

# Headers input
headers_label = tk.Label(request_tab, text="Request Headers (one per line, key:value format):")
headers_label.pack()
headers_text = tk.Text(request_tab, height=5, width=100)
headers_text.pack()

# Data input
data_label = tk.Label(request_tab, text="Request Data:")
data_label.pack()
data_text = tk.Text(request_tab, height=5, width=100)
data_text.pack()

# Make request button
request_button = tk.Button(request_tab, text="Make Request", command=make_request)
request_button.pack()

# Save and Load buttons
save_button = tk.Button(request_tab, text="Save Request", command=save_request)
save_button.pack(side=tk.LEFT, padx=5, pady=5)
load_button = tk.Button(request_tab, text="Load Request", command=load_request)
load_button.pack(side=tk.LEFT, padx=5, pady=5)

# Response tab
# Status code
status_code_label = tk.Label(response_tab, text="Status Code:")
status_code_label.pack()
status_code_text = tk.Text(response_tab, height=1, width=100)
status_code_text.pack()

# Response headers
headers_output_label = tk.Label(response_tab, text="Response Headers:")
headers_output_label.pack()
headers_output_text = tk.Text(response_tab, height=10, width=100)
headers_output_text.pack()

# Response content
result_label = tk.Label(response_tab, text="Response Content:")
result_label.pack()
result_text = tk.Text(response_tab, height=20, width=100)
result_text.pack()

# Request History tab
request_history = tk.Text(history_tab, height=20, width=100)
request_history.pack()

# Code Generation tab
code_label = tk.Label(code_tab, text="Python Code:")
code_label.pack()
code_text = tk.Text(code_tab, height=20, width=100)
code_text.pack()

# Theme button
theme_button = tk.Button(window, text="Change Theme", command=choose_theme, bg=DEFAULT_THEME_COLOR, fg="white", activebackground=DEFAULT_THEME_COLOR, activeforeground="white")
theme_button.pack(side=tk.BOTTOM, pady=5)

# Set initial theme
change_theme()  # Black matte finish theme

# Add opening animation
animate_window()

# Run the GUI event loop
window.mainloop()
