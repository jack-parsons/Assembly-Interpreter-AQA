

from string import whitespace

REGISTERS = 13
MEMSIZE = 20


class Interpreter:

    def __init__(self, filename="triangle numbers.txt"):
        self.opcodes = {
            "LDR": self.ldr,
            "STR": self.sto,
            "ADD": self.add,
            "SUB": self.sub,
            "MOV": self.mov,
            "CMP": self.cmp,
            "B": self.branch,
            "AND": self.and_,
            "ORR": self.orr,
            "EOR": self.eor,
            "MVN": self.mvn,
            "LSL": self.lsl,
            "LSR": self.lsr,
            "HALT": self.halt
        }
        self.code = self.ld_code(filename)
        self.regs = [0 for _ in range(REGISTERS)]
        self.mem = [0 for _ in range(MEMSIZE)]
        self.current_line = 0
        self.cmp_sto = (0, 0)
        self.labels = {}
        self.current_op = None
        self.current_operands = []

    def ld_code(self, filename):
        with open(filename, "r") as f:
            return f.readlines()

    def get_reg_num(self, r):
        try:
            if r[0] == "R":
                return int(r[1:])
            else:
                raise Exception
        except:
            raise SyntaxError("Invalid register op, line %i" % self.current_line)

    def reg_set(self, r, val):
        self.regs[r] = val

    def get_mem_val(self, ref):
        ref = self.get_val(ref)
        if 0 <= ref < MEMSIZE:
            return self.mem[ref]
        else:
            raise MemoryError("Reference out of bounds")

    def set_mem_val(self, ref, val):
        ref = self.get_val(ref)
        if 0 <= ref < MEMSIZE:
            self.mem[ref] = val
        else:
            raise MemoryError("Reference out of bounds")

    def get_val(self, op):
        try:
            if op[0] == "#":
                return int(op[1:])
            elif op[0] == "R":
                return self.regs[int(op[1:])]
            else:
                raise SyntaxError("Invalid operand, line %i")
        except:
            raise SyntaxError("Invalid operand, line %i")

    def get_label_pos(self, label):
        return self.labels[label]

    def ldr(self, rd, memref):
        """LDR Rd, <memory ref>     Load the value stored in the memory location specified by 
        <memory ref> into register d."""
        self.regs[self.get_reg_num(rd)] = self.get_mem_val(memref)

    def sto(self, rd, memref):
        """STR Rd, <memory ref>     Store the value that is in register d 
        into the memory location specified by <memory ref>"""
        self.set_mem_val(memref, self.regs[self.get_reg_num(rd)])

    def add(self, rd, rn, op2):
        """ADD Rd, Rn, <operand2>   Add the value specified in <operand2> 
        to the value in register n and store the result in register d"""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn)+self.get_val(op2))

    def sub(self, rd, rn, op2):
        """SUB Rd, Rn, <operand2>   Subtract the value specified by <operand2> from the value 
        in register n and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn)-self.get_val(op2))

    def mov(self, rd, op2):
        """MOV Rd, <operand2>   Copy the value specified by <operand2> into register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(op2))

    def cmp(self, rn, op2):
        """CMP Rn, <operand2>   Compare the value stored in register n with the value specified by <operand2>."""
        self.cmp_sto = (self.get_val(rn), self.get_val(op2))

    def branch(self, label, op2 = None):
        """B <label>    Always branch to the instruction at position <label> in the program."""
        if op2 == "EQ" and self.cmp_sto[0] == self.cmp_sto[1]:
            self.current_line = self.get_label_pos(label)
        if op2 == "NE" and self.cmp_sto[0] != self.cmp_sto[1]:
            self.current_line = self.get_label_pos(label)
        if op2 == "LT" and self.cmp_sto[0] < self.cmp_sto[1]:
            self.current_line = self.get_label_pos(label)
        if op2 == "GT" and self.cmp_sto[0] > self.cmp_sto[1]:
            self.current_line = self.get_label_pos(label)
        if op2 is None:
            self.current_line = self.get_label_pos(label)

    def and_(self, rd, rn, op2):
        """AND Rd, Rn, <operand2>   Perform a bitwise logical AND operation between the value in register n
         and the value specified by <operand2> and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn) & self.get_val(op2))

    def orr(self, rd, rn, op2):
        """AND Rd, Rn, <operand2>   Perform a bitwise logical AND operation between the value in register n
         and the value specified by <operand2> and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn) | self.get_val(op2))

    def eor(self, rd, rn, op2):
        """EOR Rd, Rn, <operand2>   Perform a bitwise logical XOR (exclusive or) operation between the value
         in register n and the value specified by <operand2> and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn) ^ self.get_val(op2))

    def mvn(self, rd, rn):
        """MVN Rd, <operand2>   Perform a bitwise logical NOT operation on the value specified by <operand2>
         and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), ~self.get_val(rn))

    def lsl(self, rd, rn, op2):
        """LSL Rd, Rn, <operand2>   Logically shift left the value stored in register n
         by the number of bits specified by <operand2> and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn) << self.get_val(op2))

    def lsr(self, rd, rn, op2):
        """LSR Rd, Rn, <operand2>   Logically shift right the value stored in register n by the number of bits specified by <operand2> and store the result in register d."""
        self.reg_set(self.get_reg_num(rd), self.get_val(rn) >> self.get_val(op2))

    def halt(self):
        """HALT     Stops the execution of the program."""
        self.current_line = -1

    def exec_line(self, opcode, *operands):
        self.opcodes[opcode](*operands)

    def print_memory(self):
        print("memory:\t\t" + "\t".join("[%i]%i" % (n, g) for n, g in enumerate(self.mem)))

    def print_regs(self):
        print("registers: \t" + "\t".join("[R%i]%i" % (n, g) for n, g in enumerate(self.regs)))

    def print_instr(self):
        print("line:", self.current_line, "\top:", self.current_op, "\toperands:", self.current_operands)

    def run(self):
        while 0 <= self.current_line < len(self.code):
            line = self.code[self.current_line]
            self.current_line += 1
            line = line.strip(whitespace)
            if ":" in line:
                self.labels[line[:line.index(":")]] = self.current_line
            elif len(line) > 0:
                split_line = line.split()
                if line[0] == line[1] == "/":
                    pass
                elif split_line[0][0] == "B":
                    self.current_op, *self.current_operands = split_line
                    self.print_instr()
                    self.print_regs()
                    self.print_memory()
                    self.exec_line("B", split_line[1], split_line[0][1:])
                elif split_line[0] in self.opcodes:
                    self.exec_line(*split_line)
                    self.current_op, *self.current_operands = split_line
                    self.print_instr()
                    self.print_regs()
                    self.print_memory()
                else:
                    raise SyntaxError("Invalid op code line: %i"%self.current_line)
                print()


if __name__ == '__main__':
    Interpreter(input("Enter file name: ")).run()
