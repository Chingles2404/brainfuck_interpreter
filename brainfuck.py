# processes all brainfuck functions except for loops themselves
def brainfuck_functions(code, i, idx, mem, output):
    if code[i] == ">":
        idx += 1
    elif code[i] == "<":
        idx -= 1
    elif code[i] == "+":
        mem[idx] += 1
    elif code[i] == "-":
        mem[idx] -= 1
    elif code[i] == ".":
        output += chr(mem[idx])
    elif code[i] == ",":
        mem[idx] = int(input())
    if idx > len(mem) - 1:
        for j in range(len(mem) - 1, idx):
            mem.append(0)
    return idx, mem, output

# processes brainfuck loops
def f_loop(loop, code, idx, mem, output):
    i = 0
    done_1 = False
    while not done_1:
        # terminating condition
        if mem[idx] == 0 and i == 0:
            done_1 = True
        else:
            if type(loop[i]) == str:
                idx, mem, output = brainfuck_functions(loop, i, idx, mem, output)
            else:
                j = 0
                done_2 = False
                while not done_2:
                    # terminating condition
                    if mem[idx] == 0 and j == 0:
                        done_2 = True
                    else:
                        idx, mem, output = brainfuck_functions(loop[i], j, idx, mem, output)
                        j += 1
                        if j == len(loop[i]):
                            j = 0
            i += 1
            if i == len(loop):
                i = 0
    return idx, mem, output

# removes all redundant characters
def read_file(filename):
    f = open(filename, "r")
    line = f.readline()
    bf_chars = [">", "<", "+", "-", ".", ",", "[", "]"]
    code = ""
    while line:
        for char in line:
            if char in bf_chars:
                code += char
        line = f.readline()
    f.close()
    return code

# determines when a loop is created or when a non-loop function is being carried out
def read_brainfuck(code):
    idx = 0
    mem = [0]
    output = ""
    loop = []
    i = 0
    while i < len(code):
        if loop == []:
            if code[i] == "[":
                if code[i + 1] != "[":
                    loop.append(code[i + 1])
                    i += 1
                else:
                    loop.append([])
            else:
                idx, mem, output = brainfuck_functions(code, i, idx, mem, output)
        else:
            if code[i] == "[":
                loop.append([])
            elif code[i] == "]":
                if type(loop[-1]) == list:
                    if code[i + 1] == "[":
                        loop.append([])
                    elif code[i + 1] == "]":
                        idx, mem, output = f_loop(loop, code, idx, mem, output)
                        loop = []
                    else:
                        loop.append(code[i + 1])
                    i += 1
                else:
                    idx, mem, output = f_loop(loop, code, idx, mem, output)
                    loop = []
            elif type(loop[-1]) == list:
                    loop[-1].append(code[i])
            else:
                loop.append(code[i])
        i += 1
    print(output)

def brainfuck(filename):
    code = read_file(filename)
    read_brainfuck(code)

brainfuck("helloworld.txt")