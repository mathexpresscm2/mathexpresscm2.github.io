import os, sys, re

def check_path_case_sensitive(path):
    parts = path.split('/')
    current_dir = '.'
    for part in parts:
        if not part: continue
        if not os.path.isdir(current_dir) and not os.path.exists(current_dir):
            return False, f'{current_dir} does not exist'
        try:
            actual_contents = os.listdir(current_dir)
        except Exception as e:
            return False, str(e)
        if part not in actual_contents:
            return False, f'Mismatch at {current_dir}: looking for {part}'
        current_dir = os.path.join(current_dir, part)
    return True, ''

html = open('index.html', encoding='utf-8').read()
links = re.findall(r'href=\"(Meeting/[^\"]+)\"', html)
for url in links:
    ok, err = check_path_case_sensitive(url)
    if not ok:
        print(f'ERROR in index.html: {url} -> {err}'.encode('utf-8'))
print('Done checking index.html')
