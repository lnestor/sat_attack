if __name__ == "__main__":
    filename = "benchmarks/c1335-RN320/c1355-RN320.v"

    key_string = ""
    with open(filename) as f:
        for line in f.readlines():
            if "KeyGate" in line:
                tokens = line.split()

                key_bit = False
                if tokens[0] == "xor":
                    key_bit = False
                elif tokens[0] == "xnor":
                    key_bit = True
                else:
                    print("Invalid key gate " + tokens[0])

                if "NOT" in tokens[1]:
                    key_bit = not key_bit

                if key_bit:
                    key_string += "1"
                else:
                    key_string += "0"

    print(key_string)
    print(len(key_string))
