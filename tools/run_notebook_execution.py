import json
import sys
import io
import traceback
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

NB_PATH = Path('notebooks/airline_analysis.ipynb')

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Global execution scope
try:
    from IPython.display import display
except ImportError:
    display = print

scope = {"display": display}
exec_count = 1

print(f'Starting execution of {len(nb["cells"])} cells...')

for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    src = ''.join(cell['source']).strip()
    if not src:
        cell['execution_count'] = None
        cell['outputs'] = []
        continue

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    
    header = src.splitlines()[0][:60]
    print(f'[{exec_count}] Running Cell {idx}: {header} ...')
    
    has_error = False
    err_msg = ''
    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        try:
            exec(src, scope)
        except Exception as e:
            has_error = True
            err_msg = traceback.format_exc()

    cell['execution_count'] = exec_count
    exec_count += 1
    
    outputs = []
    out_text = stdout_buf.getvalue()
    err_text = stderr_buf.getvalue()
    
    if out_text:
        outputs.append({
            'name': 'stdout',
            'output_type': 'stream',
            'text': [line + '\n' for line in out_text.splitlines()]
        })
    if err_text:
        outputs.append({
            'name': 'stderr',
            'output_type': 'stream',
            'text': [line + '\n' for line in err_text.splitlines()]
        })
    if has_error:
        print(f'❌ Error in Cell {idx}:\n{err_msg}')
        outputs.append({
            'ename': 'ExecutionError',
            'evalue': str(err_msg),
            'output_type': 'error',
            'traceback': err_msg.splitlines()
        })
        cell['outputs'] = outputs
        break
    else:
        cell['outputs'] = outputs

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'\nFinished running notebook! {exec_count - 1} code cells executed.')
