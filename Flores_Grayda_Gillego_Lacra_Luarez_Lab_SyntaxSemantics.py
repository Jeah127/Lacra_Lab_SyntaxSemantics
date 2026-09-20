# Laboratory Activity 2: Syntax Checker and Evaluator
# Group Members:
#Flores Jonah
# Gillego Althea
#Grayda Rashell
# Lacra Jeah
# Luarez Alowena Claire


class ExpressionParser:
    def __init__(self, text):
        # Remove spaces to simplify parsing
        self.text = text.replace(" ", "")
        self.index = 0

    def current_char(self):
        """Returns the character at the current index, or None if at the end."""
        if self.index < len(self.text):
            return self.text[self.index]
        return None

    def consume(self):
        """Advances to the next character and returns the previous one."""
        char = self.current_char()
        self.index += 1
        return char

    # <factor> -> ( <expr> ) | <digit>
    def parse_factor(self):
        char = self.current_char()

        # Handle parenthesized expressions: ( expr )
        if char == '(':
            self.consume()
            value = self.parse_expr()  # Recursion happens here!
            
            if self.current_char() != ')':
                raise SyntaxError(f"Missing closing ')' at index {self.index}")
            self.consume()
            return value

        # Handle single digits
        if char and char.isdigit():
            return float(self.consume())

        # If it's neither a digit nor '(', it's an unexpected character
        raise SyntaxError(f"Unexpected token '{char}' at index {self.index}")

    # <term> -> <factor> { (* | /) <factor> }
    def parse_term(self):
        value = self.parse_factor()

        while self.current_char() in ('*', '/'):
            operator = self.consume()
            next_value = self.parse_factor()
            
            if operator == '*':
                value *= next_value
            elif operator == '/':
                if next_value == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                value /= next_value

        return value

    # <expr> -> <term> { (+ | -) <term> }
    def parse_expr(self):
        value = self.parse_term()

        while self.current_char() in ('+', '-'):
            operator = self.consume()
            next_value = self.parse_term()
            
            if operator == '+':
                value += next_value
            elif operator == '-':
                value -= next_value

        return value

    def run(self):
        """Runs the parser and returns (status, result)."""
        try:
            result = self.parse_expr()
            
            # Check if there are leftover unparsed characters
            if self.index < len(self.text):
                raise SyntaxError(f"Leftover characters at index {self.index}")
                
            # Convert whole floats (e.g., 14.0) to clean integers (14)
            formatted_result = int(result) if result.is_integer() else result
            return "Valid", formatted_result
            
        except (SyntaxError, ZeroDivisionError) as error:
            return f"Invalid syntax ({error})", "—"


if __name__ == "__main__":
    while True:
        user_input = input("Enter expression: ").strip()

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        if not user_input:
            continue

        status, result = ExpressionParser(user_input).run()
        print(f"Syntax Check : {status}")
        print(f"Evaluated    : {result}\n")