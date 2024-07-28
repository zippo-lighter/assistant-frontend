import asyncio
import json
from nicegui import ui, events, Tailwind
from api_call import check_backend_connection, call_assistant_api, extract_reviewed_text, extract_corrections
from style import  *

uploaded_file_name = None
file_content = None

def restart():
    global uploaded_file_name, file_content
    file_content = None
    uploaded_file_name = None
    generate_button.set_text('Review Text File!')
    generate_button.disable()
    source_row.visible = False
    show_source_row.visible = False 
    results_row.visible = False
    restart_button.visible = False 
    # ui.navigate.reload()

async def check_connection():
    (success, result) = await check_backend_connection()
    if success:
        ui.notify(f'API call successful: {result}')
        badge.text = '✅'
    else:
        ui.notify(f'API call failed: {result}', type='negative')
        badge.text = '🟥'

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
    generate_button.set_text('Loading...')
    generate_button.disable()
    restart_button.visible = True
    (success, result) = await call_assistant_api(uploaded_file_name, file_content)
    if success:
        generate_button.set_text('Response bellow')
        reviewed_text.set_value(extract_reviewed_text(result[0]['content'][0]['text']['value']))
        list_corrections.set_value(extract_corrections(result[0]['content'][0]['text']['value']))
        source_text.set_value(result[0]['content'][0]['text']['value'])
        reviewed_text.update()
        list_corrections.update()
        source_text.update()
        show_source_row.visible = True
        results_row.visible = True

    else:
        ui.notify(f'API call failed: {result}', type='negative')

def show_source():
    source_row.visible = not source_row.visible
    
dark = ui.dark_mode()
dark.enable()

with ui.column().classes('w-full  items-center '):
    with ui.row().classes('flex '):
        ui.label('Word reviewer').classes('text-2xl')
    with ui.row():    
        with ui.chip('Backend connection ', icon='question', on_click=check_connection).classes('bg-indigo hover:bg-green text-white font-bold py-2 px-4 rounded'):
            ui.tooltip('Click to check your connection to FastAPI').classes('bg-indigo-900')
            badge = ui.badge('?', color='indigo-900').classes('text-white ml-2')
    ui.upload(on_upload=handle_upload).classes('custom-upload  text-white font-bold py-2 px-4 rounded') 
    with ui.row():    
        restart_button = ui.button('Restart', on_click=restart).classes('bg-pink-9 hover:bg-green text-white font-bold py-2 px-4 rounded')
        restart_button.visible = False 
        generate_button = ui.button('Review Text File!', 
            on_click=lambda: asyncio.create_task(handle_button_click())).classes('bg-indigo hover:bg-green text-white font-bold py-2 px-4 rounded')
        generate_button.disable()
    with ui.row().classes('w-full flex-wrap justify-evenly') as results_row:
        with ui.column().classes('w-full col-12 col-md-5  items-center '):
            ui.label('Reviewed Text').classes('text-xl')
            reviewed_text = ui.codemirror(theme='darcula', line_wrapping=True).classes('h-96 w-full')
        with ui.column().classes('w-full col-12 col-md-5  items-center '):
            ui.label('List of Corrections').classes('text-xl')
            list_corrections = ui.codemirror(theme='darcula', line_wrapping=True).classes('h-96 w-full')
        results_row.visible = False
    with ui.row() as show_source_row:
        show_source_button = ui.button('Show OpenAI Assistant response', on_click=show_source).classes('bg-indigo hover:bg-green text-white font-bold py-2 px-4 rounded')
        show_source_row.visible = False 
    with ui.row().classes('w-full no-wrap justify-evenly') as source_row:
        with ui.column().classes('w-full  items-center '):
            source_text = ui.codemirror(theme='darcula', line_wrapping=True).classes('h-96 w-full')
        source_row.visible = False


ui.run()
