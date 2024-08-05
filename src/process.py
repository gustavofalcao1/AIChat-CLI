import re
import pyperclip
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console
from rich.text import Text

console = Console()

def formatted_code(text):
    """
    Find and format code blocks in the text provided.
    """
    standard_code = r"```(\w*)\n(.*?)```"
    correspondences = re.findall(standard_code, text, re.DOTALL)

    formatted_codes = []

    for i, (language, code) in enumerate(correspondences):
        language = language.strip() or "plaintext"
        
        syntax = Syntax(code, language, theme="dracula")
        panel = Panel(syntax, title=f"{language.title()}")
        
        placeholder = f"[[CODE_{i}]]"
        formatted_codes.append((language, placeholder, panel))

    return formatted_codes

def formatar_markdown(text):
    """
    Converts Markdown text into rich formatting using Rich.
    """
    def format_title(match):
        level = len(match.group(1))
        title = match.group(2).strip()
        styles = {
            1: 'bold magenta',
            2: 'bold cyan',
            3: 'bold yellow',
            4: 'bold white',
            5: 'bold red',
            6: 'bold blue'
        }
        style = styles.get(level, 'bold')
        return f'[{style}]{title}[/{style}]'

    text = re.sub(r'^(#{1,6}) (.+)$', format_title, text, flags=re.MULTILINE)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'[bold]\1[/bold]', text)

    # Italic
    text = re.sub(r'\*(.+?)\*', r'[italic]\1[/italic]', text)
    
    # Inline code
    text = re.sub(r'`(.+?)`', lambda match: f'[code]{match.group(1)}[/code]', text)
    
    # Lists (not sorted and ordained)
    text = re.sub(r'^- (.+)$', lambda match: f'* {match.group(1)}', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\. (.+)$', lambda match: f'• {match.group(1)}', text, flags=re.MULTILINE) 
    
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', lambda match: f'[link={match.group(2)}]{match.group(1)}[/link]', text)
    
    # Images
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', lambda match: f'[image={match.group(2)}]{match.group(1)}[/image]', text)

    return text

def process(text):
    """
    Process the text provided by replacing code blocks with placeholders and displaying the formatted text.
    """
    parts_code = formatted_code(text)

    for language, placeholder, panel in parts_code:
        text = text.replace(f"```{language}\n{panel.renderable.code}```", placeholder)

    parts_text = re.split(r"(\[\[CODE_\d+\]\])", text)

    for part in parts_text:
        match = re.match(r"\[\[CODE_(\d+)\]\]", part)
        if match:
            index = int(match.group(1))
            _, _, panel = parts_code[index]
            console.print(panel)

            action = input("Press 'C' to copy the code to the transfer area, or any other key to continue: ").lower()
            if action == 'c':
                pyperclip.copy(panel.renderable.code)
                print("The code was copied to the transfer area.")
        else:
            text_formatted = formatar_markdown(part.strip())
            console.print(Text.from_markup(text_formatted))

