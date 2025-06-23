# Math Function Plotter
2024131043 홍안지

(1) 프로젝트 설명:
사용자가 직접 수학 함수를 입력하면 그에 해당하는 함수와 도함수를 그래프로 시각화하여 출력해주는 파이썬 프로그램입니다. 
수업시간에 집중적으로 배운 class 개념을 이용하여 객체지향 프로그래밍(OOP)을 바탕으로 해당 프로그램을 구성하였습니다.
함수의 수치계산에 있어 numpy 모듈을, 함수의 시각화에 있어 matplotlib 모듈을 사용하였습니다.


(2) 주요기능:
-사용자로부터 직접 수학 함수를 입력 받기 (예: 'sin(x) + x**2')
-잘못된 수식을 입력하였을 경우 오류 안내 및 재입력 요청
-입력 받은 함수의 도함수를 계산
-입력 받은 함수와 도함수를 한꺼번에 그래프로 시각화하여 출력

예) 'sin(x) + x**2'를 입력하면 'sin(x) + x**2'와 그 도함수('cos(x) + 2*x')의 그래프를 출력

-함수 1개뿐만 아니라 함수 여러개와 각각의 도함수도 한꺼번에 출력하여 하나의 화면에 나타낼 수 있습니다.


(3) 실행 방법:
1. 저장소를 클론하거나 파일을 다운로드한다.
2. 필요한 패키지를 설치한다:
	pip install -r requirements.txt
3. 프로그램을 실행한다:
	python plotter.py
4. 아래와 같은 순서로 입력(input)을 진행한다.
 - 함수 개수 입력
 - 각 함수 수식 입력 (`x**2`, `sin(x) + cos(x)` 등)
 - x축 범위 입력
 - 도함수 출력 여부 선택
 *입력 예시:
	몇 개의 함수를 입력하시겠습니까? 2
	1번째 함수 수식을 입력하세요: sin(x)*exp(-x)
	2번째 함수 수식을 입력하세요: 2
	x축 최소값을 입력하세요: 0
	x축 최대값을 입력하세요: 10
	도함수도 함께 그릴까요? (y/n): y
5.출력을 확인한다.
-입력한 함수와 그 도함수가 사용자가 입력한 x값의 범위에 따라 그래프로 출력된다.
-입력함수는 실선으로, 도함수는 점선으로 표현된다.
*출력 예시:
	'sin(x)*exp(-x)' 함수와 '2' 함수가 각각의 도함수와 함께 그래프로 출력된다.
	사용자가 입력한 x값의 범위에 따라 0부터 10까지의 x값에 따른 그래프가 나타난다.
	'sin(x)*exp(-x)' 함수와 '2' 함수는 실선으로, 각각의 도함수는 점선으로 출력된다.


(4)코드 설명:
1.모듈 불러오기: numpy, matplotlib, re
2.사용자가 입력한 수식를 'np.'형태로 변환하기: 예) 'sin(x) -> 'np.sin(x)'
3.Function 클래스: 함수를 저장하기, 함수값을 계산하기, 도함수를 저장하기
4.Plot 클래스: 함수와 도함수를 '그래프'로 출력하기
5.사용자로부터 함수와 x값의 범위, 도함수 출력여부를 입력받기
6.최종적으로 시각화하기



*상세 설명:
1.모듈 불러오기
import numpy as np                 # 수치 계산용 numpy 라이브러리 불러오기
import matplotlib.pyplot as plt    # 그래프 그리기용 matplotlib.pyplot 불러오기
import re                          # 정규표현식 사용을 위한 re 모듈 불러오기


2.사용자가 입력한 수식을 'np.'형태로 변환하기
def convert_to_numpy_expression(expr):
    math_funcs = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs']
    for func in math_funcs:
        expr = re.sub(rf'\b{func}\b', f'np.{func}', expr)
    return expr

3.Function 클래스
-수식을 저장하기:
class Function:
    def __init__(self, expression: str):
        self.original_expr = expression                 # 원래 사용자가 입력한 수식 저장
        self.expression = convert_to_numpy_expression(expression)  # numpy 형태로 변환

-수식의 값을 계산하기:
    def evaluate(self, x):
        try:
            result = eval(self.expression, {"np": np, "x": x})  # np, x 허용된 환경에서 수식 평가
            if np.isscalar(result):                             # 상수이면
                return np.full_like(x, result)                  # x와 같은 크기의 배열로 변환
            return result
        except Exception as e:
            print(f"Error evaluating function '{self.original_expr}': {e}")  # 오류 메시지 출력
            return None

