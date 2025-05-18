import dis
import marshal
import sys
import types
from typing import List

# Mapping of byte values to emoji and back
byte_to_emoji = {i: chr(0x1F600 + i) for i in range(256)}
emoji_to_byte = {v: k for k, v in byte_to_emoji.items()}


def python_to_bytes(source: str) -> bytes:
    compiled = compile(source, filename="<string>", mode="exec")
    return compiled.co_code


def bytes_to_python(bytecode: bytes) -> types.CodeType:
    dummy = compile('', '<string>', 'exec')

    if sys.version_info >= (3, 11):
        code_obj = types.CodeType(
            dummy.co_argcount,
            dummy.co_posonlyargcount,
            dummy.co_kwonlyargcount,
            dummy.co_nlocals,
            dummy.co_stacksize,
            dummy.co_flags,
            bytecode,
            dummy.co_consts,
            dummy.co_names,
            dummy.co_varnames,
            dummy.co_filename,
            dummy.co_name,
            dummy.co_qualname,
            dummy.co_firstlineno,
            dummy.co_linetable,
            dummy.co_exceptiontable,
            dummy.co_freevars,
            dummy.co_cellvars,
        )
    elif sys.version_info >= (3, 10):
        code_obj = types.CodeType(
            dummy.co_argcount,
            dummy.co_posonlyargcount,
            dummy.co_kwonlyargcount,
            dummy.co_nlocals,
            dummy.co_stacksize,
            dummy.co_flags,
            bytecode,
            dummy.co_consts,
            dummy.co_names,
            dummy.co_varnames,
            dummy.co_filename,
            dummy.co_name,
            dummy.co_firstlineno,
            dummy.co_linetable,
            dummy.co_freevars,
            dummy.co_cellvars,
        )
    else:
        code_obj = types.CodeType(
            dummy.co_argcount,
            dummy.co_posonlyargcount,
            dummy.co_kwonlyargcount,
            dummy.co_nlocals,
            dummy.co_stacksize,
            dummy.co_flags,
            bytecode,
            dummy.co_consts,
            dummy.co_names,
            dummy.co_varnames,
            dummy.co_filename,
            dummy.co_name,
            dummy.co_firstlineno,
            dummy.co_lnotab,
            dummy.co_freevars,
            dummy.co_cellvars,
        )

    return code_obj



def python_to_emojis(source: str) -> str:
    compiled = compile(source, filename="<string>", mode="exec")
    marshaled = marshal.dumps(compiled)  # FULL object, not just bytecode
    emojis = ''.join(byte_to_emoji[b] for b in marshaled)

    # Round-trip verification
    round_trip = bytes(emoji_to_byte[c] for c in emojis)
    if round_trip != marshaled:
        raise ValueError("Emoji round-trip verification failed!")

    return emojis

def emojis_to_python(emojis: str) -> types.CodeType:
    marshaled = bytes(emoji_to_byte[c] for c in emojis)
    code_obj = marshal.loads(marshaled)
    return code_obj


def save_emojis(filepath: str, emojis: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(emojis)

def load_emojis(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()



# Example usage
if __name__ == "__main__":
    python_code = """
def hello(name):
    print(f"Hello, {name}!")

hello("World")
"""

    emoji_output = python_to_emojis(python_code)
    emoji_file = 'hello_emojis.txt'
    save_emojis(emoji_file, emoji_output)

    emoji_input = load_emojis(emoji_file)
    code_obj = emojis_to_python(emoji_input)
    exec(code_obj)
