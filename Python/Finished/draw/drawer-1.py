import sys
import time
import random as r

def main():
    composite_based_code = True
    while composite_based_code:
        time.sleep(0.5)
        
        turtle_available = False
        turtle = None
        
        try:
            print("正在启动turtle库>>>")
            time.sleep(0.5)
            import turtle
            turtle_available = True
            print("turtle库启动成功>>>")
        except ImportError as e:
            print(f"turtle启动失败: {e}>>>")
        
        exec_namespace = {}

        if turtle_available:
            a001 = """
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.title("a001")
t = turtle.Turtle()
t.speed(0)
t.fd(100)
"""
            a002 = """
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("a002")

"""
        else:
            a001 = "print('turtle库不可用>>>')"
            a002 = "print('turtle库不可用>>>')"
        
        time.sleep(0.5)
        
        Launcher = r.randint(1, 2)
        user_input = ""
        
        try:
            if Launcher == 1:
                time.sleep(0.5)
                user_input = input("启动器状态 : 启动成功>>> ")
                if not user_input:
                    time.sleep(0.5)
                    raise ValueError("错误指令>>>")
                
            elif Launcher == 2:
                retry_count = 0
                while retry_count < 4:
                    time.sleep(0.5)
                    print("启动状态 : 启动失败>>>\n正在重新启动>>>")
                    Launcher = r.randint(1, 2)
                    
                    if Launcher == 1:
                        time.sleep(0.5)
                        user_input = input("启动器状态 : 启动成功>>> ")
                        break
                    else:
                        retry_count += 1
                        if retry_count == 4:
                            print("启动状态 : 启动完全失败>>>\n")
                            sys.exit(1)
        except Exception as e:
            time.sleep(0.5)
            print(f"数据处理失败: {e} >>>")
            sys.exit(1)

        time.sleep(0.5)
            
        try:
            if user_input == "启动a001":
                time.sleep(0.5)
                print("启动a001中...>>>")
                time.sleep(0.5)
                
                try:
                    exec_globals = {'turtle': turtle} if turtle_available else {}
                    exec(a001, exec_globals, exec_namespace)
                    
                    if turtle_available:
                        screen = exec_namespace.get('screen')
                        t_obj = exec_namespace.get('t')
                        if screen and t_obj:
                            print("a001启动成功>>>\n")
                            screen.mainloop()
                        else:
                            print("启动失败: screen或t未初始化 >>>\n")
                            sys.exit(1)
                    else:
                        print("启动完成>>>\n")
                        
                except Exception as e:
                    print(f"a001启动失败...>>>\n启动错误: {e} >>>")
                    sys.exit(1)
                    
            elif user_input == "启动a002":
                time.sleep(0.5)
                print("启动a002中...>>>")
                time.sleep(0.5)
                
                try:
                    exec_globals = {'turtle': turtle} if turtle_available else {}
                    exec(a002, exec_globals, exec_namespace)
                    
                    if turtle_available:
                        screen = exec_namespace.get('screen')
                        t_obj = exec_namespace.get('t')
                        if screen and t_obj:
                            print("a002启动成功...>>>\n")
                            screen.mainloop()
                        else:
                            print("启动失败: screen或t未初始化 >>>\n")
                            sys.exit(1)
                    else:
                        print("启动完成>>>\n")
                        
                except Exception as e:
                    print(f"a002启动失败...>>>\n启动错误: {e} >>>\n")
                    sys.exit(1)

            elif user_input.lower() in ("exit", "退出"):
                print("正在退出程序...")
                composite_based_code = False
               
            else:
                print("无效指令，请输入'启动a001'、'启动a002'或'exit'>>>\n")
                
        except Exception as e:
            print(f"程序错误数据: {e} >>>\n")
            sys.exit(1)

if __name__ == "__main__":
    main()
