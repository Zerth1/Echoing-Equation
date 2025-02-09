from enum import Enum, auto
from typing import *
from pyray import *
from sympy import *
import matplotlib.pyplot as plt
import os
import json
import math
import random
import user_interface
RESOLUTION_X = 1450 # No Touchie
RESOLUTION_Y = 800 # No Touchie
RESOLUTION_MULTIPLIER = 1.0 # Touch Me

ACTUAL_RESOLUTION_X = int(RESOLUTION_X * RESOLUTION_MULTIPLIER)
ACTUAL_RESOLUTION_Y = int(RESOLUTION_Y * RESOLUTION_MULTIPLIER)
SETTINGS = {
    "Addition": {
        "Active": True,
        "Gaps": 5,
        "InitialDegreeMin": 1,
        "InitialDegreeMax": 5,
        "TotalTerms": 2,
        "PatternTotalTerms": 2,
    },
    "Multiplication": {
        "Active": True,
        "Gaps": 3,
        "InitialDegreeMin": 1,
        "InitialDegreeMax": 3,
        "TotalTerms": 2,
        "PatternTotalTerms": 1,
    },
}
primary_symbol = symbols("x", positive=True)
index_symbol = symbols("n", positive=True)

init_window(ACTUAL_RESOLUTION_X, ACTUAL_RESOLUTION_Y, "Echoing-Equation")
set_target_fps(get_monitor_refresh_rate(get_current_monitor()))
if os.path.getsize("settings_data.json") == 0:
    with open("settings_data.json", "w") as settings_file:
        settings_file.write(json.dumps(SETTINGS, indent=4))
with open("settings_data.json", "r") as file:
    settings_data = json.load(file)
is_generating = False
is_playing = False
is_settings = False
deep_settings = False
def scale_UI(quantity: float):
    return int(RESOLUTION_MULTIPLIER * quantity)
settings_buttons = {}
settings_buttons["addition_active"] = user_interface.Button("Active:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Active:", 25) + 10), scale_UI(75), scale_UI(25), scale_UI(25)))
settings_buttons["addition_gaps"] = user_interface.InputButton("Gaps:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Gaps:", 25) + 10), scale_UI(125), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["addition_initial_degree_min"] = user_interface.InputButton("Initial Degree Min:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Initial Degree Min:", 25) + 10), scale_UI(175), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["addition_initial_degree_max"] = user_interface.InputButton("Initial Degree Max:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Initial Degree Max:", 25) + 10), scale_UI(225), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["addition_total_terms"] = user_interface.InputButton("Total Terms:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Total Terms:", 25) + 10), scale_UI(275), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["addition_pattern_total_terms"] = user_interface.InputButton("Pattern Total Terms:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Pattern Total Terms:", 25) + 10), scale_UI(325), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["multiplication_active"] = user_interface.Button("Active:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Active:", 25) + 10), scale_UI(75), scale_UI(25), scale_UI(25)))
settings_buttons["multiplication_gaps"] = user_interface.InputButton("Gaps:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Gaps:", 25) + 10), scale_UI(125), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["multiplication_initial_degree_min"] = user_interface.InputButton("Initial Degree Min:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Initial Degree Min:", 25) + 10), scale_UI(175), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["multiplication_initial_degree_max"] = user_interface.InputButton("Initial Degree Max:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Initial Degree Max:", 25) + 10), scale_UI(225), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["multiplication_total_terms"] = user_interface.InputButton("Total Terms:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Total Terms:", 25) + 10), scale_UI(275), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["multiplication_pattern_total_terms"] = user_interface.InputButton("Pattern Total Terms:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Pattern Total Terms:", 25) + 10), scale_UI(325), scale_UI(measure_text("0", 25)), scale_UI(25)))

