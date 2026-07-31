import re

with open('generate_slides.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    (r'\in \textbf{Ư}(15)$', r'\in $ <strong>Ư</strong>$(15)$'),
    (r'Mà $\textbf{Ư}(15)', r'Mà <strong>Ư</strong>$(15)'),
    (r'\in \textbf{Ư}(250)$', r'\in $ <strong>Ư</strong>$(250)$'),
    (r'\in \textbf{Ư}(350)$', r'\in $ <strong>Ư</strong>$(350)$'),
    (r'\in \textbf{Ư}\text{C}(250, 350)$', r'\in $ <strong>Ư</strong>C$(250, 350)$'),
    (r'Ta có $\textbf{Ư}(250)', r'Ta có <strong>Ư</strong>$(250)'),
    (r'$\textbf{Ư}(350)', r'<strong>Ư</strong>$(350)'),
    (r'vì $\textbf{Ư}\text{CLN}(n+1; n+2)', r'vì <strong>Ư</strong>CLN$(n+1; n+2)'),
    (r'Gọi $d = \textbf{Ư}\text{CLN}(n+1, n+2)$', r'Gọi $d =$ <strong>Ư</strong>CLN$(n+1, n+2)$'),
    (r'hay $\textbf{Ư}\text{CLN}(n+1, n+2)', r'hay <strong>Ư</strong>CLN$(n+1, n+2)')
]

for old, new in replacements:
    content = content.replace(old, new)

with open('generate_slides.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
