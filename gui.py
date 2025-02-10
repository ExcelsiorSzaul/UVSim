import customtkinter as ctk
from tkinter import colorchooser, filedialog, ttk
from sim import Sim
import json
import os
import threading
from theme_selector import ThemeSelector

# Main GUI
class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        """Initialize the UVSim GUI and its components."""
        # Load color scheme from file and set it as the default theme
        with open('color_scheme.txt', 'r') as f:
            scheme = f.readline().strip()  
        ctk.set_default_color_theme(scheme)  

        # Color Order: Background, Frame/button, Hover/EntryBox, Text 
        self.colors = ['#1e482c', '#275d38', '#578164', '#E5E9F0']

        # Store future textboxes
        self.textboxes = []
    
        # Other Variables
        self.new_word = '+0000'
        self.active_tab_index = None
        self.is_closed = False

        # Main Window Initialization
        self.root = ctk.CTk()  
        self.root.resizable(False, False) 
        ctk.set_appearance_mode('dark')
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_close)
        
        # Define window dimensions and center it on the screen
        w, h = 1200, 850  
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2) 
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.title('UVSim')  

        # Frame Creation
        # ----------- Main Frames ------------
        self.main_frame = ctk.CTkFrame(self.root) 
        self.input_frame = ctk.CTkFrame(self.root)

        self.main_frame.grid(row=0, column=0, padx=50, pady=20, sticky='nesw')
        self.input_frame.grid(row=1, column=0, padx=50, sticky='nesw')

        # ------------ Sub Frames ------------ 
        self.display_frame = ctk.CTkFrame(self.main_frame)  
        self.register_display = ctk.CTkFrame(self.main_frame)

        self.display_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky='nesw')
        self.register_display.grid(row=0, column=1, padx=(10, 0), pady=0, sticky='nesw')

        # Widget Creation
        # ------------ Text Boxes ------------
        self.entry_box = ctk.CTkEntry(self.input_frame, width=300, height=40)
        self.display_box = ttk.Notebook(self.display_frame, width=900, height=665)  
        self.register_box = ctk.CTkTextbox(self.register_display, width=175, height=400)
        self.sim_output_box = ctk.CTkTextbox(self.register_display, width=175, height=200)
        self.add_new_tab()

        # -------------- Labels -------------- 
        self.display_label = ctk.CTkLabel(self.display_frame, width=100, height=25, text='--- Ready For Instructions ---', font=('Roboto', 25), pady=5)  
        self.registers_label = ctk.CTkLabel(self.register_display, width=100, height=25, text='Registers', font=('Roboto', 25), pady=5)
        self.input_status_label = ctk.CTkLabel(self.input_frame, width=100, height=10, text='', font=('Roboto', 12), pady=5)
        self.sim_output_label = ctk.CTkLabel(self.register_display, width=100, height=25, text='Output', font=('Roboto', 25))

        # -------------- Buttons -------------
        self.load_instructions_button = ctk.CTkButton(self.input_frame, text='Load', width=110, height=40) 
        self.save_instructions_button = ctk.CTkButton(self.input_frame, text='Save', width=110, height=40)
        ###### might remove #######\/\/\/\/\/\/\/\/\/
        #self.convert_instructions_button = ctk.CTkButton(self.input_frame, text='Convert', width=110, height=40)  
        self.color_change_button = ctk.CTkButton(self.input_frame, text='Change Color Scheme', width=110, height=40)
        self.run_button = ctk.CTkButton(self.input_frame, text="Run", width=110, height=40)
        self.submit_button = ctk.CTkButton(self.input_frame,text="Submit", width=110, height=40)
        self.add_tab_button = ctk.CTkButton(self.input_frame, text='Add Tab', width=110, height=40, command=self.add_new_tab)

        # Instantiate Widgets
        # ----------- Display Frame -----------
        self.display_label.grid(row=0, column=0)  
        self.display_box.grid(row=1)  

        # ----------- Register Frame ----------
        self.registers_label.grid(row=0)
        self.register_box.grid(row=1)
        self.sim_output_label.grid(row=2, pady=(10, 0))
        self.sim_output_box.grid(row=3, pady=(10, 0))

        # ------------ Input Frame ------------ might have problems with how this looks here
        self.load_instructions_button.grid(row=0, column=0, padx=(0, 10)) 
        self.save_instructions_button.grid(row=0, column=1, padx=(0, 10))
        self.add_tab_button.grid(row=0, column=2, padx=(0, 15))
        ###### might remove #######\/\/\/\/\/\/\/\/\/
        #self.convert_instructions_button.grid(row=0, column=2, padx=(0, 10))
        self.run_button.grid(row=0, column=3, padx=(0, 25)) 
        self.color_change_button.grid(row=0, column=4, padx=(5, 5))
        self.entry_box.grid(row=0, column=5, padx=(25, 15))
        self.submit_button.grid(row=0, column=6, padx=(0, 15))
        self.input_status_label.grid(row=1, column=5)

        

        # Configure Widgets
        self.entry_box.configure(state='disabled', font=('Roboto', 16))
        self.register_box.configure(state='disabled', font=('Roboto', 14))
        self.sim_output_box.configure(state='disabled', font=('Roboto', 14))
        self.color_change_button.configure(command=self.color_button_callback)
        self.load_instructions_button.configure(command=self.load_instructions_button_callback)
        #self.convert_instructions_button.configure(state='disabled', command=self.convert_button_callback)
        self.save_instructions_button.configure(state='disabled', command=self.save_instructions_button_callback)
        self.run_button.configure(state='disabled', command=self.convert_and_run_callback)
        self.submit_button.configure(state='disabled', command=self.submit_button_callback)

        # Link Main App and GUI
        self.event = threading.Event()
        self.stop_event = threading.Event()
        self.UVSim = Sim(self, self.event, self.stop_event)

    # -------------------------------------- GUI Functions ----------------------------------------

    def add_new_tab(self):
        tab_index = len(self.display_box.tabs()) + 1
        new_tab = ctk.CTkTextbox(self.display_box)
        self.display_box.add(new_tab, text=f'Tab {tab_index}')
        new_tab.configure(state='normal', font=('Roboto', 16))
        new_tab.configure(state='disabled')

        self.textboxes.append(new_tab)
    
    def current_tab(self):
        current_tab_index = self.display_box.index("current")  # Get the index of the current tab
        if 0 <= current_tab_index < len(self.textboxes):  # Check if the index is valid
            return self.textboxes[current_tab_index]  # Return the corresponding textbox
        return None

