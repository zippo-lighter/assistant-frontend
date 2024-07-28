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
    

async def call_assistant_api(file_name: str, file_content: bytes, message: str = "Review this text"):
    try:
        form = aiohttp.FormData()
        form.add_field('file', file_content, filename=file_name, content_type='application/octet-stream')
        form.add_field('message', message)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{BACKEND_HOST}/text-reviewer/{file_name}', data=form) as response:
                data = await response.json()
                return (True, data)
    except Exception as e:
        return (False, e)
    

import re

def extract_reviewed_text(text):
    """
    Extracts the reviewed english text a given text.
    
    Parameters:
    text (str): The input text containing whole OpenAI respoinse.
    
    Returns:
    str: The extracted reviewed text or an empty string if not found.
    """
    # Define the regular expression pattern to match the reviewed text block
    pattern = r'---\n\n(.*?)---\n\n'
    
    # Search for the pattern in the given text using re.DOTALL to match across multiple lines
    match = re.search(pattern, text, re.DOTALL)
    
    # If a match is found, return the reviewed text block
    if match:
        return f"{match.group(1).strip()}"
    
    # If no match is found, return an empty string
    return ""

def extract_corrections(text):
    """
    Extracts the list of corrections of a given text.
    
    Parameters:
    text (str): The input text containing the list of corrections.
    
    Returns:
    str: The extracted list of corrections or an empty string if not found.
    """
    # Define the regular expression pattern to match the list of corrections
    pattern = r'### (?:List of )?Corrections:\n(.*?)\n###'
    
    # Search for the pattern in the given text using re.DOTALL to match across multiple lines
    match = re.search(pattern, text, re.DOTALL)
    
    # If a match is found, return the list of corrections
    if match:
        return f"{match.group(1).strip()}"
    
    # If no match is found, return an empty string
    return ""