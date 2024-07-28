import asyncio
import json
from nicegui import ui, events, Tailwind
from api_call import check_backend_connection, call_assistant_api, extract_reviewed_text, extract_corrections
from style import  *

uploaded_file_name = None
file_content = None
latest_code = ''

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
    (success, result) = await call_assistant_api(uploaded_file_name, file_content)
    if success:
        # ui.notify(f'API call successful!')
        generate_button.set_text('Response bellow')
        indented_result = json.dumps(result, indent=4)
        json_output.set_value(value=indented_result)
        diagram_extracted_code = extract_mermaid_code(result[0]['content'][0]['text']['value'])
        extracted_code.set_value(diagram_extracted_code)
        diagram.content=diagram_extracted_code
        json_output.update()
        extracted_code.update()
        diagram.update()
        panels.visible = True
        tabs.visible = True

    else:
        ui.notify(f'API call failed: {result}', type='negative')

def on_code_change(event):
    global latest_code
    try:
        latest_code = event.value
        if diagram.visible:
            diagram.content = latest_code
            diagram.update()
    except Exception as e:
        print(f"Error updating diagram: {e}")

def on_tab_change(event):
    global latest_code
    if event.name == 'show' and event.args[0] == 'diagram':
        try:
            diagram.content = latest_code
            diagram.update()
        except Exception as e:
            print(f"Error updating diagram: {e}")


dark = ui.dark_mode()
dark.enable()

with ui.column().classes('w-full  items-center '):
    with ui.row().classes('flex '):
        ui.label('Code 2 Diagram').classes('text-2xl')
    # with ui.row():
    #     ui.codemirror(language='JSON', theme='darcula').classes('h-96 w-full').set_value(contentDemo)
    with ui.row():    
        with ui.chip('Backend connection ', icon='question', on_click=check_connection).classes('bg-teal hover:bg-green text-white font-bold py-2 px-4 rounded'):
            ui.tooltip('Click to check your connection to FastAPI').classes('bg-teal-900')
            badge = ui.badge('?', color='teal-900').classes('text-white ml-2')
    ui.upload(on_upload=handle_upload).classes('custom-upload  text-white font-bold py-2 px-4 rounded') 
    with ui.row():    
        generate_button = ui.button('Generate Diagram!', 
            on_click=lambda: asyncio.create_task(handle_button_click())).classes('bg-teal hover:bg-green text-white font-bold py-2 px-4 rounded')
        generate_button.disable()
    with ui.tabs().classes('w-full') as tabs:
        code_editor = ui.tab('Raw response')
        extracted_code = ui.tab('Diagram code')
        diagram = ui.tab('Diagram')
        tabs.visible = False
    with ui.tab_panels(tabs, value=diagram).classes('w-full') as panels:
        panels.on('show', on_tab_change)
        with ui.tab_panel(code_editor):
            json_output = ui.codemirror(language='JSON', theme='darcula').classes('h-96 w-full')
        with ui.tab_panel(extracted_code):
            extracted_code = ui.codemirror(language='JSON', theme='darcula').classes('h-96 w-full').on_value_change(on_code_change)
        with ui.tab_panel(diagram).classes('items-center'):
            diagram = ui.mermaid(content='').on('error', lambda e: print(e.args['message'])).classes('h-96 w-full')
            
            # ui.label('File upload')
        panels.visible = False


ui.run()