settings_buttons["addition_active"]._on = settings_data["Addition"]["Active"]
settings_buttons["addition_gaps"].text = str(settings_data["Addition"]["Gaps"])
settings_buttons["addition_initial_degree_min"].text = str(settings_data["Addition"]["InitialDegreeMin"])
settings_buttons["addition_initial_degree_max"].text = str(settings_data["Addition"]["InitialDegreeMax"])
settings_buttons["addition_total_terms"].text = str(settings_data["Addition"]["TotalTerms"])
settings_buttons["addition_pattern_total_terms"].text = str(settings_data["Addition"]["PatternTotalTerms"])

settings_buttons["multiplication_active"]._on = settings_data["Multiplication"]["Active"]
settings_buttons["multiplication_gaps"].text = str(settings_data["Multiplication"]["Gaps"])
settings_buttons["multiplication_initial_degree_min"].text = str(settings_data["Multiplication"]["InitialDegreeMin"])
settings_buttons["multiplication_initial_degree_max"].text = str(settings_data["Multiplication"]["InitialDegreeMax"])
settings_buttons["multiplication_total_terms"].text = str(settings_data["Multiplication"]["TotalTerms"])
settings_buttons["multiplication_pattern_total_terms"].text = str(settings_data["Multiplication"]["PatternTotalTerms"])
blacklist_toggle = []
def redirect_settings():
    global deep_settings
    draw_text("Addition Mode", scale_UI(50), scale_UI(80), scale_UI(25), WHITE)
    draw_text("Multiplication Mode", scale_UI(50), scale_UI(130), scale_UI(25), WHITE)
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        current_position = get_mouse_position()
        if check_collision_point_rec(current_position, Rectangle(scale_UI(50), scale_UI(80), scale_UI(measure_text("Addition Mode", 25)), scale_UI(25))):
            deep_settings = True
            settings_buttons["addition_active"].toggle()
            settings_buttons["addition_gaps"].toggle()
            settings_buttons["addition_initial_degree_min"].toggle()
            settings_buttons["addition_initial_degree_max"].toggle()
            settings_buttons["addition_total_terms"].toggle()
            settings_buttons["addition_pattern_total_terms"].toggle()
        elif check_collision_point_rec(current_position, Rectangle(scale_UI(50), scale_UI(130), scale_UI(measure_text("Multiplication Mode", 25)), scale_UI(25))):
            deep_settings = True
            settings_buttons["multiplication_active"].toggle()
            settings_buttons["multiplication_gaps"].toggle()
            settings_buttons["multiplication_initial_degree_min"].toggle()
            settings_buttons["multiplication_initial_degree_max"].toggle()
            settings_buttons["multiplication_total_terms"].toggle()
            settings_buttons["multiplication_pattern_total_terms"].toggle()
complex_patterns = ["Identity", "Factorial", "Prime", "Exponential", "Fibonacci", "Square", "Triangle"]
fundamental_operations = ["Add", "Sub", "Mul", "Div"]
def custom_factorial(n: int):
    if n == 1:
        return 1
    return n * custom_factorial(n - 1)
def is_prime(n: int):
    for i in range(int(math.sqrt(n))):
        if n % (i + 2) == 0:
            return False
    return True
def custom_prime(n: int):
    primes_encountered = 0
    i = 2
    while primes_encountered != n:
        if is_prime(i):
            primes_encountered += 1
        i += 1
    return i
def custom_exponential(n: int):
    return int(2 ** n)
def custom_fibonacci(n: int):
    if n == 1:
        return 1
    if n == 2:
        return 1
    return custom_fibonacci(n - 1) + custom_fibonacci(n - 2)
def custom_square(n: int):
    return int(n ** 2)
def custom_triangle(n: int):
    return int((n * (n + 1)) / 2)
