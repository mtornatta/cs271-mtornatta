#assembler.py by Michael Tornatta
#cs271 Yong Bakos
#March 2019

from asm_parser import asm_parser

parser = asm_parser()

print('Hi There, input file name')
parser.assemble(file_name = input())
print('.hack file created')
