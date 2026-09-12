try:
    import time as tm
    import sys
    import os

    def get_time_with_centiseconds():
        current_time = tm.time()

        time_tuple = tm.localtime(current_time)

        milliseconds = (current_time - int(current_time)) * 1 * 100
        centiseconds = int(milliseconds / 10)

        time_str = "["+tm.strftime("%H:%M:%S", time_tuple)+"]"
        return time_str

    command = input("请输入运行(实时监测 或 临时获取)模式(Mode) : ")

    if command == "实时监测":
        while True:
            print(get_time_with_centiseconds())
            tm.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    elif command == "临时获取":
        print(get_time_with_centiseconds())
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        print("无效指令")
        os.execv(sys.executable, [sys.executable] + sys.argv)

except:
    os.execv(sys.executable, [sys.executable] + sys.argv)