import ollama
import os
import Terminal
import sys
import os
import time as tm
import System32

if sys.platform == 'win32':
    os.system('')

message = 'hello'
current_y = 0
strl = 0

Terminal.output('start [.__worked__.]')

while True:
    Terminal.move(x=0, y=2)
    Terminal.output(' '*strl)
    Terminal.move(x=0, y=2)
    message = Terminal.put(prompt='')
    strl = len(message)
    if message.strip() == 'close':
        Terminal.output('end [.__worked__.]', y=current_y, x=0)
        break
    Terminal.output(f'\'{message}\' [Working...]', end=False, y=current_y, x=0)
    out = []
    for chunk in ollama.chat(model='qwen2:latest', messages=[{'role': 'user', 'content': message}], stream=True):
        out.append(chunk['message']['content'])
        
    with open(r'C:\Users\WalkUp\Desktop\Temp.md', 'w', encoding='utf-8') as f:
        f.write((''.join(out)))
    
    Terminal.output(f'\'{message}\' [.__worked__.]', y=current_y, x=0)
    tm.sleep(1.5)
    os.startfile(r'C:\Users\WalkUp\Desktop\Temp.md')
    tm.sleep(2)
    System32.keys.key('ctrl-s')