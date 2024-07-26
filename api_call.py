import aiohttp
from aiohttp import ClientConnectorError

BACKEND_HOST = "YOUR_BACKEND_HOST"  # Replace with your Backend host server

if BACKEND_HOST == "YOUR_BACKEND_HOST":
    raise ValueError("Please set your backend endpoint at the openai_lib.py file")

async def check_backend_connection():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{BACKEND_HOST}/') as response:
                if response.status == 200:
                    data = await response.json()
                    return (True, data)
                else:    
                    return (False, response.status)
    
    except ClientConnectorError as e:
        return (False, f"Connection failed: {e}")
            
    except Exception as e:
        return (False, f"An error occurred: {e}")
    

async def call_assistant_api(file_name: str, file_content: bytes):
    try:
        form = aiohttp.FormData()
        form.add_field('file', file_content, filename=file_name, content_type='application/octet-stream')
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{BACKEND_HOST}/diagram-file/{file_name}', data=form) as response:
                data = await response.json()
                return (True, data)
    except Exception as e:
        return (False, e)
    

import re

def extract_mermaid_code(text):
    """
    Extracts the Mermaid code block from a given text.
    
    Parameters:
    text (str): The input text containing the Mermaid code block.
    
    Returns:
    str: The extracted Mermaid code block or an empty string if not found.
    """
    # Define the regular expression pattern to match the Mermaid code block
    pattern = r'```mermaid\n(.*?)\n```'
    
    # Search for the pattern in the given text using re.DOTALL to match across multiple lines
    match = re.search(pattern, text, re.DOTALL)
    
    # If a match is found, return the Mermaid code block
    if match:
        return f"{match.group(1).strip()}"
    
    # If no match is found, return an empty string
    return ""