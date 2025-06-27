from flask import Blueprint, request, jsonify, render_template
import uuid
import os
import json

share_bp = Blueprint('prompts', __name__, template_folder='../templates')

DATA_FILE = 'prompts.json'

# Load or initialize prompts database
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        prompts = json.load(f)
else:
    prompts = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(prompts, f)

@share_bp.route('/share', methods=['POST'])
def share_prompt():
    data = request.json
    prompt_text = data.get('prompt')
    tags = data.get('tags', [])
    version = data.get('version', '1.0')

    prompt_id = uuid.uuid4().hex[:6]
    prompts[prompt_id] = {
        'prompt': prompt_text,
        'tags': tags,
        'version': version,
        'uses': 0
    }

    save_data()
    return jsonify({'url': f'/p/{prompt_id}'})

@share_bp.route('/p/<prompt_id>')
def view_prompt(prompt_id):
    prompt_data = prompts.get(prompt_id)
    if not prompt_data:
        return "Prompt not found", 404

    prompt_data['uses'] += 1
    save_data()
    return render_template('views.html', prompt=prompt_data, id=prompt_id)

@share_bp.route('/api/prompt/<prompt_id>')
def api_prompt(prompt_id):
    prompt_data = prompts.get(prompt_id)
    if not prompt_data:
        return jsonify({'error': 'Not found'}), 404

    prompt_data['uses'] += 1
    save_data()
    return jsonify(prompt_data)



@share_bp.route('/share.html')
def share_html():
    return render_template('share.html')
