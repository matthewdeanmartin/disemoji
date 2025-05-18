import dis
import marshal
import types
from typing import List

# Mapping of bytecode instructions to emojis
emoji_map = {
    'NOP': '⚪',
    'POP_TOP': '🔝',
    'ROT_TWO': '🔄',
    'ROT_THREE': '🔄3️⃣',
    'DUP_TOP': '👯',
    'DUP_TOP_TWO': '👯2️⃣',
    'UNARY_POSITIVE': '➕',
    'UNARY_NEGATIVE': '➖',
    'UNARY_NOT': '❗',
    'UNARY_INVERT': '🔄',
    'BINARY_MATRIX_MULTIPLY': '✖️',
    'BINARY_POWER': '🔋',
    'BINARY_MULTIPLY': '✖️',
    'BINARY_MODULO': '➗',
    'BINARY_ADD': '➕',
    'BINARY_SUBTRACT': '➖',
    'BINARY_SUBSCR': '📌',
    'BINARY_FLOOR_DIVIDE': '➗',
    'BINARY_TRUE_DIVIDE': '➗',
    'BINARY_LSHIFT': '⬅️',
    'BINARY_RSHIFT': '➡️',
    'BINARY_AND': '🔀',
    'BINARY_XOR': '🔀',
    'BINARY_OR': '🔀',
    'INPLACE_POWER': '🔋',
    'INPLACE_MULTIPLY': '✖️',
    'INPLACE_MODULO': '➗',
    'INPLACE_ADD': '➕',
    'INPLACE_SUBTRACT': '➖',
    'INPLACE_LSHIFT': '⬅️',
    'INPLACE_RSHIFT': '➡️',
    'INPLACE_AND': '🔀',
    'INPLACE_XOR': '🔀',
    'INPLACE_OR': '🔀',
    'STORE_SUBSCR': '📤📌',
    'DELETE_SUBSCR': '❌📌',
    'GET_ITER': '🔄',
    'FOR_ITER': '🔄',
    'STORE_MAP': '📤🗺️',
    'LOAD_CONST': '🔢',
    'LOAD_NAME': '🔠',
    'BUILD_TUPLE': '🔗',
    'BUILD_LIST': '📋',
    'BUILD_SET': '🗂️',
    'BUILD_MAP': '📚',
    'LOAD_ATTR': '🔗',
    'COMPARE_OP': '⚖️',
    'IMPORT_NAME': '📥🔠',
    'IMPORT_FROM': '📥➡️',
    'JUMP_FORWARD': '➡️➡️',
    'POP_JUMP_IF_TRUE': '🔝❗',
    'POP_JUMP_IF_FALSE': '🔝❗',
    'JUMP_IF_TRUE_OR_POP': '➡️❗🔝',
    'JUMP_IF_FALSE_OR_POP': '➡️❗🔝',
    'JUMP_ABSOLUTE': '➡️➡️',
    # 'POP_TOP': '🔝',
    'LOAD_GLOBAL': '🌍🔠',
    'SETUP_FINALLY': '🛡️',
    'LOAD_FAST': '🚄🔠',
    'STORE_FAST': '🚄📤',
    'DELETE_FAST': '🚄❌',
    'RAISE_VARARGS': '⚠️',
    'CALL_FUNCTION': '📞',
    'MAKE_FUNCTION': '🔧',
    'BUILD_SLICE': '🔪',
    'LOAD_CLOSURE': '🔒',
    'LOAD_DEREF': '🔑',
    'STORE_DEREF': '🔑📤',
    'DELETE_DEREF': '🔑❌',
    'RETURN_VALUE': '🔙',
    'YIELD_VALUE': '⚙️',
    'YIELD_FROM': '⚙️',
    'SETUP_ANNOTATIONS': '📝',
    'IMPORT_STAR': '📥🌟',
    'POP_BLOCK': '🔝❌',
    'END_FINALLY': '🔚🛡️',
    'POP_EXCEPT': '🔝⚠️❌',
    'STORE_NAME': '🔠📤',
    'DELETE_NAME': '🔠❌',
    'UNPACK_SEQUENCE': '📦📜',
    'UNPACK_EX': '📦📜❗',
    'STORE_ATTR': '🔗📤',
    'DELETE_ATTR': '🔗❌',

    'RESUME':'',
    'PUSH_NULL':'',
    'CALL':'',
    'RETURN_CONST': '',
}

# Reverse mapping from emoji to opcode name
emoji_to_opcode: dict[str, str] = {v: k for k, v in emoji_map.items()}


def disassemble_to_emoji(code: str) -> str:
    bytecode = dis.Bytecode(code)
    emoji_output: List[str] = []
    for instr in bytecode:
        emoji = emoji_map.get(instr.opname)
        if emoji is None:
            raise ValueError(f"Opcode {instr.opname} not mapped to emoji!")
        emoji_output.append(emoji)
    return ' '.join(emoji_output)  # SPACE SEPARATED

def execute_emojis(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as f:
        emoji_code = f.read().strip()

    emoji_list = emoji_code.split()  # Now split by spaces

    opnames: List[str] = []
    for emoji in emoji_list:
        opname = emoji_to_opcode.get(emoji)
        if opname is None:
            raise ValueError(f"Unknown emoji: {emoji}")
        opnames.append(opname)

    # For now: Dummy execution
    def dummy_func() -> None:
        print("Hello from dummy function!")

    print("Executing dummy function due to emoji mapping limitation:")
    dummy_func()

# def execute_emojis(file_path: str) -> None:
#     with open(file_path, 'r', encoding='utf-8') as f:
#         emoji_code = f.read().strip()
#
#     # Convert emoji code back to opcode names
#     opnames: List[str] = []
#     buffer = ''
#     for char in emoji_code:
#         buffer += char
#         if buffer in emoji_to_opcode:
#             opnames.append(emoji_to_opcode[buffer])
#             buffer = ''
#
#     if buffer:
#         raise ValueError(f"Unrecognized emoji sequence: {buffer}")

    # # Now, for demo purposes, create a fake function
    # # In real bytecode, we'd need arguments (operands) and offsets
    # # Here we'll create a simple function returning None
    # def dummy_func() -> None:
    #     print("Hello from dummy function!")
    #
    # print("Executing dummy function due to emoji mapping limitation:")
    # dummy_func()


# Example usage
if __name__ == "__main__":
    python_code = """
def hello(name):
    print(f"Hello, {name}!")

hello("World")
    """
    emojis = disassemble_to_emoji(python_code)
    print("Emoji Bytecode Representation:")
    print(emojis)

    # Write emojis to a file
    emoji_file = 'hello_emojis_pretty.txt'
    with open(emoji_file, 'w', encoding='utf-8') as f:
        f.write(emojis)

    # Read emojis from file and execute
    execute_emojis(emoji_file)