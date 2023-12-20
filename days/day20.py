import copy
import sys
from collections import defaultdict
from enum import Enum
from queue import Queue

from aocd import get_data, submit

DAY = 20
YEAR = 2023

class Type(Enum):
    BROADCAST = 0
    FLIPFLOP = 1
    CONJUNCTION = 2
    BUTTON = 3
    OUTPUT = 4


class Module:
    def __init__(self, name: str, type: Type) -> None:
        self.name = name
        self.type = type
        self.inputs = []
        self.outputs = []
        self.memory = None
        self.pulsed_low = False
        self.pulsed_high = False

    def __repr__(self) -> str:
        return f"{self.name} {self.type} {self.inputs} {self.outputs}"


def parse(data: str) -> dict[str, Module]:
    modules = {"button": Module("button", Type.BUTTON)}
    for line in data.splitlines():
        module_info, outputs = line.split("->")
        module_type = module_info[0]
        module_name = module_info[1:].strip()
        if module_type == "%":
            module = Module(module_name, Type.FLIPFLOP)
        elif module_type == "&":
            module = Module(module_name, Type.CONJUNCTION)
        elif module_type + module_name == "broadcaster":
            module_name = "broadcaster"
            module = Module("broadcaster", Type.BROADCAST)
        else:
            raise ValueError
        module.outputs = [output.strip() for output in outputs.split(",") if output.strip()]
        modules[module_name] = module
    for module in copy.copy(modules).values():
        for output in module.outputs:
            if output not in modules:
                modules[output] = Module(output, Type.OUTPUT)
            modules[output].inputs.append(module.name)
    for module in modules.values():
        if module.type == Type.FLIPFLOP:
            module.memory = False
        elif module.type == Type.CONJUNCTION:
            module.memory = {input: False for input in module.inputs}
        elif module.type == Type.OUTPUT:
            module.memory = False
    return modules


def part1(data: str) -> str:
    modules = parse(data)
    total = {True: 0, False: 0}
    for step in range(1000):
        pulses = push(modules)
        total[True] += pulses[True]
        total[False] += pulses[False]
    res = total[True] * total[False]
    return str(res)


def push(modules: dict[str, Module]) -> dict[bool, int]:
    pulse_queue = Queue()
    pulse_queue.put(("button", "broadcaster", False))
    pulses = {True: 0, False: 0}
    while not pulse_queue.empty():
        source_name, module_name, pulse = pulse_queue.get()
        pulses[pulse] += 1
        module = modules[module_name]
        if module.type == Type.BROADCAST:
            for output in module.outputs:
                pulse_queue.put((module_name, output, pulse))
        elif module.type == Type.FLIPFLOP:
            if not pulse:
                module.memory = not module.memory
                for output in module.outputs:
                    pulse_queue.put((module_name, output, module.memory))
        elif module.type == Type.CONJUNCTION:
            module.memory[source_name] = pulse
            new_pulse = not all(module.memory.values())
            for output in module.outputs:
                pulse_queue.put((module_name, output, new_pulse))
            if not new_pulse:
                module.pulsed_low = True
            else:
                module.pulsed_high = True
        elif module.type == Type.OUTPUT:
            if not pulse:
                module.memory = True
    return pulses


def part2(data: str) -> str:
    modules = parse(data)
    output_module = [module for module in modules.values() if module.type == Type.OUTPUT][0]
    conjunction_highs = defaultdict(list)
    steps = 0
    while True:
        steps += 1
        push(modules)
        for module in modules.values():
            if module.type == Type.CONJUNCTION and module.pulsed_high:
                conjunction_highs[module.name].append(steps)
                module.pulsed_high = False
        res = 1
        if steps % 20000 == 0:
            for name, highs in conjunction_highs.items():
                if len(highs) < 1000:
                    # all relevant conjunctions are on a cycle, the solution is the lcm.
                    # turns out the cycle lenghts are prime, so the lcm is just the product.
                    res *= highs[0]
            break

    return str(res)


if __name__ == '__main__':
    sys.setrecursionlimit(1_000_000)
    input_data = get_data(day=DAY, year=YEAR)
    ans1 = part1(input_data)
    print(ans1)
    # submit(answer=ans1, day=DAY, year=YEAR, part=1)
    ans2 = part2(input_data)
    print(ans2)
    # submit(answer=ans2, day=DAY, year=YEAR, part=2)
