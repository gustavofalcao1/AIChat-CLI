import os
import sys
import json
import emoji

# Função para criar arquivos de dados se não existirem
def create_data_files():
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    files = {
        'conversations.json': {},
        'log.json': {},
    }
    
    for filename, content in files.items():
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(content, f)

# Encontre o caminho do arquivo emoji.json
emoji_json_path = os.path.join(os.path.dirname(emoji.__file__), 'unicode_codes', 'emoji.json')

# Inicialize OPTIONS_PYINSTALLER
OPTIONS_PYINSTALLER = [
    '--name=aichat-cli',
    '--onefile'
]

# Adicione arquivos de dados se existirem
data_files = [
    'data/conversations.json',
    'data/log.json',
    'data/config.json'
]

for data_file in data_files:
    if os.path.exists(data_file):
        OPTIONS_PYINSTALLER.append(f'--add-data={data_file}:data')

# Adicione o arquivo emoji.json
if os.path.exists(emoji_json_path):
    OPTIONS_PYINSTALLER.append(f'--add-data={emoji_json_path}:emoji/unicode_codes')

def main():
    create_data_files()
    command = 'pyinstaller ' + ' '.join(OPTIONS_PYINSTALLER) + ' main.py'
    if sys.platform.startswith('win'):
        # Windows
        os.system(command)
    elif sys.platform.startswith('darwin'):
        # macOS
        os.system(command)
    elif sys.platform.startswith('linux'):
        # Linux
        os.system(command)
    else:
        print('Plataforma não suportada.')

if __name__ == '__main__':
    main()