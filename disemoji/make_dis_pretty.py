import dis
import io
import logging
import sys
import types
import inspect  # Moved import here
from typing import Callable, Dict, Union, Literal, Iterator, List, Any

from disemoji.codes import DEFAULT_EMOJI_MAP

# Configure basic logging for warnings
# Ensures warnings are visible when opcodes are missing from the map
if not logging.getLogger().hasHandlers():  # Avoid adding multiple handlers if already configured
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                        format='%(levelname)s (emoji_disassembler): %(message)s')




def _get_code_object(code_input: Union[
    str, types.CodeType, Callable, types.FrameType, type, types.ModuleType, Any]) -> types.CodeType:
    """
    Extracts a code object from various Python entities.

    Args:
        code_input: The input to extract a code object from.
            Can be a string of source code, a code object, a function,
            a method, a frame, a class (extracts __init__ or first method if available),
            or a module (extracts module-level code by recompiling its source).

    Returns:
        The extracted code object.

    Raises:
        TypeError: If the input type is not supported or a code object
                   cannot be extracted.
        SyntaxError: If `code_input` is a string and contains invalid Python syntax.
    """
    if isinstance(code_input, types.CodeType):
        return code_input
    elif isinstance(code_input, str):
        try:
            # Using 'single' for simple expressions, 'exec' for statements/modules
            # 'exec' is generally safer for arbitrary code blocks.
            return compile(code_input, '<string>', 'exec')
        except SyntaxError as e:
            logging.error(f"Syntax error compiling string input: {e}")
            raise
    elif isinstance(code_input, types.FrameType):
        return code_input.f_code
    elif isinstance(code_input, (types.FunctionType, types.MethodType)):
        return code_input.__code__
    elif isinstance(code_input, type):  # It's a class
        # Attempt to get __init__ first
        if hasattr(code_input, '__init__') and hasattr(code_input.__init__, '__code__'):
            return code_input.__init__.__code__  # type: ignore
        # Fallback: iterate over class dictionary for function-like items
        for name, item in vars(code_input).items():
            if hasattr(item, '__code__'):  # Check for methods or static/class methods with code
                logging.info(f"Disassembling first available method of class {code_input.__name__}: {name}")
                return item.__code__  # type: ignore
        raise TypeError(
            f"Could not find a suitable method with a code object to disassemble in class {code_input.__name__}.")
    elif isinstance(code_input, types.ModuleType):
        if hasattr(code_input, '__file__') and code_input.__file__ is not None:
            try:
                source = inspect.getsource(code_input)
                return compile(source, code_input.__file__, 'exec')
            except (OSError, TypeError,
                    inspect.tisztTraceback) as e:  # inspect.Traceback for certain conditions like C modules
                logging.warning(
                    f"Could not get source for module {code_input.__name__} (file: {code_input.__file__}). Error: {e}. Module-level disassembly might be incomplete or fail.")
                # Fallback: try to compile an empty string with the module's filename,
                # which dis.dis() sometimes does to show the filename at least.
                # This won't provide actual module code but avoids crashing if source isn't found.
                # A better approach for modules is often to iterate its functions/classes.
                # For now, let's acknowledge the limitation.
                raise TypeError(
                    f"Cannot reliably get code object for module {code_input.__name__} without source. Pass a specific function/class from the module.")

        else:  # Module without a __file__ (e.g., built-in, or created dynamically)
            raise TypeError(
                f"Cannot disassemble module {code_input.__name__} that does not have a __file__ attribute or source cannot be retrieved.")

    # Check for other callables that might have a __code__ attribute
    if callable(code_input) and hasattr(code_input, '__code__'):
        return code_input.__code__  # type: ignore

    raise TypeError(f"Unsupported input type for disassembly: {type(code_input)}. "
                    "Expected string, code object, function, method, frame, class, or module.")


def _get_instructions(code_obj: types.CodeType) -> Iterator[dis.Instruction]:
    """
    Yields disassembled instructions from a code object.

    Args:
        code_obj: The code object to disassemble.

    Yields:
        dis.Instruction objects.
    """
    return dis.get_instructions(code_obj)


