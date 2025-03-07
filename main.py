import sys
import re

def tokenize(source_code):
    token_pattern = r'\".*?\"|\S+'
    tokens = re.findall(token_pattern, source_code)
    return tokens

def parse(tokens):
    asm_code = []
    variables = {}
    register_counter = 1
    i = 0
    while i < len(tokens):
        token = tokens[i]
        print(token)
        if token == "var":
            if i + 2 < len(tokens) and tokens[i + 2] == "=":
                var_name = tokens[i + 1]
                var_value = tokens[i + 3]
                reg = f"R{register_counter}"
                variables[var_name] = reg
                asm_code.append(f"SET {var_value} {reg}")
                register_counter += 1
                i += 3 
        elif token == "print":
            if i + 1 < len(tokens) and tokens[i + 1].startswith('"'):
                asm_code.append(f"PRINT {tokens[i + 1]}") 
                i += 1 
            else:
                asm_code.append(f"OUT {tokens[i + 1]}") 
        elif token.isdigit():
            asm_code.append(f"PUSH {token}")
        elif token == "+":
            asm_code.append("ADD")
        elif token == "-":
            asm_code.append("SUB")
        elif token == "*":
            asm_code.append("MUL")
        elif token == "/":
            asm_code.append("DIV")
        elif token == "if":
            asm_code.append("JUMP_IF_ZERO")
        elif token == "goto":
            if i + 1 < len(tokens):
                asm_code.append(f"JUMP {tokens[i+1]}")
                i += 1 
        i += 1
    return asm_code

def compile_tost_to_tasm(tost_code):
    tokens = tokenize(tost_code)
    asm_code = parse(tokens)
    return '\n'.join(asm_code)

def main():
    input_file = input("Enter the .tost file to compile: ")
    output_file = input_file.replace(".tost", ".tasm")
    
    with open(input_file, "r") as f:
        tost_code = f.read()
    
    tasm_code = compile_tost_to_tasm(tost_code)
    
    with open(output_file, "w") as f:
        f.write(tasm_code)
    
    print(f"Compilation successful! Output written to {output_file}")

if __name__ == "__main__":
    main()
