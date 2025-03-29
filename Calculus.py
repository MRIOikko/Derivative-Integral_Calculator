# skibidi rizz
from sympy import symbols, diff, integrate, simplify, trigsimp, pprint
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def main():
    print("Choose an operation: ")
    print("1. Derivative")
    print("2. Integral")
    
    choice = input("Enter 1 or 2: ")
    
    var = input("Enter the variable (e.g., 'x'): ")
    x = symbols(var)
    
    expr_str = input(f"Enter the expression to calculate its {('derivative' if choice == '1' else 'integral')}: ")
    
    expr_str = expr_str.replace('^', '**')
 
    transformations = (standard_transformations + (implicit_multiplication_application,))
    expr = parse_expr(expr_str, transformations=transformations)   
    print("\nOriginal expression (formatted):")
    pprint(expr)   
    if choice == '1':
        calculate_derivative(expr, x)
    elif choice == '2':
        lower_bound = input("lower bound(if you want the indefinite integral, leave it blank): ")
        upper_bound = input("upper bound (if you want the indefinite integral, leave it blank): ")      
        if lower_bound and upper_bound:  
            lower_bound = parse_expr(lower_bound)
            upper_bound = parse_expr(upper_bound)
            calculate_integral(expr, x, lower_bound, upper_bound)
        else:
            calculate_integral(expr, x)
    else:
        print("Invalid choice. Please restart the program.")
def calculate_derivative(expr, var):
    print("\nCalculating derivative...")
    simplified_expr = simplify(expr)
    print("\nStep 1: Simplify the expression:")
    pprint(simplified_expr)
    derivative = diff(simplified_expr, var)
    print("\nStep 2: Take the derivative:")
    pprint(derivative) 
    print("\nFinal Result:")
    pprint(derivative)
def calculate_integral(expr, var, lower_bound=None, upper_bound=None):
    print("\nCalculating integral...")
    simplified_expr = simplify(expr)
    print("\nStep 1: Simplify the expression:")
    pprint(simplified_expr) 
    if "tan" in str(simplified_expr) and "sec" in str(simplified_expr):
        print("\nStep 2: Recognize possible substitution pattern (e.g., tan(x) and sec(x)).")
        print("Since d(tan(x)) = sec^2(x) dx, we recognize this as a form of u-substitution.")
        print("Setting u = tan(x), we find du = sec^2(x) dx.")
    if lower_bound is not None and upper_bound is not None:
        integral = integrate(simplified_expr, (var, lower_bound, upper_bound))
        print(f"\nStep 3: Integrate the expression from {lower_bound} to {upper_bound}:")
    else:
        
        integral = integrate(simplified_expr, var)
        print("\nStep 3: Integrate the expression (indefinite):")
    pprint(integral)
    print("\nStep 4: Simplify the integral result (if possible):")
    simplified_integral = trigsimp(integral)
    pprint(simplified_integral)
    print("\nFinal Result:")
    pprint(simplified_integral)
main()

import tkinter as tk 
root = tk.Tk()