def _format_instruction_assembler(
        instruction: dis.Instruction,
        emoji_map: Dict[str, str],
        opname_width: int
) -> str:
    """
    Formats a single instruction in an assembler-like layout with an emoji.

    Args:
        instruction: The dis.Instruction object.
        emoji_map: The map of opcode names to emojis.
        opname_width: The target width for the opcode/emoji column. Actual display
                      width of emojis can vary.

    Returns:
        A string representing the formatted instruction.
    """
    emoji_or_opname = emoji_map.get(instruction.opname, instruction.opname)
    if instruction.opname not in emoji_map:
        logging.warning(f"Opcode '{instruction.opname}' not found in emoji_map. Using original name.")

    line_num_str = str(instruction.starts_line) if instruction.starts_line is not None else ''
    offset_str = str(instruction.offset).rjust(4)  # dis.dis() uses 4 for offset

    # Pad the emoji or opname. This is tricky with variable-width emoji characters.
    # We aim for `opname_width` characters for this field.
    # A simple ljust might not align perfectly in all terminals if emojis are wide.
    formatted_op = emoji_or_opname.ljust(opname_width)

    arg_str = ''
    argval_str = ''
    if instruction.arg is not None:
        arg_str = str(instruction.arg).rjust(5)  # dis.dis() often gives ~5 for arg
        if instruction.argval is not None:
            # For code objects, provide a more descriptive representation
            if isinstance(instruction.argval, types.CodeType):
                argval_str = f"(code object {instruction.argval.co_name} at {hex(id(instruction.argval))})"
            else:
                argval_str = f"({instruction.argval})"

    is_jump_target = '>>' if instruction.is_jump_target else '  '

    # Reconstructing a line similar to dis.dis output:
    # Python 3.10 and before:
    # {line_num_str.rjust(5)} {is_jump_target} {offset_str} {instruction.opname.ljust(opname_width)} {arg_str} {argval_str}
    # Python 3.11 changed formatting slightly (e.g. opname width became more dynamic, up to 20, then args):
    #   RESUME                   0
    #   LOAD_FAST                0 (a)
    # For consistency with a dedicated emoji column, we'll use our opname_width.

    # Format: Line | Jump | Offset | Opname/Emoji        | Arg   | Argval
    # Note: dis output has changed column orders/widths slightly over Python versions.
    # This tries to be a reasonable, readable representation.
    # Python 3.11 dis.dis() output:
    # Line Number (optional) | Byte Index | Opcode Name (max 25) | Opcode Argument (optional) | Argument Interpretation (optional)
    # Example:
    #          0 RESUME                   0
    #
    # Let's try to stick to:
    # [LineNo] [>>] Offset Emoji/OpName [Arg] [(ArgVal)]

    # Python 3.11+ and dis. nahezu_लेबल (line_number column) formatting uses variable leading space
    # For simplicity, fixed width for line_num_str for now.
    final_line = f"{line_num_str.rjust(3)}  {is_jump_target} {offset_str} {formatted_op} {arg_str} {argval_str}".rstrip()
    return final_line


