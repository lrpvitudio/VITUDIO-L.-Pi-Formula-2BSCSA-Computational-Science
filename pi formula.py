import turtle
import time
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_UP

# set precision to 150 to make sure "true" baseline is good.
getcontext().prec = 150

# "true" value of pi (100+ digits) used as answer key
pi_true_str = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647"
pi_real = Decimal(pi_true_str)

r = 10 # radius
# calculate area with true pi to compare against
area_true = 4 * pi_real * (r ** 2)

# decimal places to test
decimals_to_test = [4, 20, 40, 60, 100]

# helper function to make numbers readable.
# if val > 0.0001, show standard decimal.
# else, show scientific notation.
def smart_fmt(val):
    if val > 1e-4:
        return f"{val:.6f}"
    else:
        return f"{val:.2E}"

print("========================================")
print(" EXPERIMENT: ACCURACY OF TRUNCATION VS ROUNDING")
print("========================================")
print(f"Shape:       Sphere")
print(f"Radius (r):  {r} units")
print(f"Formula:     Area = 4 * pi * r^2")
print(f"True Area:   {area_true:.10f} (Baseline)")
print("-" * 110)

# table header
# showing both absolute difference (value) and relative error (%)
table_header = f"{'Decimals':<9} | {'TRUNC: Abs Diff':<20} | {'TRUNC: Rel %':<15} | {'ROUND: Abs Diff':<20} | {'ROUND: Rel %':<15}"

first_run = True # flag to control printing

for d in decimals_to_test:
    # tells python where to cut the number.
    quantizer = Decimal("1." + "0" * d)

    # chop off extra digits.
    pi_trunc = Decimal(pi_true_str).quantize(quantizer, rounding=ROUND_DOWN)

    # if next digit is 5+, round up.
    pi_round = Decimal(pi_true_str).quantize(quantizer, rounding=ROUND_HALF_UP)

    # calculate surface area
    area_trunc = 4 * pi_trunc * (r ** 2)
    area_round = 4 * pi_round * (r ** 2)

    # calculate errors (distance from true area)
    # absolute difference = |calculated - true|
    abs_diff_trunc = abs(area_trunc - area_true)
    abs_diff_round = abs(area_round - area_true)

    # relative error (%)
    rel_err_trunc_pct = (abs_diff_trunc / area_true) * 100
    rel_err_round_pct = (abs_diff_round / area_true) * 100

    # visualization step (only for 4 decimals)
    if first_run:
        print(f"\n[VISUALIZING CALCULATION STEP FOR {d} DECIMALS]")
        print(f"Truncation Method:")
        print(f"   Pi Used: {pi_trunc}")
        print(f"   Solve:   4 * {pi_trunc} * 100")
        print(f"   Result:  {area_trunc}")
        print(f"Rounding Method:")
        print(f"   Pi Used: {pi_round}")
        print(f"   Solve:   4 * {pi_round} * 100")
        print(f"   Result:  {area_round}")
        print("-" * 110)
        print(table_header)
        print("-" * 110)
        first_run = False

    print(f"{d:<9} | {smart_fmt(abs_diff_trunc):<20} | {smart_fmt(rel_err_trunc_pct)}%           | {smart_fmt(abs_diff_round):<20} | {smart_fmt(rel_err_round_pct)}%")

print("\n" + "="*50)
input(">>> Press ENTER to launch Visual Simulation!!!")
print("="*50)

# setup
screen = turtle.Screen()
screen.title("Accuracy Visualization: Truncation vs Rounding")
screen.bgcolor()

t = turtle.Turtle()
t.speed(6)
t.hideturtle()
t.width(3)

# grid background
def draw_grid():
    screen.tracer(0)
    grid_t = turtle.Turtle()
    grid_t.hideturtle()
    grid_t.speed(0)
    grid_t.color("#E0E0E0")
    grid_t.width(1)

    for x in range(-300, 301, 50):
        grid_t.penup()
        grid_t.goto(x, -300)
        grid_t.pendown()
        grid_t.goto(x, 300)

    for y in range(-300, 301, 50):
        grid_t.penup()
        grid_t.goto(-300, y)
        grid_t.pendown()
        grid_t.goto(300, y)

    grid_t.color("#A0A0A0")
    grid_t.width(2)
    grid_t.penup(); grid_t.goto(0, -300); grid_t.pendown(); grid_t.goto(0, 300)
    grid_t.penup(); grid_t.goto(-300, 0); grid_t.pendown(); grid_t.goto(300, 0)

    screen.update()
    screen.tracer(1)

# visual representation
def draw_circle(radius, color, label, text_x, text_y):
    t.penup()
    t.goto(0, -radius)
    t.pendown()

    t.color(color)
    t.circle(radius)

    t.penup()
    t.goto(text_x, text_y)
    t.write(label, align="center", font=("Arial", 12, "bold"))

draw_grid()
time.sleep(0.5)

t.speed(6)
draw_circle(200, "black", "TRUE AREA(BASELINE)",0, 210)
time.sleep(1)

draw_circle(150, "red", "TRUNCATED", 0, -20)
time.sleep(1)

draw_circle(190, "blue", "ROUNDED", 0, -240)

t.penup()
t.goto(0, -290)
t.color("gray")
t.write("Visual exaggerated for visibility! Not to scale!", align="right", font=("Arial", 10, "italic"))

screen.exitonclick()