def create_expr(remaining_terms: int, min_initial_degree: int, max_initial_degree: int, degree_list: List[int]):
    random_degree = random.choice(degree_list)
    degree_list.remove(random_degree)
    if len(degree_list) == 0:
        degree_list = list(range(min_initial_degree, max_initial_degree + 1))
    expr_term = random.randint(1, 9) * (primary_symbol ** random_degree)
    chosen_operation = random.choice(fundamental_operations)
    if remaining_terms == 0:
        return expr_term
    if chosen_operation == "Add":
        return expr_term + create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list)
    elif chosen_operation == "Sub":
        return expr_term - create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list)
    elif chosen_operation == "Mul":
        return expr_term * create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list) 
    elif chosen_operation == "Div":
        degree_list = list(range(min_initial_degree, max_initial_degree + 1))
        return expr_term / create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list) 
def create_pattern_expr(remaining_terms: int, term_to_add: int, min_initial_degree: int, max_initial_degree: int, degree_list: List[int]):
    expr_term = None
    chosen_operation = random.choice(fundamental_operations)
    if remaining_terms == term_to_add:    
        if random.random() < 0.5:
            expr_term = index_symbol * (primary_symbol ** random.randint(min_initial_degree, max_initial_degree))
        else:
            expr_term = random.randint(1, 9) * (primary_symbol ** index_symbol)
    else:
        random_degree = random.choice(degree_list)
        degree_list.remove(random_degree)
        if len(degree_list) == 0:
            degree_list = list(range(min_initial_degree, max_initial_degree + 1))
        expr_term = random.randint(1, 9) * (primary_symbol ** random_degree)
    if remaining_terms == 0:
        return expr_term
    if chosen_operation == "Add":
        return expr_term + create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list)
    elif chosen_operation == "Sub":
        return expr_term - create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list)
    elif chosen_operation == "Mul":
        return expr_term * create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list)
    elif chosen_operation == "Div":
        degree_list = list(range(min_initial_degree, max_initial_degree + 1))
        return expr_term / create_expr(remaining_terms - 1, min_initial_degree, max_initial_degree, degree_list)   
initial_expr = ""
output_expr = ""
input_texture = ""
hint_texture = ""
output_texture = ""
missing_value = 0
def reset_game():
    global initial_expr
    global output_expr
    global input_texture
    global hint_texture
    global output_texture
    global missing_value
    initial_expr = ""
    output_expr = ""
    input_texture = ""
    hint_texture = ""
    output_texture = ""
    missing_value = 0
def latex_to_png(latex_string, output_filename):
    fig, ax = plt.subplots(figsize=(1 * RESOLUTION_MULTIPLIER, 0.33 * RESOLUTION_MULTIPLIER))
    ax.text(0.5, 0.5, f'${latex_string}$', fontsize=scale_UI(5), ha='center', va='center', color='white')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.axis('off')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
