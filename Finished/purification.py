def purify_code(src_path: str, out_path: str):
    with open(src_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("print('["):
            continue
        out_lines.append(line)
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"[PURIFY/INFO] Purified file saved -> {out_path}")

if __name__ == "__main__":
    src = input("请输入源文件路径：")
    src = src.strip('"')
    purify_code(src, "result.txt")