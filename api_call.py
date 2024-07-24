import requests
import aiohttp


async def check_backend_connection():
    try:
        async with aiohttp.ClientSession() as session:

            async with session.get('http://127.0.0.1:8000/') as response:
        
                if response.status == 200:
                    data = await response.json()
                    return (True, data)
                else:    
                    return (False, response.status)
                
                # ui.notify(f'API call successful: {data}')
    except requests.exceptions.RequestException as e:
        return (False, e)
        # ui.notify(f'API call failed: {e}', type='negative')

async def call_assistant_api(file_name: str, file_content: bytes):
    try:

        form = aiohttp.FormData()
        form.add_field('file', file_content, filename=file_name, content_type='application/octet-stream')
        # with open(file_name, 'rb') as file:
        #     # Read the file contents
        #     file_data = file.read()
        async with aiohttp.ClientSession() as session:
            #async with session.get('http://127.0.0.1:8000/') as response:
            async with session.post(f'http://127.0.0.1:8000/diagram-file/{file_name}', data=form) as response:

                #response =await requests.post(f'http://127.0.0.1:8000/diagram-file/{file_name}')
                data = await response.json()
                return (True, data)
    except Exception as e:
        return (False, e)