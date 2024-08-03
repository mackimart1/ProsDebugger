AI Code Agent and Script Debugger
This project provides a tool for debugging and improving Python scripts using AI-powered code analysis and generation. It consists of two main components:
AICodeAgent: A class that uses the Groq API to generate code, analyze code, and learn from feedback.
ScriptDebugger: A class that uses the AICodeAgent to debug and improve Python scripts.
Features
Code Generation: Generates Python code based on a given prompt.
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
Note
This project is for educational purposes only.
The AI model used is a general-purpose model and may not always generate perfect code.
The script debugging feature is limited to executing scripts and capturing output. It does not support interactive debugging.
