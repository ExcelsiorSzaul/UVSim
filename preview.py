import customtkinter as ctk
import json
import os

# Color Theme Preview and Save Window (Opened via class: ThemeSelector - Button:"Create A New Theme" )
class PreviewWindow:
    def __init__(self, parent, colors):
        """Initialize the color preview window."""
        ctk.set_default_color_theme('blue')
        self.preview_window = ctk.CTkToplevel(parent)
        self.colors = colors
        self.color_label_names = ['Background', 'Headers/Buttons', 'Text Background', 'Text']
        self.default_colors = ['#1e482c', '#275d38', '#578164', '#E5E9F0']
        self.preview_window.title('Color Preview')
        
        # Calculate dimensions and position for centering
        w, h = 450, 225
        sw, sh = self.preview_window.winfo_screenwidth(), self.preview_window.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
        self.preview_window.geometry(f'{w}x{h}+{x}+{y}')
        self.preview_window.grab_set()
        self.preview_window.focus()
        self.preview_window.lift()

        self.create_preview()  # Create the preview of colors

    def create_preview(self):
        """Generate the preview of selected colors and save buttons."""
        
        def save(file_name):
            """Save the current color scheme to a specified file."""
            try:
                with open(os.path.join('themes', 'Default.json'), 'r') as f:
                    data = json.load(f)  # Load default color scheme
            except FileNotFoundError:
                print("Default.json file not found!")  # Handle missing file
                return
            
            # Update default color scheme with selected colors
            for i, c in enumerate(self.default_colors):
                change_data(data, c, self.colors[i])  # Change old color to new color

            # Save updated color scheme to the specified file
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
            
            # Save the file name for later use
            with open('color_scheme.txt', 'w') as f:
                f.write(file_name)

        def change_data(data, old, new):
            """Recursively change old color values to new in the data structure."""
            for key, value in data.items():
                if isinstance(value, dict):
                    change_data(value, old, new)  # Recurse into dictionaries
                elif isinstance(value, list):
                    # Change color in lists
                    for i in range(len(value)):
                        if isinstance(value[i], str) and value[i] == old:
                            value[i] = new
                elif isinstance(value, str) and value == old:
                    data[key] = new  # Change old value to new

        # Create color labels for each selected color
        for i, color in enumerate(self.colors):
            label = ctk.CTkLabel(self.preview_window, text=f'{self.color_label_names[i]}', fg_color=color, width=120, height=30)
            label.pack(pady=5)  # Add label to the window

        # Create save buttons for custom color schemes
        self.save_button1 = ctk.CTkButton(self.preview_window, width=20, text='Save Custom1')
        self.save_button2 = ctk.CTkButton(self.preview_window, width=20, text='Save Custom2')
        self.save_button3 = ctk.CTkButton(self.preview_window, width=20, text='Save Custom3')
        self.save_button1.pack(side=ctk.LEFT, padx=(70, 5))  # Position save button 1
        self.save_button2.pack(side=ctk.LEFT, padx=5)  # Position save button 2
        self.save_button3.pack(side=ctk.LEFT, padx=5)  # Position save button 3

        # Configure save buttons to call the save function with appropriate filenames
        self.save_button1.configure(command=lambda: save(os.path.join('themes', 'Custom1.json')))
        self.save_button1.configure(command=lambda: save(os.path.join('themes', 'Custom2.json')))
        self.save_button1.configure(command=lambda: save(os.path.join('themes', 'Custom3.json')))

    def destroy_GUI(self):
        """Close the preview window."""
        self.preview_window.destroy()  # Destroy the preview window