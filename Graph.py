import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import sympy as sp

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("수식 그래프 그리기")

# 전역 폰트 설정
font = ("Arial", 16)

# 라벨 한 개만 생성하여 텍스트를 업데이트할 수 있도록 수정
ex = tk.Label(root, text="", font=font)

def plot_graph():
    # 유저 인풋
    user_input = entry.get()
    input_text = user_input
    # 입력값이 비어있을 경우 처리
    if user_input.strip() == "":
        ex.config(text="입력된 값이 없습니다.")
        return
    
    print(f"입력된 수식: {user_input}")
    
    # 수식에서 'y ='를 제거하고 'x'로 변수 변경, 그리고 ^를 **로 변환
    user_input = user_input.replace("y =", "").replace("^", "**")
    
    # 숫자와 변수(x) 사이에 곱셈 연산자 '*'를 추가
    user_input = re.sub(r'(\d)(x)', r'\1 * x', user_input)  # 숫자와 'x' 사이에 곱셈 연산자를 추가
    print(f"변경된 수식: {user_input}")

    # sympy에서 사용할 변수 정의
    x = sp.symbols('x')

    try:
        # 수식 파싱 (x를 변수로 인식하도록 수정)
        y = sp.sympify(user_input, locals={'x': x})
    except sp.SympifyError:
        print("잘못된 수식입니다.")
        ex.config(text="잘못된 수식입니다.")
        return
    
    # x 값 범위 설정 (동적 범위 설정)
    x_vals = np.arange(-2.0, 2.0, 0.01)  # 기본적으로 범위는 -3에서 3까지

    # y 값 계산 (각 x 값에 대해 y 값을 계산)
    try:
        y_vals = np.array([float(y.subs(x, val)) for val in x_vals])
    except Exception as e:
        print(f"y 값 계산 오류: {e}")
        ex.config(text="y 값 계산 오류")
        return
    
    # y 값의 최대/최소 값 계산
    if len(y_vals) == 0:  # 만약 y_vals가 비어있다면
        ex.config(text="y 값이 계산되지 않았습니다.")
        return
    
    y_min, y_max = np.min(y_vals), np.max(y_vals)
    
    # y축 범위 설정 (여백을 두어 범위가 화면에 맞게 조정되도록)
    y_margin = 0.15 * (y_max - y_min)
    ax_y_min = y_min - y_margin
    ax_y_max = y_max + y_margin
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x_vals, y_vals, label=f"{input_text}", color="blue")
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title(f"{input_text}", fontsize=14)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True)

    # y축 범위 설정
    ax.set_ylim(ax_y_min, ax_y_max)

    # 기존 그래프 제거 후 새 그래프 삽입
    for widget in graph_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# 값받기
def validate_input(new_value):
    # 정규 표현식을 이용하여 'y = 2x^2 + x'와 같은 수식을 허용
    pattern = r"^[0-9\+\-\*\/\^x\^y\s=]*$"  # 숫자, 연산자(+,-,*,/), ^, x, 공백, =만 허용
    if re.match(pattern, new_value):
        return True
    return False

vcmd = root.register(validate_input)  # 검증 함수 등록

# 그래프 프레임
graph_frame = tk.Frame(root)
graph_frame.pack(pady=10)

# 버튼 프레임
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# 그래프 그리기 버튼 (입력값 출력 후 그래프 그리기)
btn_plot = tk.Button(button_frame, text="그래프 그리기", 
                     command=lambda: plot_graph(), font=("Arial", 16))
btn_plot.pack(side="left", padx=10)

# 그래프 값 정의
Label_graph = tk.Label(root, text="그래프 값 입력 (예:y = 2x^2 + x)", font=font)
Label_graph.pack(pady=20)

# Entry 위젯 생성
entry = tk.Entry(root, width=15, font=font, validate="key", validatecommand=(vcmd, "%P"))
entry.pack(pady=5)

# 종료 버튼
btn_exit = tk.Button(button_frame, text="종료", command=root.destroy, font=font)
btn_exit.pack(side="left", padx=10)

# 오류 라벨
ex.pack(pady=(5, 20))

# 메인 루프 실행
root.mainloop()
