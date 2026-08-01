import os
import re

def check_html_links():
    errors = []
    for root, dirs, files in os.walk('Meeting'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    content = open(path, 'r', encoding='utf-8').read()
                except Exception:
                    continue
                
                # Check for src or href attributes
                links = re.findall(r'(?:src|href)=[\"\'\\](.*?)[\"\'\\]', content)
                for link in links:
                    if link.startswith('http') or link.startswith('#') or link.startswith('data:') or link == '':
                        continue
                    # resolve path relative to html file
                    target_path = os.path.normpath(os.path.join(root, link))
                    
                    # check case sensitivity
                    parts = target_path.split(os.sep)
                    current_dir = '.'
                    for part in parts:
                        if part == '.': continue
                        if part == '..': current_dir = os.path.dirname(current_dir); continue
                        
                        try:
                            actual_contents = os.listdir(current_dir if current_dir != '.' else '.')
                        except Exception:
                            break
                        if part.lower() in [f.lower() for f in actual_contents]:
                            if part not in actual_contents:
                                errors.append(f'{path}: Link points to {link} but actual case is different (mismatch at {part})')
                                break
                        else:
                            # Not found at all (could be external or missing, skip)
                            break
                        current_dir = os.path.join(current_dir, part)
    for e in errors:
        print(e.encode('utf-8'))
check_html_links()
