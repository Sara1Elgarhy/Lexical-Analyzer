LETTER = 0
DIGIT = 1
UNKNOWN = 99
END_OF_FILE = -1

INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26

char_class = None
lexeme = ''
next_char = ''
next_token = None
in_fp = None


def add_char():
    global lexeme, next_char
    lexeme += next_char


def get_char():
    global next_char, char_class
    next_char = in_fp.read(1)
    if next_char:
        if next_char.isalpha():
            char_class = LETTER
        elif next_char.isdigit():
            char_class = DIGIT
        else:
            char_class = UNKNOWN
    else:
        char_class = END_OF_FILE


def get_non_blank():
    global next_char
    while next_char.isspace():
        get_char()


def lookup(ch):
    global next_token
    lookup_table = {
        '(': LEFT_PAREN,
        ')': RIGHT_PAREN,
        '+': ADD_OP,
        '-': SUB_OP,
        '*': MULT_OP,
        '/': DIV_OP,
        '=': ASSIGN_OP,
    }
    add_char()
    next_token = lookup_table.get(ch, END_OF_FILE)
    return next_token


def lex():
    global lexeme, next_token
    lexeme = ''
    get_non_blank()

    if char_class == LETTER:
        add_char()
        get_char()
        while char_class in [LETTER, DIGIT]:
            add_char()
            get_char()
        next_token = IDENT

    elif char_class == DIGIT:
        add_char()
        get_char()
        while char_class == DIGIT:
            add_char()
            get_char()
        next_token = INT_LIT

    elif char_class == UNKNOWN:
        lookup(next_char)
        get_char()

    elif char_class == END_OF_FILE:
        next_token = END_OF_FILE
        lexeme = "EOF"

    print(f"Next token is: {next_token}, Next lexeme is {lexeme}")
    return next_token


def main():
    global in_fp
    try:
        with open("front.in", "r") as in_fp_context:
            globals()['in_fp'] = in_fp_context
            get_char()
            while True:
                if lex() == END_OF_FILE:
                    break
    except FileNotFoundError:
        print("ERROR - cannot open front.in")


if __name__ == "__main__":
    main()