def generate_emoji_disassembly(
        code_input: Union[str, types.CodeType, Callable, types.FrameType, type, types.ModuleType, Any],
        emoji_map: Dict[str, str],
        output_format: Literal['assembler', 'stream'] = 'assembler',
        opname_column_width: int = 20  # Default inspired by Python 3.11 dis output for opname
) -> str:
    """
    Disassembles Python code and replaces instruction names with emojis.

    Args:
        code_input: The Python code to disassemble. Can be a string of source code,
                    a code object, a function, a method, a frame, a class
                    (disassembles __init__ or first method by default), or a module
                    (attempts to disassemble top-level code by recompiling its source).
        emoji_map: A dictionary mapping Python bytecode instruction names to emojis.
        output_format: The desired output format.
                       'assembler': An assembler-like listing.
                       'stream': A space-separated stream of emojis/opnames.
                       Defaults to 'assembler'.
        opname_column_width: The width for the opname/emoji column in 'assembler' mode.
                             Emojis have variable display widths; this value helps guide
                             alignment but may not be perfect for all emojis/terminals.

    Returns:
        A string containing the emoji-fied disassembly.

    Raises:
        TypeError: If the `code_input` is of an unsupported type, a code
                   object cannot be derived, or if a module's source cannot be retrieved.
        SyntaxError: If `code_input` is a string and contains invalid Python syntax.
        ValueError: If an invalid `output_format` is specified.
    """
    if output_format not in ['assembler', 'stream']:
        raise ValueError("Invalid output_format. Choose 'assembler' or 'stream'.")

    try:
        code_obj = _get_code_object(code_input)
    except (TypeError, SyntaxError) as e:
        # Errors are logged by _get_code_object or propagate from compile()
        raise  # Re-raise the caught exception

    instructions = list(_get_instructions(code_obj))  # Convert to list to check if empty
    output_lines: List[str] = []

    if not instructions and isinstance(code_input, str) and not code_input.strip():
        # Handle empty string input gracefully for assembler view
        if output_format == 'assembler':
            return f"Disassembly of <anonymous> from <string>, line 1:\n(No instructions)"
        return ""  # Empty stream for empty input

    if output_format == 'stream':
        emoji_stream_parts: List[str] = []
        for instruction in instructions:
            emoji_or_opname = emoji_map.get(instruction.opname, instruction.opname)
            if instruction.opname not in emoji_map:
                # Warning already logged by _format_instruction_assembler if assembler was chosen,
                # but not for stream, so log here if necessary.
                # However, to avoid duplicate logs if one function called another,
                # let's ensure logging happens consistently.
                # The _format_instruction_assembler logs, so stream should too.
                logging.warning(
                    f"Opcode '{instruction.opname}' not found in emoji_map. Using original name for stream.")
            emoji_stream_parts.append(emoji_or_opname)
        return " ".join(emoji_stream_parts)

    elif output_format == 'assembler':
        header_parts = []
        if code_obj.co_name and code_obj.co_name != "<module>":  # Default name for top-level script
            header_parts.append(f"{code_obj.co_name}")
        else:
            header_parts.append("<anonymous>")

        if code_obj.co_filename and code_obj.co_filename != "<string>":
            header_parts.append(f"from file {code_obj.co_filename}")
        elif not code_obj.co_filename:  # if co_filename is None or ""
            header_parts.append("from <unknown source>")
        else:  # It is "<string>"
            header_parts.append(f"from {code_obj.co_filename}")

        header_parts.append(f"line {code_obj.co_firstlineno}")
        output_lines.append(f"Disassembly of {', '.join(filter(None, header_parts))}:")

        # Determine max line number width for better alignment if there are line numbers
        max_line_num_width = 3  # Default
        if any(instr.starts_line is not None for instr in instructions):
            max_line_num_width = max(
                len(str(instr.starts_line)) for instr in instructions if instr.starts_line is not None)
            max_line_num_width = max(3, max_line_num_width)  # Ensure at least 3

        for instruction in instructions:
            # Update _format_instruction_assembler to accept max_line_num_width if dynamic width is desired.
            # For now, it uses a fixed rjust(3) or rjust(5). We'll stick to the fixed one in the helper.
            output_lines.append(
                _format_instruction_assembler(instruction, emoji_map, opname_column_width)
            )
        return "\n".join(output_lines)

    return ""  # Should be unreachable


