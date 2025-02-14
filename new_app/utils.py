import json
import requests

def run_llm(task, aip_proxy_token):
    """
    Sends the task to an LLM for processing via the API Proxy.
    """
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {aip_proxy_token}",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": task},
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception("Failed to contact LLM API")
    return response.json()

def extract_dates(input_file, output_file):
    # Function to count Wednesdays in a list of dates from a file and write result to output
    with open(input_file, "r") as f:
        dates = f.readlines()
    wednesdays_count = sum(1 for date in dates if "Wednesday" in date)  # Simplified for example
    with open(output_file, "w") as f:
        f.write(str(wednesdays_count))
    return f"Wednesdays count written to {output_file}"

def sort_contacts(input_file, output_file):
    # Sort contacts in a JSON file
    with open(input_file, "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open(output_file, "w") as f:
        json.dump(sorted_contacts, f, indent=4)
    return f"Contacts sorted and saved to {output_file}"

# Additional utility functions will be written here
