import requests



def parse_task_with_llm(task_description: str, aip_proxy_token: str):
    """
    Sends the task description to the LLM and returns structured instructions
    in a format that can be executed by the task executor.
    """
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {aip_proxy_token}",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": task_description},
            {"role": "system", "content": """
                You are a task automation assistant. 
                Convert the task description provided into a structured format.
                Output your response as JSON. 
                Each step should contain:
                  - "action": the type of operation (e.g., "install_package", "run_script", "format_file", "sort_data", "count_items", "query_db").
                  - "details": any details or paths relevant to the action (e.g., file paths, sorting criteria, SQL queries, etc.)
                Example:
                [
                  {"action": "run_script", "details": {"script_url": "https://some-url.com/script.py", "arguments": ["email@example.com"]}},
                  {"action": "count_items", "details": {"file": "/data/dates.txt", "item": "Wednesday", "output_file": "/data/wednesday-count.txt"}}
                ]
            """}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception("Failed to communicate with LLM API")

    parsed_response = response.json()
    steps = parsed_response["choices"][0]["message"]["content"]

    try:
        return eval(steps)  # Convert string to Python list of dictionaries
    except Exception as e:
        raise ValueError("Failed to parse LLM response as JSON") from e