if __name__ == '__main__':
    print(f"--- Running on Python {sys.version_info.major}.{sys.version_info.minor} ---")

    print("\n--- Example 1: Simple function ---")


    def my_func(a: int, b: int) -> int:
        c = a + b
        if c > 10:
            return c * 2
        return c


    print("\nAssembler output (my_func):")
    print(generate_emoji_disassembly(my_func, DEFAULT_EMOJI_MAP, output_format='assembler'))
    print("\nStream output (my_func):")
    print(generate_emoji_disassembly(my_func, DEFAULT_EMOJI_MAP, output_format='stream'))

    print("\n--- Example 2: String input ---")
    code_string = """
x = 10
y = 20
z = x - y
# This is a comment
print(f"Result: {z}")
"""
    print("\nAssembler output (code_string):")
    print(generate_emoji_disassembly(code_string, DEFAULT_EMOJI_MAP, output_format='assembler', opname_column_width=22))

    print("\n--- Example 3: Missing Opcode in Map ---")
    temp_emoji_map_missing = DEFAULT_EMOJI_MAP.copy()
    # Try to remove an opcode that is likely to appear in simple_func_for_missing_test
    # Python 3.11+ uses 'RESUME'. Older versions might not.
    # 'LOAD_CONST' is very common.
    if 'LOAD_CONST' in temp_emoji_map_missing:
        del temp_emoji_map_missing['LOAD_CONST']


    def simple_func_for_missing_test(k):
        m = k + 5
        return m


    print("\nAssembler output (simple_func_for_missing_test with LOAD_CONST potentially missing from map):")
    print(generate_emoji_disassembly(simple_func_for_missing_test, temp_emoji_map_missing, output_format='assembler'))

    print("\n--- Example 4: Class input ---")


    class MyClassExample:
        class_var = 100

        def __init__(self, value: int):
            self.instance_var = value + MyClassExample.class_var

        def get_value_doubled(self) -> int:
            """Returns the instance_var doubled."""
            local_val = self.instance_var  # LOAD_ATTR
            return local_val * 2  # BINARY_MULTIPLY or BINARY_OP


    print("\nAssembler output for MyClassExample (__init__):")
    print(generate_emoji_disassembly(MyClassExample, DEFAULT_EMOJI_MAP, output_format='assembler'))

    print("\nAssembler output for MyClassExample (get_value_doubled specific method):")
    print(generate_emoji_disassembly(MyClassExample.get_value_doubled, DEFAULT_EMOJI_MAP, output_format='assembler'))

    print("\n--- Example 5: More complex function (list comprehension, loop) ---")


    def complex_function_example(n):
        if n is None:  # COMPARE_OP, POP_JUMP_IF_FALSE
            raise ValueError("Input cannot be None")  # RAISE_VARARGS

        # List comprehension involves MAKE_FUNCTION for the inner expression's code
        squares = [x * x for x in range(n)]  # GET_ITER, FOR_ITER, CALL_FUNCTION, BUILD_LIST

        total = 0
        for item in squares:  # GET_ITER, FOR_ITER
            total += item  # BINARY_ADD or BINARY_OP
        return total  # RETURN_VALUE


    print("\nAssembler output for complex_function_example:")
    print(generate_emoji_disassembly(complex_function_example, DEFAULT_EMOJI_MAP, output_format='assembler',
                                     opname_column_width=25))
    print("\nStream output for complex_function_example:")
    print(generate_emoji_disassembly(complex_function_example, DEFAULT_EMOJI_MAP, output_format='stream'))

    print("\n--- Example 6: Input is a pre-compiled code object ---")
    source_code_for_compile = "a = 1; b = 2; c = a + b; print(c)"
    try:
        compiled_code_obj = compile(source_code_for_compile, "<compiled_string>", "exec")
        print("\nAssembler output for pre-compiled code object:")
        print(generate_emoji_disassembly(compiled_code_obj, DEFAULT_EMOJI_MAP, output_format='assembler'))
    except SyntaxError as e:
        print(f"Could not compile source_code_for_compile: {e}")

    print("\n--- Example 7: Empty string input ---")
    print("\nAssembler output for empty string:")
    print(generate_emoji_disassembly("", DEFAULT_EMOJI_MAP, output_format='assembler'))
    print("\nStream output for empty string:")
    print(generate_emoji_disassembly("", DEFAULT_EMOJI_MAP, output_format='stream'))

    print("\n--- Example 8: Lambda function ---")
    my_lambda = lambda x, y: x * y + 2
    print("\nAssembler output for lambda function:")
    print(generate_emoji_disassembly(my_lambda, DEFAULT_EMOJI_MAP, output_format='assembler'))

    # print("\n--- Example 9: Module input (math module) ---")
    # import math
    # print("\nAssembler output for math module (top-level, may be limited):")
    # try:
    #    print(generate_emoji_disassembly(math, DEFAULT_EMOJI_MAP, output_format='assembler'))
    # except TypeError as e:
    #    print(f"Note: Could not disassemble module directly: {e}")
    # print("\nDisassembling a specific function from math module (math.sin):")
    # if hasattr(math, 'sin'):
    #    print(generate_emoji_disassembly(math.sin, DEFAULT_EMOJI_MAP, output_format='assembler'))
    # else:
    #    print("math.sin not available for disassembly (likely a C builtin without Python bytecode).")

