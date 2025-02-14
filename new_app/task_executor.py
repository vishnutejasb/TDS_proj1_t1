import subprocess
import json
from utils import  sort_contacts, extract_dates

def extract_email_from_task(task: str) -> str:
    import re
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    match = re.search(email_pattern, task)
    return match.group(0) if match else None


def execute_task_from_llm_response(steps):
    """
    Takes structured steps (from the LLM response) and dynamically executes them.
    """
    execution_result = []

    for step in steps:
        action = step.get("action")
        details = step.get("details", {})

        if action == "run_script":
            script_url = details.get("script_url")
            arguments = details.get("arguments", [])
            result = run_datagen_script(script_url, arguments)
            execution_result.append(result)

        elif action == "install_package":
            package_name = details.get("package_name")
            result = install_package(package_name)
            execution_result.append(result)

        elif action == "format_file":
            file_path = details.get("file_path")
            result = format_file_with_prettier(file_path)
            execution_result.append(result)

        elif action == "sort_data":
            input_file = details.get("input_file")
            output_file = details.get("output_file")
            result = sort_contacts(input_file, output_file)
            execution_result.append(result)

        elif action == "count_items":
            input_file = details.get("file")
            item = details.get("item")
            output_file = details.get("output_file")
            result = extract_dates(input_file, item, output_file)
            execution_result.append(result)

        else:
            raise ValueError(f"Unknown action: {action}")

    return execution_result

def install_package(package_name):
    """
    Installs a package using pip.
    """
    command = f"pip install {package_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to install package: {result.stderr}")
    return f"Package {package_name} installed successfully."
