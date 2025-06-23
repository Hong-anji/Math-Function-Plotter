import numpy as np
import matplotlib.pyplot as plt
import re

def convert_to_numpy_expression(expr):
    math_funcs = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs']
    for func in math_funcs:
        expr = re.sub(rf'\b{func}\b', f'np.{func}', expr)
    return expr

class Function:
    def __init__(self, expression: str):
        self.original_expr = expression
        self.expression = convert_to_numpy_expression(expression)

    def evaluate(self, x):
        try:
            result = eval(self.expression, {"np": np, "x": x})
            if np.isscalar(result):
                return np.full_like(x, result)
            return result
        except Exception as e:
            print(f"Error evaluating function '{self.original_expr}': {e}")
            return None

    def derivative(self, x):
        y = self.evaluate(x)
        if y is not None:
            return np.gradient(y, x)
        return None

class Plot:
    def __init__(self, functions: list, x_range: tuple = (-10, 10), show_derivative=False):
        self.functions = functions
        self.x_range = x_range
        self.show_derivative = show_derivative

    def draw(self):
        x = np.linspace(*self.x_range, 1000)
        
        for func in self.functions:
            y = func.evaluate(x)
            if y is not None:
                plt.plot(x, y, label=f"f(x) = {func.original_expr}")
                if self.show_derivative:
                    dy = func.derivative(x)
                    if dy is not None:
                        plt.plot(x, dy, linestyle='--', label=f"f'(x) = d/dx({func.original_expr})")

        plt.title("Function Plotter")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        plt.show()

num_funcs = int(input("몇 개의 함수를 입력하시겠습니까? "))

functions = []
for i in range(num_funcs):
    while True:
        expr = input(f"{i+1}번째 함수 수식을 입력하세요 (예: sin(x) + cos(x), x**2 + 3*x): ")
        test_func = Function(expr)
        x_test = np.linspace(-1, 1, 10)
        if test_func.evaluate(x_test) is not None:
            functions.append(test_func)
            break
        else:
            print("잘못된 수식입니다. 다시 입력해주세요.")

x_min = float(input("x축 최소값을 입력하세요: "))
x_max = float(input("x축 최대값을 입력하세요: "))
show_derivative = input("도함수도 함께 그릴까요? (y/n): ").strip().lower() == 'y'

plot = Plot(functions, x_range=(x_min, x_max), show_derivative=show_derivative)
plot.draw()

