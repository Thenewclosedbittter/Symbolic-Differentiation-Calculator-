print("Symbolic Differentiation Calculator")


# Find GCD
def gcd(a,b):
    while b:
        a, b = b, a % b
    return a
# Adding fraction support (Calculator doesn't support fraction module in Python)
class Fraction:
    def __init__(self, numerator, denominator=1):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)

    def __add__(self, other):
        # Common denominator means we are just adding the numerators
        if self.denominator == other.denominator:
            return Fraction(self.numerator + other.numerator, self.denominator)
        # Find common denominator
        new_num = (self.numerator * other.denominator + other.numerator * self.denominator)
        new_den = (self.denominator * other.denominator)

        divisor = gcd(new_num, new_den)
        new_num //= divisor
        new_den //= divisor

        return Fraction(new_num, new_den)
    # Subtract fractions
    def __sub__(self, other):
        if self.denominator == other.denominator:
            return Fraction(self.numerator - other.numerator, self.denominator)
        new_num = (self.numerator * other.denominator - other.numerator * self.denominator)
        new_den = (self.denominator * other.denominator)

        divisor = gcd(new_num, new_den)
        new_num //= divisor
        new_den //= divisor
        return Fraction(new_num, new_den)
    # Multiplying fractions
    def __mul__(self, other):
        new_num = (self.numerator * other.numerator)
        new_den = (self.denominator * other.denominator)
        divisor = gcd(new_num, new_den)
        new_num //= divisor
        new_den //= divisor
        return Fraction(new_num, new_den)
    def divide(self, other):
        # KCF
        flipped_num = other.denominator
        flipped_den = other.numerator

        new_num = self.numerator * flipped_num
        new_den = self.denominator * flipped_den

        divisor = gcd(new_num, new_den)
        new_num //= divisor
        new_den //= divisor

        return Fraction(new_num, new_den)


fraction = Fraction(3, 5)
fraction1 = Fraction(3, 4)
print(fraction.divide(fraction1))


# Power rule for single terms
def power_rule(df_x):
    a = ""
    for c in df_x:
        if c == "x":
            break
        a += c

    n = ""
    i = 0
    while i < len(df_x):
        if df_x[i] == "^":
            n = df_x[i + 1:]
            break
        i += 1

    if "x" not in df_x:
        return "0"
    if df_x == "x":
        return "1"
    if df_x == "-x":
        return "-1"
    if df_x.endswith("x") and "^" not in df_x:
        return a if a not in ["", "-"] else ("-1" if a == "-" else "1")

    # Coefficient a
    if a == "-":
        a = Fraction(-1)
    elif a != "" and "/" not in a:
        a = Fraction(int(a))
    elif "/" in a:
        numerator, denominator = a.split("/")
        a = Fraction(int(numerator), int(denominator))
    else:
        a = Fraction(1)

    # Exponent n
    if n == "":
        n = Fraction(1)
    elif "/" in n:
        numerator, denominator = n.split("/")
        n = Fraction(int(numerator), int(denominator))
    else:
        n = Fraction(int(n))

    # Compute new coefficient and exponent safely
    new_coeff = a * n
    new_exp = n - Fraction(1)

    # Convert to int if whole number
    if isinstance(new_coeff, Fraction) and new_coeff.denominator == 1:
        new_coeff = new_coeff.numerator
    if isinstance(new_exp, Fraction) and new_exp.denominator == 1:
        new_exp = new_exp.numerator

    if new_exp == 0:
        return str(new_coeff)

    result = str(new_coeff) + "x"
    if new_exp != 1:
        result += "^" + str(new_exp)
    return result



# Subtraction helper (subtracts a list: opposite of sum)
def sub(nums):
    result = nums[0]
    for n in nums[1:]:
        result -= n
    return result


# Split terms, ignoring signs after ^
def split_terms(expr, sign):
    terms = []
    term = ""
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == sign and (i == 0 or expr[i - 1] != "^"):
            if term != "":
                terms.append(term)
            term = ""
        term += c
        i += 1
    if term:
        terms.append(term)
    return terms


def process_terms(df_x, sign):
    df_x = split_terms(df_x, sign)

    # Differentiate each term
    for i in range(len(df_x)):
        df_x[i] = power_rule(df_x[i])

    # Combine like terms
    combined = {}
    for t in df_x:
        if t == "0":
            continue  # skip zero terms early

        if "x" in t:
            if "^" in t:
                var = t[t.find("x"):]
            else:
                var = "x"
        else:
            var = ""

        coeff_str = t[:t.find("x")] if "x" in t else t

        # Handle empty or "-" coefficients
        if coeff_str == "" or coeff_str == "+":
            coeff = 1
        elif coeff_str == "-":
            coeff = -1
        else:
            coeff = int(coeff_str)

        combined[var] = combined.get(var, 0) + coeff

    # Build result
    result = []
    for var, coeff in combined.items():
        if coeff == 0:
            continue

        if var == "":
            result.append(str(coeff))
        elif coeff == 1:
            result.append(var)
        elif coeff == -1:
            result.append("-" + var)
        else:
            result.append(str(coeff) + var)
    if not result:
        return "0"

    return "+".join(result).replace("+-", "-")


# This functions determines what rule is going to be used: power rule, chain rule, trigonometric identities, quotient rule, etc.

def diff(df_x):
    df_x = df_x.replace(" ", "")
    # If there are multiple terms/the function is a polynomial and the two terms are being added together (eg 2x+2)
    if "+" in df_x:
        return process_terms(df_x, "+")
    # If there are multiple terms/the function is a polynomial and the two terms are being subtracted (eg 2x-2)
    elif "-" in df_x[1:]:
        return process_terms(df_x, "-")
    # Single term (eg 5x). No need to "simplify" terms; if you do so, the output won't be correct (eg derivative of constant will display nothing instead of 0). Also, it's already simplified because it's one term. 
    else:
        return power_rule(df_x)



f_x = input("Input f(x): ")

if "**" in f_x:
    f_x = f_x.replace("**", "^")
if "X" in f_x:
    f_x = f_x.replace("X", "x")

print("f'(x) = " + diff(f_x))
