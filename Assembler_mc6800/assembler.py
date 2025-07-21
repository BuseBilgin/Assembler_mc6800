import re
from opcodes_full import OPCODES

class AssemblerError(Exception):
    pass

class Instruction:
    def __init__(self, label, mnemonic, operand, line):
        self.label = label
        self.mnemonic = mnemonic.upper()
        self.operand = operand
        self.line = line
        self.address = None
        self.opcode = None
        self.operand_value = []

class Assembler:
    def __init__(self):
        self.instructions = []
        self.symbol_table = {}
        self.machine_code = []
        self.listing = []
        self.current_address = 0x0000

        self.memory = [0x00] * 256
        self.registers = {
            "A": 0x00,
            "B": 0x00,
            "X": 0x0000,
            "SP": 0x00FF
        }

    def parse_line(self, line):
        line = line.split(";")[0].strip()
        if not line:
            return None
        match = re.match(r"(?:(\w+):)?\s*(\w+)(?:\s+(.*))?", line)
        if not match:
            raise AssemblerError(f"Hatalı sözdizimi: {line}")
        label, mnemonic, operand = match.groups()
        return Instruction(label, mnemonic, operand, line)

    def parse_code(self, code):
        self.instructions = []
        for line in code.splitlines():
            instr = self.parse_line(line)
            if instr:
                self.instructions.append(instr)

    def first_pass(self):
        addr = self.current_address
        for instr in self.instructions:
            if instr.mnemonic == "ORG":
                addr = int(instr.operand.replace("$", "0x"), 16)
                self.current_address = addr
                continue
            if instr.label:
                if instr.label in self.symbol_table:
                    raise AssemblerError(f"Çift tanımlı etiket: {instr.label}")
                self.symbol_table[instr.label] = addr
            instr.address = addr
            if instr.mnemonic == "BYTE":
                addr += 1
            elif instr.mnemonic in ("EQU", "END"):
                continue
            elif instr.mnemonic in OPCODES or instr.mnemonic.startswith("B"):
                addr += 2 if instr.operand else 1
            else:
                addr += 2
        self.current_address = addr

    def second_pass(self):
        self.machine_code = []
        self.listing = []
        for instr in self.instructions:
            if instr.mnemonic == "ORG":
                self.current_address = int(instr.operand.replace("$", "0x"), 16)
                continue
            elif instr.mnemonic == "END":
                break
            elif instr.mnemonic == "EQU":
                self.symbol_table[instr.label] = int(instr.operand.replace("$", "0x"), 16)
                continue
            elif instr.mnemonic == "BYTE":
                val = int(instr.operand.replace("$", "0x"), 16)
                self.machine_code.append(val)
                self.memory[self.current_address] = val
                self.listing.append((instr.line, opcode, operand, instr.address))
                self.current_address += 1
                continue
            else:
                key = instr.mnemonic
                operand = instr.operand
                val = None

                if operand:
                    if operand in self.symbol_table:
                        addr = self.symbol_table[operand]
                        if key in ["BRA", "BEQ", "BNE", "BMI", "BPL", "BCS", "BCC", "BVS", "BVC", "BRN"]:
                            offset = addr - (instr.address + 2)
                            if not -128 <= offset <= 127:
                                raise AssemblerError(f"Offset taşması: {key} {operand}")
                            val = offset & 0xFF
                        else:
                            key += "_EXT" if addr > 0xFF else "_DIR"
                            val = addr
                    elif operand.startswith("#"):
                        key += "_IMM"
                        val = int(operand.replace("#", "").replace("$", "0x"), 16)
                    elif operand.endswith(",X"):
                        key += "_IDX"
                        part = operand.replace(",X", "").strip()
                        val = 0 if not part else int(part.replace("$", "0x"), 16)
                    elif operand.startswith("$"):
                        v = int(operand.replace("$", "0x"), 16)
                        key += "_DIR" if v <= 0xFF else "_EXT"
                        val = v
                    else:
                        raise AssemblerError(f"Operand çözülemedi: {operand}")

                if key not in OPCODES:
                    raise AssemblerError(f"Geçersiz komut: {key}")

                opcode = OPCODES[key]
                self.machine_code.append(opcode)
                self.memory[self.current_address] = opcode
                self.current_address += 1
                if val is not None:
                    if "_EXT" in key:
                        self.machine_code.append((val >> 8) & 0xFF)
                        self.machine_code.append(val & 0xFF)
                        self.memory[self.current_address] = (val >> 8) & 0xFF
                        self.memory[self.current_address + 1] = val & 0xFF
                        self.current_address += 2
                    else:
                        self.machine_code.append(val & 0xFF)
                        self.memory[self.current_address] = val & 0xFF
                        self.current_address += 1

                self.execute_instruction(key, val)
                self.listing.append((instr.line, opcode, operand, instr.address))

    def execute_instruction(self, mnemonic, operand):
        if mnemonic.startswith("LDAA"):
            if "_IMM" in mnemonic and operand is not None:
                self.registers["A"] = operand
            elif "_DIR" in mnemonic and operand is not None:
                self.registers["A"] = self.memory[operand]
        elif mnemonic.startswith("LDAB"):
            if "_IMM" in mnemonic and operand is not None:
                self.registers["B"] = operand
            elif "_DIR" in mnemonic and operand is not None:
                self.registers["B"] = self.memory[operand]
        elif mnemonic.startswith("LDX"):
            if "_IMM" in mnemonic and operand is not None:
                self.registers["X"] = operand
            elif "_DIR" in mnemonic and operand is not None:
                self.registers["X"] = (self.memory[operand] << 8) | self.memory[operand + 1]
        elif mnemonic.startswith("STAA"):
            if "_DIR" in mnemonic and operand is not None:
                self.memory[operand] = self.registers["A"]
            elif "_IDX" in mnemonic and operand is not None:
                addr = (self.registers["X"] + operand) & 0xFFFF
                self.memory[addr] = self.registers["A"]
        elif mnemonic.startswith("ADDA"):
            if "_IMM" in mnemonic and operand is not None:
                self.registers["A"] = (self.registers["A"] + operand) & 0xFF
            elif "_DIR" in mnemonic and operand is not None:
                self.registers["A"] = (self.registers["A"] + self.memory[operand]) & 0xFF
        elif mnemonic == "PSHA":
            sp = self.registers["SP"]
            self.memory[sp] = self.registers["A"]
            self.registers["SP"] = (sp - 1) & 0xFF
        elif mnemonic == "PULA":
            self.registers["SP"] = (self.registers["SP"] + 1) & 0xFF
            sp = self.registers["SP"]
            self.registers["A"] = self.memory[sp]
        elif mnemonic == "PSHB":
            sp = self.registers["SP"]
            self.memory[sp] = self.registers["B"]
            self.registers["SP"] = (sp - 1) & 0xFF
        elif mnemonic == "PULB":
            self.registers["SP"] = (self.registers["SP"] + 1) & 0xFF
            sp = self.registers["SP"]
            self.registers["B"] = self.memory[sp]

    def assemble(self, code):
        self.parse_code(code)
        self.first_pass()
        self.second_pass()
        return self.machine_code

    def write_lst(self, filename="output.lst"):
        with open(filename, "w") as f:
            for line, opcode, operand, addr in self.listing:
                if opcode is not None:
                    f.write(f"{addr:04X} {line:30} ; {opcode:02X} {operand if operand else ''}\n")
                else:
                    f.write(f"{addr:04X} {line:30} ; {operand}\n")

    def write_obj(self, filename="output.obj"):
        with open(filename, "wb") as f:
            f.write(bytes(self.machine_code))