chosen_gamemode = ""
while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    if is_generating:
        gamemode_options = []
        if settings_data["Addition"]["Active"]:
            gamemode_options.append("Addition")
        if settings_data["Multiplication"]["Active"]:
            gamemode_options.append("Multiplication")
        chosen_gamemode = random.choice(gamemode_options)
        is_generating = False
        print(chosen_gamemode)
        if chosen_gamemode == "Addition":
            evaluation_number = None
            terms_left = settings_data["Addition"]["TotalTerms"]
            pattern_terms_left = settings_data["Addition"]["PatternTotalTerms"]

            initial_expr = simplify(create_expr(terms_left, settings_data["Addition"]["InitialDegreeMin"], settings_data["Addition"]["InitialDegreeMax"], list(range(settings_data["Addition"]["InitialDegreeMin"], settings_data["Addition"]["InitialDegreeMax"] + 1))))
            chosen_complexity = random.choice(complex_patterns)
            pattern_expr = create_pattern_expr(pattern_terms_left, random.randint(0, pattern_terms_left), settings_data["Addition"]["InitialDegreeMin"], settings_data["Addition"]["InitialDegreeMax"], list(range(settings_data["Addition"]["InitialDegreeMin"], settings_data["Addition"]["InitialDegreeMax"] + 1)))
            hint_expr = None
            output_expr = initial_expr
            print(chosen_complexity)
            for i in range(settings_data["Addition"]["Gaps"]):
                to_add = None
                if chosen_complexity == "Identity":
                    to_add = pattern_expr.subs(index_symbol, i + 1)
                elif chosen_complexity == "Factorial":
                    to_add = pattern_expr.subs(index_symbol, custom_factorial(i + 1))
                elif chosen_complexity == "Prime":
                    to_add = pattern_expr.subs(index_symbol, custom_prime(i + 1))
                elif chosen_complexity == "Exponential":
                    to_add = pattern_expr.subs(index_symbol, custom_exponential(i + 1))
                elif chosen_complexity == "Fibonacci":
                    to_add = pattern_expr.subs(index_symbol, custom_fibonacci(i + 1))
                elif chosen_complexity == "Square":
                    to_add = pattern_expr.subs(index_symbol, custom_square(i + 1))
                elif chosen_complexity == "Triangle":
                    to_add = pattern_expr.subs(index_symbol, custom_triangle(i + 1))
                output_expr += to_add
                print(str(i + 1) + " | Pattern: " + str(sympify(to_add)))
                if i == int(math.ceil(settings_data["Addition"]["Gaps"] / 2)) - 1:
                    hint_expr = sympify(output_expr)
            latex_to_png(latex(initial_expr), "input.png")
            latex_to_png(latex(collect(expand(hint_expr), primary_symbol)), "hint.png")        
            latex_to_png(latex(collect(expand(output_expr), primary_symbol)), "output.png")
            input_texture = load_texture("input.png")
            hint_texture = load_texture("hint.png")
            output_texture = load_texture("output.png")
            if chosen_complexity == "Identity":
                to_add = pattern_expr.subs(index_symbol, settings_data["Addition"]["Gaps"] + 1)
            elif chosen_complexity == "Factorial":
                to_add = pattern_expr.subs(index_symbol, custom_factorial(settings_data["Addition"]["Gaps"] + 1))
            elif chosen_complexity == "Prime":
                to_add = pattern_expr.subs(index_symbol, custom_prime(settings_data["Addition"]["Gaps"] + 1))
            elif chosen_complexity == "Exponential":
                to_add = pattern_expr.subs(index_symbol, custom_exponential(settings_data["Addition"]["Gaps"] + 1))
            elif chosen_complexity == "Fibonacci":
                to_add = pattern_expr.subs(index_symbol, custom_fibonacci(settings_data["Addition"]["Gaps"] + 1))
            elif chosen_complexity == "Square":
                to_add = pattern_expr.subs(index_symbol, custom_square(settings_data["Addition"]["Gaps"] + 1))
            elif chosen_complexity == "Triangle":
                to_add = pattern_expr.subs(index_symbol, custom_triangle(settings_data["Addition"]["Gaps"] + 1))
            missing_value = int((output_expr + to_add).subs(primary_symbol, 2).evalf())
            print(str(i + 1) + " | Pattern: " + sympify(to_add))
            print(missing_value)
        elif chosen_gamemode == "Multiplication":
            evaluation_number = None
            terms_left = settings_data["Multiplication"]["TotalTerms"]
            pattern_terms_left = settings_data["Multiplication"]["PatternTotalTerms"]
            initial_expr = simplify(create_expr(terms_left, settings_data["Multiplication"]["InitialDegreeMin"], settings_data["Multiplication"]["InitialDegreeMax"], list(range(settings_data["Addition"]["InitialDegreeMin"], settings_data["Multiplication"]["InitialDegreeMax"] + 1))))
            chosen_complexity = random.choice(complex_patterns)
            pattern_expr = create_pattern_expr(pattern_terms_left, random.randint(0, pattern_terms_left), settings_data["Addition"]["InitialDegreeMin"], settings_data["Addition"]["InitialDegreeMax"], list(range(settings_data["Addition"]["InitialDegreeMin"], settings_data["Addition"]["InitialDegreeMax"] + 1)))
            hint_expr = None
            output_expr = initial_expr
            print(chosen_complexity)
            for i in range(settings_data["Multiplication"]["Gaps"]):
                to_multiply = None
                if chosen_complexity == "Identity":
                    to_multiply = pattern_expr.subs(index_symbol, i + 1)
                elif chosen_complexity == "Factorial":
                    to_multiply = pattern_expr.subs(index_symbol, custom_factorial(i + 1))
                elif chosen_complexity == "Prime":
                    to_multiply = pattern_expr.subs(index_symbol, custom_prime(i + 1))
                elif chosen_complexity == "Exponential":
                    to_multiply = pattern_expr.subs(index_symbol, custom_exponential(i + 1))
                elif chosen_complexity == "Fibonacci":
                    to_multiply = pattern_expr.subs(index_symbol, custom_fibonacci(i + 1))
                elif chosen_complexity == "Square":
                    to_multiply = pattern_expr.subs(index_symbol, custom_square(i + 1))
                elif chosen_complexity == "Triangle":
                    to_multiply = pattern_expr.subs(index_symbol, custom_triangle(i + 1))
                output_expr *= to_multiply
                print(str(i + 1) + " | Pattern: " + str(sympify(to_multiply)))
                if i == int(math.ceil(settings_data["Multiplication"]["Gaps"] / 2)) - 1:
                    hint_expr = sympify(output_expr)
            latex_to_png(latex(initial_expr), "input.png")
            latex_to_png(latex(collect(expand(hint_expr), primary_symbol)), "hint.png")    
            latex_to_png(latex(collect(expand(output_expr), primary_symbol)), "output.png")
            input_texture = load_texture("input.png")
            hint_texture = load_texture("hint.png")
            output_texture = load_texture("output.png")
            if chosen_complexity == "Identity":
                to_multiply = pattern_expr.subs(index_symbol, settings_data["Multiplication"]["Gaps"] + 1)
            elif chosen_complexity == "Factorial":
                to_multiply = pattern_expr.subs(index_symbol, custom_factorial(settings_data["Multiplication"]["Gaps"] + 1))
            elif chosen_complexity == "Prime":
                to_multiply = pattern_expr.subs(index_symbol, custom_prime(settings_data["Multiplication"]["Gaps"] + 1))
            elif chosen_complexity == "Exponential":
                to_multiply = pattern_expr.subs(index_symbol, custom_exponential(settings_data["Multiplication"]["Gaps"] + 1))
            elif chosen_complexity == "Fibonacci":
                to_multiply = pattern_expr.subs(index_symbol, custom_fibonacci(settings_data["Multiplication"]["Gaps"] + 1))
            elif chosen_complexity == "Square":
                to_multiply = pattern_expr.subs(index_symbol, custom_square(settings_data["Multiplication"]["Gaps"] + 1))
            elif chosen_complexity == "Triangle":
                to_multiply = pattern_expr.subs(index_symbol, custom_triangle(settings_data["Multiplication"]["Gaps"] + 1))
            missing_value = int((output_expr * to_multiply).subs(primary_symbol, 1).evalf())
            print(missing_value)
    if is_settings:
        if deep_settings:
            pass
        else:
            redirect_settings()
    else:
        draw_text("[Space] Start/Stop", scale_UI(int(RESOLUTION_X / 2) - int(measure_text("[Space] Start/Stop", 50) / 2)), scale_UI(int(0.85 * (RESOLUTION_Y))), scale_UI(50), WHITE)      
        if is_playing:
            draw_texture_ex(input_texture, Vector2(0, 0), 0.0, max(1.0, float(int(scale_UI(1.0)))), WHITE)
            draw_texture_ex(hint_texture, Vector2(0, int(scale_UI(input_texture.height))), 0.0, max(1.0, float(int(scale_UI(1.0)))), WHITE)
            draw_texture_ex(output_texture, Vector2(0, int(scale_UI(input_texture.height + hint_texture.height))), 0.0, max(1.0, float(int(scale_UI(1.0)))), WHITE)
            draw_text("Term: 1", scale_UI(input_texture.width + 100), scale_UI(input_texture.height / 2), scale_UI(25), WHITE)
            draw_text("Term: " + str(int(math.ceil(settings_data[chosen_gamemode]["Gaps"] / 2))), scale_UI(hint_texture.width + 100), scale_UI(int(input_texture.height) + int(hint_texture.height / 2)), scale_UI(25), WHITE)
            draw_text("Term: " + str(settings_data[chosen_gamemode]["Gaps"] + 1), scale_UI(output_texture.width + 100), scale_UI(int(input_texture.height + hint_texture.height) + int(output_texture.height / 2)), scale_UI(25), WHITE)
            if chosen_gamemode == "Addition":
                draw_text("Term: " + str(settings_data[chosen_gamemode]["Gaps"] + 2) + " [x=2] | ?", scale_UI(50), scale_UI(RESOLUTION_Y - scale_UI(55)), scale_UI(25), WHITE)
            elif chosen_gamemode == "Multiplication":
                draw_text("Term: " + str(settings_data[chosen_gamemode]["Gaps"] + 2) + " [x=1] | ?", scale_UI(50), scale_UI(RESOLUTION_Y - scale_UI(55)), scale_UI(25), WHITE)
        else:
            draw_text("[S] Settings", scale_UI(50), scale_UI(30), scale_UI(25), WHITE)
        if is_key_pressed(KeyboardKey.KEY_SPACE):
            if not is_playing:
                is_generating = True
                reset_game()
            is_playing = not is_playing
    if not is_playing and is_key_pressed(KeyboardKey.KEY_S):
        reset_game()
        if deep_settings:
            deep_settings = False
            for key, settings_object in settings_buttons.items():
                if settings_object._enabled:
                    blacklist_toggle.append(key)    
                    settings_object.toggle()
                else:
                    if key in blacklist_toggle:
                        blacklist_toggle.remove(key)
        else:
            is_settings = not is_settings
        settings_data["Addition"]["Active"] = settings_buttons["addition_active"]._on
        settings_data["Addition"]["Gaps"] = max(int(settings_buttons["addition_gaps"].text), 3)
        settings_data["Addition"]["InitialDegreeMin"] = max(int(settings_buttons["addition_initial_degree_min"].text), 1)
        settings_data["Addition"]["InitialDegreeMax"] = max(int(settings_buttons["addition_initial_degree_max"].text), settings_data["Addition"]["InitialDegreeMin"], 1)
        settings_data["Addition"]["TotalTerms"] = max(int(settings_buttons["addition_total_terms"].text), 1)
        settings_data["Addition"]["PatternTotalTerms"] = max(int(settings_buttons["addition_pattern_total_terms"].text), 1)
        settings_data["Multiplication"]["Active"] = settings_buttons["multiplication_active"]._on 
        settings_data["Multiplication"]["Gaps"] = max(int(settings_buttons["multiplication_gaps"].text), 3)
        settings_data["Multiplication"]["InitialDegreeMin"] = max(int(settings_buttons["multiplication_initial_degree_min"].text), 1)
        settings_data["Multiplication"]["InitialDegreeMax"] = max(int(settings_buttons["multiplication_initial_degree_max"].text), settings_data["Multiplication"]["InitialDegreeMin"], 1)
        settings_data["Multiplication"]["TotalTerms"] = max(int(settings_buttons["multiplication_total_terms"].text), 1)
        settings_data["Multiplication"]["PatternTotalTerms"] = max(int(settings_buttons["multiplication_pattern_total_terms"].text), 1)
        with open("settings_data.json", "w") as file:
            json.dump(settings_data, file)
    for settings_object in settings_buttons.values():
        settings_object.update()
    end_drawing()
close_window()    