# Open Theme Selector GUI
    def color_button_callback(self):
        """Open the theme selector for changing color scheme."""
        selector = ThemeSelector(self.root, self.colors, self)

# Load Instructions Into Display and Sim
    def load_instructions_button_callback(self):
        """Load An Instruction File Into Sim.instructions, Display Box, and Update Registers"""
        file = filedialog.askopenfilename()
        if file in ('', None):
            # Check if 'Loaded Instructions' are in the current tab's textbox
            current_textbox = self.current_tab()
            if current_textbox is None or 'Loaded Instructions' not in current_textbox.get(1.0, 'end'):
                self.lock(['run', 'save'])
            return

        self.unlock(['run', 'save', 'convert'])

        # Load instructions from the file
        self.UVSim.load_instructions(file)

        # Use the current textbox to display loaded instructions
        current_textbox = self.current_tab()
        if current_textbox is not None:
            self.write_to_display(self.UVSim.instructions, 'Loaded Instructions')

        # Update the register display
        self.update_register_display(self.UVSim.registers)
    
# Save Button Function
    def save_instructions_button_callback(self):
        """Saves What Is Shown In The Main Display Box To A File And Loads Them Into Sim"""

        # Save 'Instructions'
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text files", "*.txt")], title="Save As")
        current_textbox = self.current_tab()
        if file_path: # Prevent saving if user closes filedialog
            try:
                text = self.current_textbox.get(1.0, 'end')
            except:
                text = self.display_box.get(1.0, 'end')
                

            prepared_text = text.strip()

        # Attempt Save
            try:
                with open(file_path, 'w') as f:
                    f.write(prepared_text)

        # Print Any Errors to Terminal
            except Exception as e:
                print(f'Error While Saving: {e}')
            
        # Load Instructions Into Sim
            self.UVSim.load_instructions(file_path)
            self.write_to_display(self.UVSim.instructions, 'Loaded Instructions')
            self.update_register_display(self.UVSim.registers)

