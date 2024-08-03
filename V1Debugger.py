import sys
import traceback
import os
from datetime import datetime
import logging
from io import StringIO
from typing import List, Dict, Any, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.table import Table
from rich.logging import RichHandler
from groq import Groq
import pylint.lint
from pylint.reporters.text import TextReporter
import json
import config

# Set up logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")
console = Console()

class AICodeAgent:
    def __init__(self):
        self.learned_info: Dict[str, List[Dict[str, Any]]] = {}
        self.groq_client = Groq(api_key=config.GROQ_API_KEY)

    def generate_task_specific_code(self, prompt: str) -> str:
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in generating Python code."},
                    {"role": "user", "content": f"Generate Python code for the following task:\n{prompt}"}
                ],
                model="mixtral-8x7b-32768",
                max_tokens=1000,
            )
            generated_code = response.choices[0].message.content
            return generated_code
        except Exception as e:
            console.print(f"[bold red]Error generating code: {str(e)}[/bold red]")
            return f"# Error occurred while generating code\n# {str(e)}"

    def learn(self, code: str, feedback: str, context: str) -> None:
        if context not in self.learned_info:
            self.learned_info[context] = []
        
        self.learned_info[context].append({
            "code": code,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        })

    def analyze_generated_code(self, code: str) -> Dict[str, Any]:
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in analyzing Python code."},
                    {"role": "user", "content": f"Analyze the following Python code and provide insights:\n\n{code}"}
                ],
                model="mixtral-8x7b-32768",
                max_tokens=1000,
            )
            analysis = response.choices[0].message.content
            return {
                "code": code,
                "analysis": analysis
            }
        except Exception as e:
            console.print(f"[bold red]Error analyzing code: {str(e)}[/bold red]")
            return {
                "code": code,
                "analysis": f"Error occurred while analyzing code: {str(e)}"
            }

    def display_learned_info(self) -> None:
        console.print(Panel("Learned Information:", style="bold cyan"))
        for context, info_list in self.learned_info.items():
            console.print(f"[bold]Context: {context}[/bold]")
            for item in info_list:
                console.print(f"Timestamp: {item['timestamp']}")
                console.print(f"Feedback: {item['feedback']}")
                console.print(Syntax(item['code'], "python", theme="monokai", line_numbers=True))
                console.print("---")

    def save_learned_info(self, filename: str = "learned_info.json") -> None:
        try:
            with open(filename, 'w') as f:
                json.dump(self.learned_info, f, indent=2)
            console.print(f"[green]Learned information saved to {filename}[/green]")
        except IOError as e:
            console.print(f"[bold red]IOError while saving learned information: {str(e)}[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error saving learned information: {str(e)}[/bold red]")

    def load_learned_info(self, filename: str = "learned_info.json") -> None:
        try:
            with open(filename, 'r') as f:
                self.learned_info = json.load(f)
            console.print(f"[green]Learned information loaded from {filename}[/green]")
        except FileNotFoundError:
            console.print(f"[yellow]No saved information found at {filename}[/yellow]")
        except json.JSONDecodeError as e:
            console.print(f"[bold red]Error decoding JSON from {filename}: {str(e)}[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error loading learned information: {str(e)}[/bold red]")

    def clear_learned_info(self) -> None:
        self.learned_info.clear()
        console.print("[green]Learned information cleared[/green]")

class ScriptDebugger:
    def __init__(self, script_path: str):
        self.script_path = os.path.abspath(script_path)
        try:
            self.groq_client = Groq(api_key=config.GROQ_API_KEY)
            self.ai_agent = AICodeAgent()
        except Exception as e:
            log.error(f"Error initializing Groq client or AICodeAgent: {str(e)}")
            raise

    def debug_and_improve(self) -> None:
        console.print(Panel(f"Debugging script: {self.script_path}", style="bold green"))
        
        # Read the script content
        with open(self.script_path, 'r') as file:
            script_content = file.read()
        
        # Run static analysis
        self.run_static_analysis(script_content)
        
        # Execute the script and capture output
        output, error = self.execute_script(script_content)
        
        if error:
            console.print(Panel("Error occurred during execution:", style="bold red"))
            console.print(error)
            
            # Generate improved code using AI
            improved_code = self.generate_improved_code(script_content, error)
            
            # Display the improved code
            console.print(Panel("Improved Code:", style="bold green"))
            console.print(Syntax(improved_code, "python", theme="monokai", line_numbers=True))
            
            # Prompt user for feedback
            feedback = Prompt.ask("Provide feedback on the improved code")
            
            # Learn from the feedback
            self.ai_agent.learn(improved_code, feedback, "error_correction")
            
            # Update the file with the improved code
            self.update_script_file(improved_code)
        else:
            console.print(Panel("Script executed successfully!", style="bold green"))
            console.print(output)
        
        # Display learned information
        self.ai_agent.display_learned_info()
        
        # Save learned information
        self.ai_agent.save_learned_info()

    def run_static_analysis(self, script_content: str) -> None:
        console.print(Panel("Running static analysis...", style="bold blue"))
        
        # Use pylint for static analysis
        pylint_output = StringIO()
        reporter = TextReporter(pylint_output)
        pylint.lint.Run([self.script_path], reporter=reporter, exit=False)
        
        # Display pylint results
        console.print(pylint_output.getvalue())

    def execute_script(self, script_content: str) -> Tuple[str, Optional[str]]:
        console.print(Panel("Executing script...", style="bold blue"))
        
        # Capture stdout and stderr
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = StringIO(), StringIO()
        
        try:
            # Execute the script
            exec(script_content, globals())
            output = sys.stdout.getvalue()
            error = None
        except Exception as e:
            output = sys.stdout.getvalue()
            error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        finally:
            # Restore stdout and stderr
            sys.stdout, sys.stderr = old_stdout, old_stderr
        
        return output, error

    def generate_improved_code(self, original_code: str, error: str) -> str:
        console.print(Panel("Generating improved code...", style="bold blue"))
        
        prompt = f"""
        Given the following Python script and the error it produced, please provide an improved version of the code that fixes the error:

        Original Code:
        ```python
        {original_code}
        ```

        Error:
        {error}

        Please provide the improved code that fixes this error.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant specialized in Python programming and debugging."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                max_tokens=1000,
            )
            
            improved_code = response.choices[0].message.content
            return improved_code
        except Exception as e:
            log.error(f"Error generating improved code: {str(e)}")
            return "# Error occurred while generating improved code"

    def update_script_file(self, improved_code: str) -> None:
        try:
            with open(self.script_path, 'w') as file:
                file.write(improved_code)
            console.print(f"[green]Script file updated with improved code: {self.script_path}[/green]")
        except IOError as e:
            console.print(f"[bold red]IOError while updating script file: {str(e)}[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error updating script file: {str(e)}[/bold red]")

def debug_script(script_path: str) -> None:
    debugger = ScriptDebugger(script_path)
    while True:
        debugger.debug_and_improve()
        if not Prompt.ask("Do you want to debug this script again?", choices=["y", "n"]).lower() == "y":
            break

if __name__ == "__main__":
    script_path = Prompt.ask("Enter the path to the script you want to debug", default=os.path.join(os.getcwd(), "script_to_debug.py"))
    
    script_path = os.path.abspath(script_path)
    
    if not os.path.exists(script_path):
        log.error(f"The script file '{script_path}' does not exist.")
    elif not config.GROQ_API_KEY:
        log.error("Groq API key is not set in the config file.")
    else:
        debug_script(script_path)