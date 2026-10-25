import ollama
import re
import System32
from PIL import Image
import ctypes

DPI_SCALE = 1.25

user32 = ctypes.windll.user32
screen_phys_w = user32.GetSystemMetrics(0)
screen_phys_h = user32.GetSystemMetrics(1)
screen_logic_w = int(screen_phys_w / DPI_SCALE)
screen_logic_h = int(screen_phys_h / DPI_SCALE)

print(f"[SCREEN_INFO] 屏幕物理分辨率 W={screen_phys_w}, H={screen_phys_h}")
print(f"[SCREEN_INFO] 屏幕逻辑分辨率 W={screen_logic_w}, H={screen_logic_h}")
print(f"[DPI_INFO] 设定倍率={DPI_SCALE}")

def vl_ask_and_parse(image_path: str, prompt: str, model_name: str = "qwen2.5vl:7b", x_supplement=0, y_supplement=0, retry=3):
    print("[LOG] 开始调用ollama视觉识别")
    im = Image.open(image_path)
    img_w, img_h = im.size
    mid_line = img_w / 2
    print(f"[DEBUG] 图片宽度={img_w}, 中线位置={mid_line}")
    for attempt in range(retry):
        print(f"[LOG] 第 {attempt+1}/{retry} 次尝试识别")
        try:
            resp = ollama.chat(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_path]
                    }
                ],
                options={"temperature": 0.0},
                keep_alive=0
            )
            raw_text = resp["message"]["content"]
            print(f"[LOG] 模型原始输出: {raw_text}")
        except Exception as err:
            print(f"[VL_ERROR] ollama调用异常: {err}")
            continue
        pat = re.search(r"\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]", raw_text)
        if not pat:
            print("[PARSE_LOG] 正则没有匹配到包围盒！")
            continue
        x1 = float(pat.group(1))
        y1 = float(pat.group(2))
        x2 = float(pat.group(3))
        y2 = float(pat.group(4))
        if x1 <= 1.0 and y1 <= 1.0 and x2 <= 1.0 and x2 <= 1.0:
            mode = "0~1归一"
            px1 = x1 * img_w
            py1 = y1 * img_h
            px2 = x2 * img_w
            py2 = y2 * img_h
        else:
            mode = "原生像素"
            px1 = x1
            py1 = y1
            px2 = x2
            py2 = y2
        center_x_phys = ((px1 + px2) / 2 + x_supplement)
        center_y_phys = (py1 + py2) / 2 + y_supplement

        # 保留你的校正规则！
        if center_x_phys < mid_line:
            center_x_logic = center_x_phys * 0.75
            print(f"[CORRECT] X在左半区，系数0.75")
        else:
            center_x_logic = center_x_phys * 1.25
            print(f"[CORRECT] X在右半区，系数1.25")
        center_y_logic = center_y_phys

        print(f"[PARSE_LOG] ✅ 识别通过，无范围限制")
        return center_x_phys, center_y_phys, center_x_logic, center_y_logic, px1, py1, px2, py2, x1, y1, x2, y2, mode, mid_line
    print(f"[PARSE_LOG] {retry}次重试全部失败，无有效结果")
    return None, None, None, None, None, None, None, None, None, None, None, None, None, None

# ============ 最大化按钮识别 ============
if __name__ == "__main__":
    img_file = r"e:\Temp\10.23 19-16.png"
    question = """Find the maximize button of this window.
Only output bounding box as [x1,y1,x2,y2], pixel coordinates for this screenshot.
Do NOT output any explanation, description, extra words.
Ignore minimize, close X button and other irrelevant elements."""
    cx_phys, cy_phys, cx_logic, cy_logic, px1, py1, px2, py2, rx1, ry1, rx2, ry2, mode, mid = vl_ask_and_parse(
        img_file,
        question,
        x_supplement=0,
        y_supplement=0,
        retry=3
    )
    if cx_phys is not None:
        print(f"图片中线: {mid:.2f}")
        print(f"识别模式：{mode}")
        print(f"原始值: x1={rx1}, y1={ry1}, x2={rx2}, y2={ry2}")
        print(f"转像素框: px1={px1:.2f}, py1={py1:.2f}, px2={px2:.2f}, py2={py2:.2f}")
        print(f"【物理像素中心点】 x={cx_phys:.2f}, y={cy_phys:.2f}")
        print(f"【换算后坐标】 x={cx_logic:.2f}, y={cy_logic:.2f}")

        cx_logic = max(0.0, min(cx_logic, screen_phys_w - 1))
        cy_logic = max(0.0, min(cy_logic, screen_phys_h - 1))
        print(f"【最终传入鼠标API整数坐标】 x={int(cx_logic)}, y={int(cy_logic)}")
        System32.mouse.move(int(cx_logic), int(cy_logic))
    else:
        print("多次识别都没有拿到合法按钮框")
