from sympy import symbols, diff, integrate, simplify, trigsimp, pprint
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def main():
    print("Choose an operation: ")
    print("1. Derivative")
    print("2. Integral")
    print("3. Partial Derivative")
    print("4. Double Integral")
    
    choice = input("Enter 1, 2, 3, or 4: ")
    
    if choice == '3':
        # Handles partial derivatives
        vars_input = input("Enter all variables, separated by commas (e.g., 'x,y,z'): ")
        var_list = [v.strip() for v in vars_input.split(',')]
        sym_vars = symbols(var_list)
        
        diff_var = input("Enter the variable to differentiate with respect to: ")
        if diff_var not in var_list:
            print(f"Error: {diff_var} is not in the list of variables.")
            return
            
        expr_str = input("Enter the expression to calculate its partial derivative: ")
        expr_str = expr_str.replace('^', '**')
        
        transformations = (standard_transformations + (implicit_multiplication_application,))
        expr = parse_expr(expr_str, transformations=transformations, local_dict={str(s): s for s in sym_vars})
        
        print("\nOriginal expression (formatted):")
        pprint(expr)
        
        # Gets the symbol to differentiate with respect to
        diff_sym = symbols(diff_var)
        calculate_partial_derivative(expr, diff_sym)
    elif choice == '4':
        # Handles double integrals
        vars_input = input("Enter the two variables for integration, separated by comma (e.g., 'x,y'): ")
        var_list = [v.strip() for v in vars_input.split(',')]
        
        if len(var_list) != 2:
            print("Error: Double integral requires exactly two variables.")
            return
            
        sym_vars = symbols(var_list)
        x, y = sym_vars
        
        expr_str = input("Enter the expression to calculate its double integral: ")
        expr_str = expr_str.replace('^', '**')
        
        transformations = (standard_transformations + (implicit_multiplication_application,))
        expr = parse_expr(expr_str, transformations=transformations, local_dict={str(sym_vars[0]): sym_vars[0], str(sym_vars[1]): sym_vars[1]})
        
        print("\nOriginal expression (formatted):")
        pprint(expr)
        
        # Get integration bounds
        x_lower = input(f"Enter lower bound for {var_list[0]} (leave blank for indefinite integral): ")
        x_upper = input(f"Enter upper bound for {var_list[0]} (leave blank for indefinite integral): ")
        y_lower = input(f"Enter lower bound for {var_list[1]} (leave blank for indefinite integral): ")
        y_upper = input(f"Enter upper bound for {var_list[1]} (leave blank for indefinite integral): ")
        
        # Parse bounds if provided
        x_lower = parse_expr(x_lower) if x_lower else None
        x_upper = parse_expr(x_upper) if x_upper else None
        y_lower = parse_expr(y_lower) if y_lower else None
        y_upper = parse_expr(y_upper) if y_upper else None
        
        # Check if we have all bounds or none for each variable
        x_def = (x_lower is not None and x_upper is not None)
        y_def = (y_lower is not None and y_upper is not None)
        
        calculate_double_integral(expr, x, y, x_lower, x_upper, y_lower, y_upper, x_def, y_def)
    else:
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

def calculate_partial_derivative(expr, var):
    print(f"\nCalculating partial derivative with respect to {var}...")
    simplified_expr = simplify(expr)
    print("\nStep 1: Simplify the expression:")
    pprint(simplified_expr)
    
    partial_derivative = diff(simplified_expr, var)
    print(f"\nStep 2: Take the partial derivative with respect to {var}:")
    pprint(partial_derivative)
    
    simplified_derivative = simplify(partial_derivative)
    print("\nStep 3: Simplify the result (if possible):")
    pprint(simplified_derivative)
    
    print("\nFinal Result:")
    pprint(simplified_derivative)

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

def calculate_double_integral(expr, x_var, y_var, x_lower=None, x_upper=None, y_lower=None, y_upper=None, x_def=False, y_def=False):
    print("\nCalculating double integral...")
    simplified_expr = simplify(expr)
    print("\nStep 1: Simplify the expression:")
    pprint(simplified_expr)
    
    # Step 2: We'll integrate with respect to the first variable first
    print(f"\nStep 2: Integrate with respect to {y_var} first:")
    
    if y_def:
        # Definite integral for y
        inner_integral = integrate(simplified_expr, (y_var, y_lower, y_upper))
        print(f"\nIntegrating with respect to {y_var} from {y_lower} to {y_upper}:")
    else:
        # Indefinite integral for y
        inner_integral = integrate(simplified_expr, y_var)
        print(f"\nIntegrating with respect to {y_var} (indefinite):")
    
    pprint(inner_integral)
    
    # Step 3: Now integrate the result with respect to the second variable
    print(f"\nStep 3: Integrate the result with respect to {x_var}:")
    
    if x_def:
        # Definite integral for x
        final_integral = integrate(inner_integral, (x_var, x_lower, x_upper))
        print(f"\nIntegrating with respect to {x_var} from {x_lower} to {x_upper}:")
    else:
        # Indefinite integral for x
        final_integral = integrate(inner_integral, x_var)
        print(f"\nIntegrating with respect to {x_var} (indefinite):")
    
    pprint(final_integral)
    
    # Step 4: Simplify the result if possible
    print("\nStep 4: Simplify the final result (if possible):")
    simplified_integral = trigsimp(final_integral)
    pprint(simplified_integral)
    
    print("\nFinal Result:")
    pprint(simplified_integral)
    
    # Provides summary of the integration with bounds
    if x_def and y_def:
        print(f"\nSummary: ∫∫ f({x_var},{y_var}) d{y_var} d{x_var} from {y_var}={y_lower} to {y_var}={y_upper} and {x_var}={x_lower} to {x_var}={x_upper} = {simplified_integral}")
    elif x_def:
        print(f"\nSummary: ∫(∫ f({x_var},{y_var}) d{y_var}) d{x_var} from {x_var}={x_lower} to {x_var}={x_upper} = {simplified_integral}")
    elif y_def:
        print(f"\nSummary: ∫(∫ f({x_var},{y_var}) d{y_var} from {y_var}={y_lower} to {y_var}={y_upper}) d{x_var} = {simplified_integral}")
    else:
        print(f"\nSummary: ∫∫ f({x_var},{y_var}) d{y_var} d{x_var} = {simplified_integral}")

if __name__ == "__main__":
    main()