# UVSim GUI Machine Interpreter

## A Python-based program with a fully functional GUI for running machine instructions from text files, supporting multi-tab workflows and customizable themes.

**Background**
This project is part of the Software Engineering course at UVU and is designed to simulate real-world software development in a collaborative team setting. It introduces students to the process of iterative development, starting with a basic program and progressively enhancing it to meet more complex requirements.

## Goals
- Develop a tool that emulates a simple machine capable of interpreting and executing instructions.
- Transition from a terminal-based program to a user-friendly GUI application.
- Enable handling of up to 250 signed instructions (4-digit or 6-digit integers).
- Introduce features for working with multiple files simultaneously.

## Accomplishments
- Transformed a terminal-based program into a fully functional GUI application.
- Enhanced the instruction limit from 100 to 250 signed integers (both 4-digit and 6-digit formats).
- Integrated file-loading capabilities, allowing users to load, edit, and save .txt files.
- Added support for multiple tabs, enabling users to work with several files concurrently.
- Designed an intuitive interface that visualizes registers and outputs during execution.



## System Requirements
* You must have Python 3.x installed on your system.
* You must install CustomTkinter for the GUI components. You can install it using pip with the following command:

```bash
pip install customtkinter
```

## Running the Project
**You Will Need a .txt File** | 
Have a text file ready, with instructiosn for the program.
Each line or "word" of the .txt file to be run must meet the required format of a signed, 4 digit integer or signed 6 digit integer. Up to 250 words may be loaded in a single .txt file.


1. Clone the Repository or download to your local machine
2. Navigate to the project directory and run using the following command: "python gui.py"
3. Upon launching, you can load the instructions to be run by selecting 'Load Instructions', which will open your
machines file selector. Select the .txt file you wish to run.
4. After loading the .txt file, you can view and edit the file in the main window.
5. If necessary, select the 'Save Instructions' option to save changes made to the .txt file.
6. Select the 'Run Instructions' button to run the instructions displayed in the main window. Registers on the right
hand side will update to what is displayed in the main window.
7. The user may be prompted to READ another word into memory. This can be entered into the input box located in the
bottom right hand corner as another signed, four or six digit integer. Click the 'Submit' button to submit your input.
8. If there is any output, it will be displayed in the window located under the 'Output' header.
9. Once the instructions have been run, the program will prompt for new instructions.
10. The 'Add Tab' button allows you to open multiple tabs, each capable of displaying the same or different .txt files. 
11. Select a tab, load the desired .txt file, and run instructions independently on each tab.
12. Complete the instructions for each file until you see the message "Instructions Executed: Please Load New Instructions" in the main display.

**Theme Customization**
This project features the ability to add a custom color scheme.
 - Select the 'Change Color Scheme' button to select a different theme.
 - Custom themes may be added to the 'themes' folder as a .json file.

 Note: Themes must be selected before Loading and running instructions.
