🛠️ Motorola 6800 Assembler with GUI
This project is an assembler simulator for the Motorola 6800 microprocessor. Developed in Python, it not only translates assembly instructions into machine code but also provides a user-friendly graphical interface to visualize memory and register states after compilation.

🎯 Project Purpose
The aim of this project is to understand the logic behind an assembler and to build an interactive system capable of translating Motorola 6800 assembly code into corresponding machine code.

📁 Project Structure
bash
Kopyala
Düzenle
Assembler_mc6800/
├── assembler.py            # Assembler class: parsing, opcode handling, memory and register operations
├── gui.py                  # Tkinter-based graphical user interface
├── opcodes_full.py         # Complete 6800 instruction set and opcode definitions
├── tempCodeRunnerFile.py   # Temporary working file (can be ignored)
├── __pycache__/            # Compiled Python bytecode files (can be ignored)
🖥️ Features
Analyzes assembly code line by line.

Supports label resolution and various addressing modes.

Handles pseudo-instructions such as .ORG, .END, .BYTE, .EQU.

Displays the state of registers (A, B, X, SP) and memory visually.

Lists the resulting machine code.

▶️ Installation and Running
Requirements
Python 3.7+

Tkinter (included with standard Python installation)

To Run the Application
bash
Kopyala
Düzenle
python gui.py
Once the GUI opens, you can enter your assembly code and click the Assemble button. The compiled output, memory content, and register state will be displayed on the screen.

🧠 Notes for Developers
The code follows a two-pass assembler logic: the first pass resolves labels, and the second pass translates opcodes.

opcodes_full.py contains all opcode variations (immediate, direct, extended, indexed).

Future improvements may include step-by-step simulation, breakpoint support, and a debugging interface.
