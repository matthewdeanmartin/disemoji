from typing import Optional, Set, Callable, Any, Dict, List
import sys
import dis
import inspect
from contextlib import contextmanager
from dataclasses import dataclass, field

from disemoji.codes import DEFAULT_EMOJI_MAP
from disemoji.ui import emoji_print


@dataclass
class BytecodeTracer:
    traced_functions: Set[str] = field(default_factory=set)
    _disassembled_instructions_cache: Dict[int, List[dis.Instruction]] = field(default_factory=dict)
    _printed_headers: Set[int] = field(default_factory=set)
    _last_printed_lines: Dict[int, int] = field(default_factory=dict)

    def trace_function(self, func_name: str):
        """Register a function to be traced."""
        self.traced_functions.add(func_name)
        return self

    @contextmanager
    def activate(self):
        """
        Context manager for tracing that automatically
        manages state entry and exit.
        """
        try:
            # Save the original trace function
            original_trace = sys.gettrace()

            # Set our custom tracer
            sys.settrace(self._tracer)

            yield self

        finally:
            # Restore original trace function
            sys.settrace(original_trace)

            # Clear internal state
            self._disassembled_instructions_cache.clear()
            self._printed_headers.clear()
            self._last_printed_lines.clear()

    def _tracer(self, frame, event, arg):
        """
        Comprehensive bytecode tracing logic.
        Full opcode tracing mechanism.
        """
        func_name = frame.f_code.co_name

        # Selective tracing based on function name
        should_trace_detail = func_name in self.traced_functions

        if should_trace_detail:
            frame.f_trace_opcodes = True

        if event == 'opcode' and should_trace_detail:
            code = frame.f_code
            code_id = id(code)
            current_bytecode_offset = frame.f_lasti

            # Print full disassembly once per function
            if code_id not in self._printed_headers:
                emoji_print(f"\n--- Disassembly for: {func_name} ({code.co_filename}, line {code.co_firstlineno}) ---")

                # Retrieve or cache disassembled instructions
                if code_id not in self._disassembled_instructions_cache:
                    self._disassembled_instructions_cache[code_id] = list(dis.Bytecode(code))

                all_instrs = self._disassembled_instructions_cache[code_id]

                for instr in all_instrs:
                    starts_line_str = f" " if instr.starts_line else "/"
                    emoji_op_name = DEFAULT_EMOJI_MAP.get(instr.opname)
                    emoji_print(f"{starts_line_str} {instr.offset:3d}: {emoji_op_name} {instr.argrepr}")

                emoji_print(f"--- End Disassembly for {func_name} ---\n")
                emoji_print(f"--- Execution Trace for {func_name} (File: {code.co_filename}) ---")

                self._printed_headers.add(code_id)
                self._last_printed_lines.pop(code_id, None)

            # Display current source line if changed
            current_source_lineno = frame.f_lineno

            if self._last_printed_lines.get(code_id) != current_source_lineno:
                try:
                    source_lines, start_line = inspect.getsourcelines(code)
                    line_index = current_source_lineno - start_line
                    if 0 <= line_index < len(source_lines):
                        source_line_text = source_lines[line_index].rstrip()
                        emoji_print(f"\nLn.{current_source_lineno:3d} {source_line_text}")
                        self._last_printed_lines[code_id] = current_source_lineno
                except (OSError, TypeError):
                    # Handle cases where source can't be retrieved
                    pass

            # Find and print current bytecode instruction
            all_instructions = self._disassembled_instructions_cache[code_id]
            current_instruction = next(
                (instr for instr in all_instructions if instr.offset == current_bytecode_offset),
                None
            )

            if current_instruction:
                emoji_op_name = DEFAULT_EMOJI_MAP.get(current_instruction.opname)
                emoji_print(
                    f"   {current_instruction.offset:3d}: {emoji_op_name} {current_instruction.argrepr}"
                )
            else:
                emoji_print(f"  --> Error: Could not find instruction at offset {current_bytecode_offset} in {func_name}.")

        return self._tracer


# Example usage
def test_tracer():
    tracer = BytecodeTracer()

    def sample_function(x, y):
        result = x + y
        print(f"Result: {result}")
        return result


    with tracer.trace_function('sample_function').activate():
        sample_function(3, 4)

if __name__ == "__main__":
    test_tracer()
