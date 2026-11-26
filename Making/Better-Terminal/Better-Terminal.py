import System32
from termcolor import cprint as print
import sys
import os
import json

path = System32.file.user()

# 基层
def cmd_exit(args): sys.exit(0)
def cmd_print(args): print(' '.join(args))
def occurr_errer(line): print(f'\'{line}\' 不是一个可执行的程序或指令', color='red')
def crash_test(args):
    crash_cfg = {"type": "warning", "title": "Error", "message": "此程序发生灾难性毁灭！", "error code": "NONE"}
    if len(args) >= 1: crash_cfg["type"] = args[0]
    if len(args) >= 2: crash_cfg["title"] = args[1]
    if len(args) >= 3: crash_cfg["message"] = args[2]
    if len(args) >= 4: crash_cfg["error code"] = args[3]
    json_path = System32.file.Self_dir() + "\\crash_info.json"
    with open(json_path, "w", encoding="utf-8") as f: json.dump(crash_cfg, f, ensure_ascii=False, indent=4)
    System32.file.startup(System32.file.Self_dir() + "\\crash.pyw")
    raise Exception("manual crash")
def set_(args):
    try:
        if args[0] == 'studio':
            raw_p = ''.join(args[1])
            fmt_p = os.path.normpath(raw_p)
            if os.path.exists(fmt_p): global path;path = fmt_p;print(f"已切换工作目录到: {fmt_p}")
            else: print(f'\'{fmt_p}\' 不是一个有效的路径', color='red')
    except Exception: print('set '+''.join(args), color='red', end=''); print(" <- 这里出现了问题", color='yellow')
def add(args):
    try:
        if args[0] == 'topic':
            print('Add Topic.')
            # input data
            print('Please input the topic data.')
            topic_platform = input('topic platform : ')
            topic_title = input('topic title : ')
            topic_content = input('topic content : ')
            python_code = input('topic Python codes : ')
            cpp_code = input('topic C++ codes : ')
            test_points = input('test points : ')
            difficulty = input('difficulty : ')
            python_codes_flag = "true"
            cpp_codes_flag = "true"
            
            # formate data
            print('\nformatting data.')
            print('identifying topic platform.')
            if topic_platform == 'lg': topic_platform = 'luogu';topic_studio = r"E:\文件\WalkUp\Practice Question Data\\"+topic_platform+'\\'+topic_title+'\\'
            print('identifying python codes.')
            if python_code == 'none': python_code = ''
            print('identifying C++ codes.')
            if cpp_code == 'none': cpp_code = ''
            print('identifying test_points.')
            if test_points == '': test_points = 10
            print('identifying difficulty.')
            if difficulty == '': difficulty = 'Easy'
            print('identifying python codes flag.')
            if python_code == '': python_codes_flag = "false"
            print('identifying C++ codes flag.')
            if cpp_code == '': cpp_codes_flag = "false"
            print('formatetd data.\n')
            
            # write files
            print('writing data to files.')
            print('identifying topic folder.')
            if not os.path.exists(topic_studio): os.makedirs(topic_studio, exist_ok=True)
            print('writing topic content to file.')
            with open(topic_studio+'topic.md', 'w', encoding='utf-8') as f:f.write(topic_content)
            print('writing python codes to file.')
            with open(topic_studio+'Python.py', 'w', encoding='utf-8') as f:f.write(python_code)
            print('writing C++ codes to file.')
            with open(topic_studio+'C++.cpp', 'w', encoding='utf-8') as f:f.write(cpp_code)
            print('writing states to file.')
            with open(os.path.join(topic_studio, "state.json"), 'w', encoding='utf-8') as f: f.write(f'''{{
    "state": {{
        "Python": {python_codes_flag},
        "C++": {cpp_codes_flag}
    }},
    "AC": {{
        "Python": {test_points},
        "C++": {test_points}
    }},
    "difficulty": {{
        "Python": "{difficulty}",
        "C++": "{difficulty}"
    }}
}}''')
            print('Added topic.')
        else: raise
    except Exception as e: print(f'\'add {''.join(args)}\'不是一个存在的指令。\n错误代码 : {e}')

# commands menu
programs = {
    'exit': cmd_exit,
    'print': cmd_print, 
    'set': set_, 
    'crash': crash_test, 
    'add': add, 
}

blacklist = {
    'hh':lambda:occurr_errer('hh'), 
}

# main loop
while True:
    line = input('Studio : '+path + ' > ')
    # 检查黑名单
    for i in blacklist:
        if line == i: blacklist[i]()
    if not line: continue
    parts = line.split()
    cmd = parts[0]
    args = parts[1:]
    print('')
    # Run Programs
    try:
        func = programs[cmd]
        func(args)
    except KeyError:
        try: System32.file.startup(line)
        except Exception:
            try: System32.file.startup(path + '\\' + line)
            except Exception:occurr_errer(line)
    print('')