AI Code Agent and Script Debugger
Overview

This project provides a tool for debugging and improving Python scripts using AI-powered code analysis and generation. It leverages the Groq API to generate code, analyze code, and learn from feedback.
Features


AI-Powered Code Generation: Generates Python code based on a given prompt.
Code Analysis: Analyzes Python code and provides insights.
Learning: Learns from feedback and saves learned information to a file.
Script Debugging: Debugs Python scripts, executes them, and captures output.
Improved Code Generation: Generates improved code based on errors encountered during script execution.
Static Analysis: Runs static analysis using pylint.
Usage


Set your Groq API key in the config.py file.
Run the script using python main.py.
Enter the path to the script you want to debug when prompted.
The script will be debugged, and improved code will be generated if errors are encountered.
You will be asked if you want to debug the script again. Enter 'y' to continue or 'n' to exit.

Requirements

Python 3.8+
Groq API key
groq library
pylint library
rich library

Installation

Clone the repository: git clone https://github.com/mackimart1/ai-code-agent.git
Install dependencies: pip install -r requirements.txt
Set your Groq API key in config.py

Contributing
Contributions are welcome! Please open an issue or submit a pull request.


License
This project is licensed under the MIT License. See LICENSE for details.
Acknowledgments
Groq API for providing the AI model used in this project.
pylint for providing the static analysis tool used in this project.
rich for providing the library used for formatting terminal output.
