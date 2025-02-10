import customtkinter as ctk
from preview import PreviewWindow
import os
from tkinter import colorchooser, messagebox

# Set Color Scheme Window (Opened via class: GUI - Button: "Change Color Scheme")
class ThemeSelector:
    def __init__(self, parent, colors, gui):
        """Initialize the theme selector window."""
        self.colors = colors
        self.root = ctk.CTkToplevel(parent)
        self.root.title("Select Color Theme")
        self.parent = parent
        self.GUI = gui
        
        # Define available themes
        self.themes = ["Default", "Custom1", "Custom2", "Custom3"]
        
        # Calculate dimensions and position for centering
        w, h = 400, 250
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.grab_set()
        self.root.focus()
        self.root.lift()

        # Create buttons for each theme
        for theme in self.themes:
            button = ctk.CTkButton(
                self.root,
                text=f"Choose '{theme}' Theme",
                command=lambda t=theme: self.change_default(t)
            )
            button.pack(pady=5)
        
        # Button to create a new theme
        self.create = ctk.CTkButton(self.root, text='Create A New Theme')
        self.create.pack(pady=5)

        # Configure the create button callback
        self.create.configure(command=self.create_button_callback)

    def create_button_callback(self):
        """Handle the creation of a new color theme."""
        self.root.withdraw()  # Hide theme selection window

        # Let the user choose colors
        for i, choice in enumerate(self.colors):
            self.choose_color(i, choice)
        self.open_preview()
        self.root.deiconify()  # Show theme selection window again

    def choose_color(self, i, choice):
        """Open a color chooser and update the selected color."""
        color_code = colorchooser.askcolor(color=choice, title=f"Choose Color {i + 1}")

        if color_code[1]:
            self.colors[i] = color_code[1]  # Update color

    def open_preview(self):
        """Open a preview window to display selected colors."""
        preview = PreviewWindow(self.root, self.colors)  # Instantiate preview window

    def change_default(self, t):
        """Change the default color scheme based on user selection."""
        if self.GUI.display_box.get(1.0, 'end').strip():          
            response = messagebox.askyesnocancel("Save Instructions", "The Program Will Restart: Would You Like To Save Your Instructions?")
            if response is True:
                self.GUI.save_instructions_button_callback()
            elif response is False:
                print("Continued Without Saving")
            else:
                print('Canceled')
                return

        with open('color_scheme.txt', 'w') as f:  # Open file for writing
            f.write(f"{os.path.join('themes', t)}.json")  # Write the theme name
        self.GUI.restart()