-도함수 구하기:
    def derivative(self, x):
        y = self.evaluate(x)
        if y is not None:
            return np.gradient(y, x)     # 수치적으로 도함수 계산
        return None


4.Plot 클래스
-여러 변수(function, x_range, show_derivative) 정의하기:
class Plot:
    def __init__(self, functions: list, x_range: tuple = (-10, 10), show_derivative=False):
        self.functions = functions
        self.x_range = x_range
        self.show_derivative = show_derivative

-함수와 도함수의 그래프 그리기
    def draw(self):
        x = np.linspace(*self.x_range, 1000)   # x축 값 1000개 생성 (등간격)

        for func in self.functions:
            y = func.evaluate(x)
            if y is not None:
                plt.plot(x, y, label=f"f(x) = {func.original_expr}")   # 원래 수식 이름으로 그래프 표시
                if self.show_derivative:
                    dy = func.derivative(x)
                    if dy is not None:
                        plt.plot(x, dy, linestyle='--', label=f"f'(x) = d/dx({func.original_expr})")  # 도함수는 점선

        plt.title("Function Plotter")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        plt.show()


5.사용자로부터 함수와 x값의 범위, 도함수 출력여부를 입력받기
-함수의 개수를 입력받기:
num_funcs = int(input("몇 개의 함수를 입력하시겠습니까? "))

-함수를 입력받기(만약 잘못된 함수를 입력받으면 다시 입력받기):
functions = []
for i in range(num_funcs):
    while True:
        expr = input(f"{i+1}번째 함수 수식을 입력하세요 (예: sin(x) + cos(x), x**2 + 3*x): ")
        test_func = Function(expr)
        x_test = np.linspace(-1, 1, 10)              # 테스트용 x값
        if test_func.evaluate(x_test) is not None:   # 평가가 성공하면
            functions.append(test_func)              # Function 객체 저장
            break
        else:
            print("잘못된 수식입니다. 다시 입력해주세요.")

-x값의 범위와 도함수 출력 여부를 입력받기:
x_min = float(input("x축 최소값을 입력하세요: "))
x_max = float(input("x축 최대값을 입력하세요: "))
show_derivative = input("도함수도 함께 그릴까요? (y/n): ").strip().lower() == 'y'


6.최종적으로 시각화하기
plot = Plot(functions, x_range=(x_min, x_max), show_derivative=show_derivative)
plot.draw()




(5)흥미로운 부분(수업 내용과 연관)
1. re모듈을 이용해 'sin(x) + cos(x)'와 같은 비공식적 코딩 표현을 'np.sin(x) + np.cos(x)'로 고칠 수 있다는 것이 흥미롭다.
2. try구문을 이용해 만약 함수의 값이 존재하지 않을경우 곧바로 프로그램이 종료되는 것이 아니라 "Error evaluating function '{self.original_expr}'" 메세지를 출력할 수 있다는 것이 흥미롭다.
3.class구문을 이용해 함수값과 도함수값을 계산하는 methods는 Function이라는 class에, 함수와 도함수를 그려주는 methods는 Plot이라는 class에 묶어서 깔끔하게 정리할 수 있다는 것이 흥미롭다.
4.입력받은 수식이 실제로 존재하는 함수인지 확인하기 위해 x_test = np.linspace(-1, 1, 10)라는 테스트용 x범위를 설정해 해당 범위에서 함수가 존재하는지 테스트해 보고 만약 존재하지 않을경우 다시 수식을 입력받게 한 점이 흥미롭다.
5.matplotlib의 method들을 이용해 여러개의 함수들을 표현하고, 축제목과 그래프 모양, 제목 등의 세부사항까지 설정 가능하다는 것이 흥미롭다.


(6)추가적인 도전
다음번에는 미분뿐만 아니라 적분값을 그래프로 출력해보고 싶다.
적분의 시작점(a)을 사용자에게 입력받은뒤 a~x의 범위에 해당하는 적분값을 그래프로 출력하는 것이다.
즉, F(x) = ∫(a~x) f(t) dt 함수를 그래프로 출력하는 것이다.

그렇게 하기 위해서는 다음과 같은 추가 코드가 필요할 것으로 예상된다.
1) 적분 계산을 위한 추가적인 모듈 import
2) Function 클래스에 적분값을 계산하는 methods를 추가
3) Plot 클래스에 적분 함수 그래프 출력 코드를 추가
4) 사용자에게 적분 시작점(a)을 입력받는 항목 추가


