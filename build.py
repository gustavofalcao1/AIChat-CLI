import os
import sys

OPTIONS_PYINSTALLER = [
    '--name=aichat-cli',
    '--onefile',
    '--add-data=data/conversations.json;data',
    '--add-data=data/log.json;data',
    '--add-data=data/config.json;data'
]

def main():
    if sys.platform.startswith('win'):
        # Windows
        os.system('pyinstaller ' + ' '.join(OPTIONS_PYINSTALLER))
    elif sys.platform == 'darwin':
        # macOS
        os.system('pyinstaller ' + ' '.join(OPTIONS_PYINSTALLER))
    elif sys.platform.startswith('linux'):
        # Linux
        os.system('pyinstaller ' + ' '.join(OPTIONS_PYINSTALLER))
    else:
        print('Plataforma não suportada.')

if __name__ == '__main__':
    main()
