#======= extractor.py =========

import os

# 기준 디렉토리
base_dir = "src"

# 결과 저장용 문자열
output = ""

# 파일 확장자 필터
valid_extensions = (".py", ".yaml", ".yml")

# 디렉토리 순회하며 파일 수집
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(valid_extensions):
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, base_dir)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            output += f"======= {relative_path} =========\n\n{content}\n\n====================\n\n"

# 결과 출력 또는 파일 저장
#print(output)  # 또는 파일로 저장하고 싶다면 아래 코드 사용
with open("formatted_output.txt", "w", encoding="utf-8") as f:
    f.write(output)

