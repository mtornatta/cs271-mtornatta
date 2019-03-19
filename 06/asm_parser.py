#asm_parser.py by Michael Tornatta
#cs271 Yong Bakos
#March 2019

class asm_parser:

    def __init__(self):
        self.comp = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101" }

        self.dest = {
        "null": "000",
        "M": "001",
        "D": "010",
        "A": "100",
        "MD": "011",
        "AM": "101",
        "AD": "110",
        "AMD": "111" }

        self.jump ={
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111" }

        self.predef = {
        "SP" : "000000000000000",
        "LCL" : "000000000000001",
        "ARG" : "000000000000010",
        "THIS" : "000000000000011",
        "THAT" : "000000000000100",
        "R0" : "000000000000000",
        "R1" : "000000000000001",
        "R2" : "000000000000010",
        "R3" : "000000000000011",
        "R4" : "000000000000100",
        "R5" : "000000000000101",
        "R6" : "000000000000110",
        "R7" : "000000000000111",
        "R8" : "000000000001000",
        "R9" : "000000000001001",
        "R10" : "000000000001010",
        "R11" : "000000000001011",
        "R12" : "000000000001100",
        "R13" : "000000000001101",
        "R14" : "000000000001110",
        "R15" : "000000000001111",
        "SCREEN" : "100000000000000",
        "KBD" : "110000000000000" }

        self.symbols = {}
        self.labels = {}
        self.label_counter = 16

    def assemble(self, file_name):
        #Get the filename for output hack file
        filename_split = file_name.split(".")
        filename_split.remove("asm")
        output_filename = filename_split[0]
        output_filename = output_filename + "michaelt.hack"

        return self.instruction_handler(self.trimmed_asm(file_name),output_filename)

    #Takes in a text file and returns a list with all asm instructions with no space or comments
    def trimmed_asm(self, trim_file):
        asm_code = []
        asm_file = open(trim_file,'r')

        for line in asm_file:
            if line != "" and line[0] != '/' and line[0] != '\n':
                #Deal with after text comments
                if "/" in line:
                    line = line.split("/")
                    line = line[0]

                asm_code.append(line.strip())


        return asm_code

    def instruction_handler(self, trimmed_asm, output_filename):
        #Create output file
        output_file = open(output_filename, "w")
        output_file.close()
        binary_log = []
        line_number = 0

        #First Pass to collect symbols
        for line in trimmed_asm:
            if line[0] == '(':
                line = line.replace('(','')
                line = line.replace(')','')
                self.symbols[line] = '{0:015b}'.format(int(line_number))
                line_number = line_number - 1
            line_number = line_number + 1

        #Open output file to append to
        output_file = open(output_filename, "a")

        #Second Pass
        for instruction in trimmed_asm:
            binary = ""
            if instruction[0] == '@':
                binary = binary + "0"
                binary = binary + self.handle_a_instruction(instruction,trimmed_asm)
            elif instruction[0] != '@':
                binary = binary + "111"
                binary = binary + self.handle_c_instruction(instruction)

            #Only write non (Symbol) codes
            #Symbols will show up as just a "111"
            if len(binary) >= 16:
                output_file.write(binary)
                output_file.write("\n")

        return output_file

    def handle_a_instruction(self,instruction,trimmed_asm):
        #Get rid of @ symbol
        instruction = instruction.replace('@','')
        binary = ""
        if instruction in self.predef:
            binary = binary + self.predef[instruction]
        elif self.check_if_float(instruction) == True:
            binary = binary + '{0:015b}'.format(int(instruction))
        elif self.check_if_float(instruction) == False:
            binary = self.handle_l_instruction(instruction,trimmed_asm)

        return binary

    def handle_c_instruction(self,instruction):
        binary = ""

        if "=" in instruction:
            split_instruction = instruction.split("=")
            if split_instruction[1] in self.comp:
                binary = binary + self.comp[split_instruction[1]]
            if split_instruction[0] in self.dest:
                binary = binary + self.dest[split_instruction[0]]

            binary = binary + "000"

        elif ";" in instruction:
            split_instruction = instruction.split(";")

            if str(split_instruction[0]) in self.comp:
                binary = binary + self.comp[split_instruction[0]]
            binary = binary + "000"
            if split_instruction[1] in self.jump:
                binary = binary + self.jump[split_instruction[1]]

        return binary

    def handle_l_instruction(self,instruction,trimmed_asm):
        #Get rid of @ symbol
        instruction = instruction.replace('@','')
        binary = ""

        if instruction in self.predef:
            binary = binary + self.predef[instruction]
        elif instruction in self.symbols:
            binary = binary + self.symbols[instruction]
        elif instruction not in self.symbols:
            if instruction in self.labels:
                binary = binary + self.labels[instruction]
            if instruction not in self.labels:
                self.labels[instruction] = '{0:015b}'.format(int(self.label_counter))
                binary = binary + '{0:015b}'.format(int(self.label_counter))
                self.label_counter = self.label_counter + 1

        return binary

    def check_if_float(self, test_value):
        try:
            float(test_value)
            return True
        except ValueError:
            return False

    def line_break(self, variable):
        print(variable)
        if input() == "exit":
            exit()
