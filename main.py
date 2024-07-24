import asyncio
from nicegui import ui, events, Tailwind
from api_call import check_backend_connection, call_assistant_api
from style import  *

uploaded_file_name = None
file_content = None

async def check_connection():
    (success, result) = await check_backend_connection()
    if success:
        ui.notify(f'API call successful: {result}')
        badge.text = '✅'
    else:
        ui.notify(f'API call failed: {result}', type='negative')

def handle_upload(event: events.UploadEventArguments):
    global uploaded_file_name, file_content
    if event is None:
        return
    uploaded_file_name = event.name
    file_content = event.content.read()
    
    generate_button.enable()

async def handle_button_click():
    global uploaded_file_name, file_content
    if uploaded_file_name is None:
        ui.notify('Please upload a file first', type='negative')
        return
    (success, result) = await call_assistant_api(uploaded_file_name, file_content)
    if success:
        ui.notify(f'API call successful: {result}')
    else:
        ui.notify(f'API call failed: {result}', type='negative')


dark = ui.dark_mode()
dark.enable()
with ui.column().classes('w-full  items-center '):
    with ui.row().classes('flex '):
        ui.label('Upload a file').classes('text-2xl')
    with ui.row():    
        with ui.chip('Backend connection ', icon='question', on_click=check_connection).classes('bg-teal hover:bg-green text-white font-bold py-2 px-4 rounded'):
            ui.tooltip('Click to check your connection to FastAPI').classes('bg-teal-900')
            badge = ui.badge('?', color='teal-900').classes('text-white ml-2')
    with ui.tabs().classes('w-full') as tabs:
        file_upload = ui.tab('Upload file')
        code_editor = ui.tab('Code editor')
    with ui.tab_panels(tabs, value=file_upload).classes('w-full'):
        with ui.tab_panel(file_upload).classes('items-center'):
            ui.upload(on_upload=handle_upload).classes('custom-upload  text-white font-bold py-2 px-4 rounded')
            # ui.label('File upload')
        with ui.tab_panel(code_editor):
            editor = ui.codemirror('# paste your code here', language='Python',theme='darcula').classes('h-32 min-w-64 w-164')
            #ui.label('Code editor')
   
           
    with ui.row():    
        generate_button = ui.button('Generate Diagram!', 
            on_click=lambda: asyncio.create_task(call_assistant_api(file_name=uploaded_file_name, file_content=file_content))).classes('bg-teal hover:bg-green text-white font-bold py-2 px-4 rounded')
        generate_button.disable()

ui.run()