# Convert 4 digit instructions to 6 digit instructions
    def convert_button_callback(self):
        current_textbox = self.current_tab()
        converted_words = []
        if current_textbox is not None:
            instructions = current_textbox.get(1.0, 'end').strip().splitlines()
            instructions = [line for line in instructions if line and not line.startswith('---')]
            for each in instructions:
                if each[0].isdigit():
                    each = f'+{each}'
                if len(each) == 5:
                    i = int(each[1:]) // 100
                    o = int(each[1:]) % 100
                    if i in (10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43):
                        new_word = f'{each[0]}{i:03}{o:03}'
                    else:
                        new_word = f'{each[0]}{each[1:].zfill(6)}'
                    converted_words.append(new_word)
                else:
                    converted_words.append(each)
            self.write_to_display(converted_words, 'Loaded Instructions')
            self.UVSim.load_instructions(converted_words)
            self.update_register_display(self.UVSim.registers)
        else:
            print("No current textbox found.")

# Write To Display Function
    def write_to_display(self, text, input_type):
        """Writes input_type, two new lines, and text To: self.display_box"""
        # Remove Any Existing Text
        self.clear_display()

        # Add Input Type Header
        # self.display_label.configure(text=f'--- {input_type} ---')

        current_textbox = self.current_tab()
        if current_textbox:
            # Add Input Type Header
            current_textbox.configure(state='normal')
            current_textbox.insert('end', f'--- {input_type} ---\n\n')

            # Write To Display
            if isinstance(text, list):
                for line in text:
                    current_textbox.insert('end', f"{line}\n")
            else:
                current_textbox.insert('end', text)

            current_textbox.configure(state='disabled')

# Clear Display Function
    def clear_display(self):
        current_textbox = self.current_tab() 
        if current_textbox:
            current_textbox.configure(state='normal')
            current_textbox.delete(1.0, 'end')
            current_textbox.configure(state='disabled')

# Write To Output
    def write_to_output(self, text):
        """Should Be Used ONLY By Sim to WRITE (opcode 11)"""
        self.sim_output_box.configure(state='normal')
        self.sim_output_box.insert('end', f'>  {text}\n')
        self.sim_output_box.configure(state='disabled')

# Clear Output Box
    def clear_output(self):
        """Should Be Used To Clear Outut At Each Run Call)"""
        self.sim_output_box.configure(state='normal')
        self.sim_output_box.delete(0.0, 'end')
        self.sim_output_box.configure(state='disabled')

# Update Registers
    def update_register_display(self, registers):
        """Accepts Sim's self.registers variable (list) and writes them to register_box"""
        # Remove Current Register List
        self.register_box.configure(state='normal')
        self.register_box.delete(0.0, 'end')

        # Write New Register List
        for i, register in enumerate(registers):
            self.register_box.insert('end', f'Reg {i:02}: {register}\n')
        self.register_box.configure(state='disabled')

    # Process Loaded Instructions
    import threading
# Run Button functionality
    def run_button_callback(self):
        """Calls Sim class .execute_instructions and updates register display, with multiple tab support and 7-digit instruction validation."""
        # Clear Output Box
        self.clear_output()

        # Get the current textbox from the active tab
        current_textbox = self.current_tab()
        if current_textbox is None:
            self.write_to_display("No active tab found.", "Error")
            return

        # Retrieve text from the current textbox
        text = current_textbox.get(1.0, 'end')
        end_of_input_type = text.find('\n\n')
        if end_of_input_type != -1:
            prepared_text = text[end_of_input_type + 2:].strip().splitlines()
        else:
            prepared_text = text.strip().splitlines()

        finished_text = []
        for i, line in enumerate(prepared_text):
            if line[0].isdigit():
                line = f'+{line}'
            if len(line) != 7:
                self.write_to_display(f'Instruction {i}: {line} is invalid', 'Invalid Instructions')
                self.unlock(['default'])
                return
            finished_text.append(line)

        try:
            self.UVSim.load_instructions(finished_text)
        except Exception as e:
            self.write_to_display(f'{e}', 'Instruction Error')
            return

        # Update register display and execute instructions in a separate thread
        self.update_register_display(self.UVSim.registers)
        if not hasattr(self, 'sim_thread') or not self.sim_thread.is_alive():
            self.sim_thread = threading.Thread(target=self.UVSim.execute_instructions)
            self.sim_thread.start()
        else:
            self.write_to_display("Simulation already running.", "Thread Error")

        # Track active tab index and reset accumulator
        self.active_tab_index = current_textbox
        self.UVSim.accumulator = '+0000'  # Reset accumulator to fix bug


