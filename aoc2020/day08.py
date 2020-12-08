from aoc2020.computer import Machine

with open("day08.txt") as f_in:
    ins = [_.strip() for _ in f_in]


def run_until_loops(machine):
    trace, accu = [], None
    while len(set(trace)) == len(trace):
        trace.append(machine.reg['pc'])
        accu = machine.reg['acc']
        machine.step()
    return accu


def main():
    machine = Machine.load(ins)
    print(f"Result 1: {run_until_loops(machine)}")

    for pos, line in enumerate(ins):
        if "jmp" not in line and "nop" not in line:
            continue
        new_ins = ins[::]
        if "jmp" in new_ins[pos]:
            new_ins[pos] = new_ins[pos].replace("jmp", "nop")
        else:
            new_ins[pos] = new_ins[pos].replace("nop", "jmp")

        machine = Machine.load(new_ins)
        try:
            run_until_loops(machine)
        except EOFError:
            print(f"Result 2: {machine.reg['acc']}")
            break


main()