# Submit Button
    def submit_button_callback(self):
        # Ensure Submit Only Works on Active Tab
        if self.active_tab_index != self.current_tab():
            self.input_status_label.configure(text="Error: Please Try Again.")
            return

        new_instruction = self.entry_box.get()

        # Validate New Instruction
        ni_signed = True if (new_instruction.startswith('+') or new_instruction.startswith('-')) else False
        if not ni_signed:
            new_instruction = f'+{new_instruction}'
            ni_signed = True

        ni_len = True if len(new_instruction) in (7, 5) else False
        ni_digit = True if new_instruction[1:].isdigit() else False

        if len(new_instruction) == 5:
            i = int(new_instruction[1:]) // 100
            o = int(new_instruction[1:]) % 100
            if i in (10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43):
                new_instruction = f'{new_instruction[0]}{i:03}{o:03}'
            else:
                new_instruction = f'{new_instruction[0]}{new_instruction[1:].zfill(6)}'

        # If New Instruction Is Valid
        if ni_len and ni_signed and ni_digit:
            self.input_status_label.configure(text='')
            self.entry_box.delete(0, 'end')
            self.new_word = new_instruction
            self.event.set()

        else:
            self.input_status_label.configure(text="Instruction Must have 4 (####) or 6 (######) digits")

# Function to call both conver and run for run button
    def convert_and_run_callback(self):
        # Disable the run button during conversion to prevent multiple clicks
        self.run_button.configure(state='disabled')

        # Call the convert_button_callback and then the run_button_callback after a delay
        self.convert_button_callback()
        
        # Use `after` to delay the call to run_button_callback until the conversion is finished
        self.after(100, self.run_button_callback)

        # Re-enable the run button after both functions are done (optional, depending on your needs)
        self.after(200, lambda: self.run_button.configure(state='normal'))

# Waits for user input if a READ operation is performed in SIM
    def wait_for_input(self):
        self.new_word = None

        while self.new_word is None:
            if self.is_closed:
                raise Exception("Window Closed")
            self.root.update()

# Locking And Unlocking Functions
    def unlock(self, target=[]):
        """Works with strings and lists"""
        current_textbox = self.current_tab()  # Get the current tab's textbox
        # if isinstance isn't happy > if type(target) == list:
        if isinstance(target, list):
            for t in target:
                match t:
                    case 'color':
                        self.color_change_button.configure(state='normal')
                    case 'load':
                        self.load_instructions_button.configure(state='normal')
                    case 'save':
                        self.save_instructions_button.configure(state='normal')
                    case 'run':
                        self.run_button.configure(state='normal')
                    case 'submit':
                        self.submit_button.configure(state='normal')
                    case 'entry':
                        self.entry_box.configure(state='normal')
                    # case 'convert':
                    #     self.convert_instructions_button.configure(state='normal')
                    case 'buttons':
                        self.unlock(target=['color', 'load', 'save', 'run'])
                    case 'default':
                        self.unlock(target=['color', 'load', 'display'])
                        self.lock(['submit', 'entry', 'run', 'save', 'convert'])
                    case 'all':
                        self.unlock(target=['color', 'load', 'save', 'convert', 'run', 'submit', 'display', 'entry'])
                    case _:
                        pass

    def lock(self, target=[]):
        """Accepts lists"""
        current_textbox = self.current_tab()  # Get the current tab's textbox
        # if isinstance isn't happy > if type(target) == list:
        if isinstance(target, list):
            for t in target:
                match t:
                    case 'color':
                        self.color_change_button.configure(state='disabled')
                    case 'load':
                        self.load_instructions_button.configure(state='disabled')
                    case 'save':
                        self.save_instructions_button.configure(state='disabled')
                    case 'run':
                        self.run_button.configure(state='disabled')
                    case 'submit':
                        self.submit_button.configure(state='disabled')
                    case 'entry':
                        self.entry_box.configure(state='disabled')
                    # case 'convert':
                    #     self.convert_instructions_button.configure(state='disabled')
                    case 'buttons':
                        self.lock(target=['color', 'load', 'save', 'run', 'convert'])
                    case 'all':
                        self.lock(target=['color', 'load', 'save', 'run', 'convert', 'submit', 'display', 'entry'])
                    case _:
                        pass

# Start GUI
    def start_gui(self):
        """Starts The Main GUI Loop"""
        self.root.mainloop()

# Restart To Apply Color
    def restart(self):
        self.on_close()

        new_app = GUI()
        new_app.start_gui()

# Ensure Program Closes Properly
    def on_close(self):
        self.stop_event.set() # Set Stop Event To Stop Sim
        self.event.set() # Un-Pause .wait() in Sim
        self.is_closed = True
        self.root.destroy()

# If Run As Main
if __name__ == '__main__':
    app = GUI()
    app.start_gui()