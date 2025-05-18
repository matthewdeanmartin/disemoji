import dis

# --- Helper to get all opcodes for the current Python version ---
# This will help us identify any missing opcodes.
# We'll manually add opcodes from other versions if they are common or important.
current_opnames = [op for op in dis.opname if '<' not in op and op != 'EXTENDED_ARG']

# --- Initial Merged and Enhanced Map ---
# We'll start by merging your two lists, making some choices,
# and then fill in the rest.

DEFAULT_EMOJI_MAP = {
    # --- Opcodes from your lists (merged and selected) ---
    'NOP': '⚪',  # No operation - a white circle, neutral.
    'POP_TOP': '🔝🗑️',  # Pop top of stack and discard - top arrow with a trash can.
    'ROT_TWO': '🔄🥈',  # Rotate top two stack items - rotate with a silver medal for two.
    'ROT_THREE': '🔄🥉',  # Rotate top three stack items - rotate with a bronze medal for three.
    'ROT_FOUR': '🔄🏅', # Rotate top four stack items - rotate with a generic medal. (Added)
    'DUP_TOP': '👯',  # Duplicate top of stack - "twins" or dancers.
    'DUP_TOP_TWO': '👯👯',  # Duplicate top two stack items - two pairs of "twins".

    # Unary Operations
    'UNARY_POSITIVE': '➕✨',  # Implements +obj - plus with a sparkle for unary.
    'UNARY_NEGATIVE': '➖✨',  # Implements -obj - minus with a sparkle for unary.
    'UNARY_NOT': '❗✨',  # Implements not obj - exclamation mark with a sparkle.
    'UNARY_INVERT': '🌀',  # Implements ~obj - a spiral for bitwise inversion.

    # Binary Operations (Python 3.10 and earlier)
    'BINARY_POWER': '🔋',  # Implements TOS1 ** TOS - battery for power.
    'BINARY_MULTIPLY': '✖️',  # Implements TOS1 * TOS - multiply sign.
    'BINARY_MODULO': '٪',  # Implements TOS1 % TOS - modulo sign.
    'BINARY_ADD': '➕',  # Implements TOS1 + TOS - plus sign.
    'BINARY_SUBTRACT': '➖',  # Implements TOS1 - TOS - minus sign.
    'BINARY_SUBSCR': '📑🔖',  # Implements TOS1[TOS] - document with a bookmark for subscripting.
    'BINARY_FLOOR_DIVIDE': ' sàn➗',  # Implements TOS1 // TOS - floor division. (Using "sàn" as a visual for floor)
    'BINARY_TRUE_DIVIDE': '➗',  # Implements TOS1 / TOS - division sign.
    'BINARY_LSHIFT': '⏪',  # Implements TOS1 << TOS - fast reverse for left shift.
    'BINARY_RSHIFT': '⏩',  # Implements TOS1 >> TOS - fast forward for right shift.
    'BINARY_AND': 'AND',  # Implements TOS1 & TOS - "AND" gate symbol (using text as emoji is hard).
    'BINARY_XOR': 'XOR',  # Implements TOS1 ^ TOS - "XOR" gate symbol.
    'BINARY_OR': 'OR',   # Implements TOS1 | TOS - "OR" gate symbol.

    # In-place Operations
    'INPLACE_POWER': '🔋⚡',  # Implements TOS1 **= TOS - battery with lightning for in-place.
    'INPLACE_MULTIPLY': '✖️⚡',  # Implements TOS1 *= TOS - multiply with lightning.
    'INPLACE_MODULO': '٪⚡',  # Implements TOS1 %= TOS - modulo with lightning.
    'INPLACE_ADD': '➕⚡',  # Implements TOS1 += TOS - plus with lightning.
    'INPLACE_SUBTRACT': '➖⚡',  # Implements TOS1 -= TOS - minus with lightning.
    'INPLACE_FLOOR_DIVIDE': ' sàn➗⚡', # Implements TOS1 //= TOS - floor divide with lightning.
    'INPLACE_TRUE_DIVIDE': '➗⚡',  # Implements TOS1 /= TOS - divide with lightning.
    'INPLACE_LSHIFT': '⏪⚡',  # Implements TOS1 <<= TOS - left shift with lightning.
    'INPLACE_RSHIFT': '⏩⚡',  # Implements TOS1 >>= TOS - right shift with lightning.
    'INPLACE_AND': 'AND⚡',  # Implements TOS1 &= TOS - AND with lightning.
    'INPLACE_XOR': 'XOR⚡',  # Implements TOS1 ^= TOS - XOR with lightning.
    'INPLACE_OR': 'OR⚡',   # Implements TOS1 |= TOS - OR with lightning.

    # Python 3.11+ Binary Operations (Supersedes many above)
    'BINARY_OP': '⚙️➕➖✖️➗', # Binary operation (generic for 3.11+) - gear with common ops.

    # Stack manipulation / Calls
    'PUSH_NULL': '🚫➡️', # Pushes a NULL to the stack for function calls (Python 3.11+) - null symbol then arrow.

    # Iteration
    'GET_ITER': '🚶🔄',  # Implements TOS = iter(TOS) - person walking to start iteration.
    'FOR_ITER': '🔁🏷️',  # Pops iterator, calls next. Pushes next or jumps if exhausted. Loop with a label.
    'YIELD_VALUE': '🎁🔚',  # Pops TOS and yields it from a generator - gift then end (of current execution slice).
    'YIELD_FROM': '🎁🎁🔚', # Pops TOS (an iterator) and delegates to it - multiple gifts.

    # Structure building
    'BUILD_TUPLE': '📜',  # Builds a tuple from stack items - a scroll (immutable).
    'BUILD_LIST': '📝',  # Builds a list from stack items - a memo/notepad (mutable).
    'BUILD_SET': '🧩',  # Builds a set from stack items - puzzle pieces (unique items).
    'BUILD_MAP': '🗺️',  # Builds a dictionary from stack items - a map (key-value).
    'BUILD_CONST_KEY_MAP': '🗺️🔑', # Builds a dict from const keys and stack values - map with a key.
    'BUILD_STRING': '✍️',  # Concatenates strings from stack - writing hand.
    'BUILD_SLICE': '🔪',  # Implements TOS2:TOS1:TOS or TOS1:TOS or TOS - a knife for slicing.

    # Load Operations
    'LOAD_CONST': '🧱',  # Pushes a constant - a brick, a fundamental building block.
    'LOAD_NAME': '📦🏷️',  # Pushes value of namei - box with a name label.
    'LOAD_GLOBAL': '🌍🏷️',  # Pushes value of global namei - globe with a name label.
    'LOAD_FAST': '💨📦',  # Pushes value of local variable - fast/dash with a box.
    'LOAD_CLOSURE': '🔗📦⏳', # Pushes a reference to a cell (closure) - link, box, hourglass (for deferred access).
    'LOAD_DEREF': '🔗🔑📦', # Pushes value from a cell (dereferenced) - link, key, box.
    'LOAD_CLASSDEREF': '🏛️🔑📦', # Like LOAD_DEREF but for class scope - building, key, box.
    'LOAD_ATTR': '🏷️.',  # Implements TOS.namei - name label with a dot for attribute access.
    'LOAD_METHOD': '📞🏷️.', # Loads a method (Python 3.7+) - phone with attribute access. (Replaced LOAD_ATTR for methods)

    # Store Operations
    'STORE_NAME': '🏷️💾',  # Stores TOS as namei - name label with a save/disk icon.
    'STORE_GLOBAL': '🌍💾',  # Stores TOS as global namei - globe with a save icon.
    'STORE_FAST': '💨💾',  # Stores TOS as local variable - fast/dash with a save icon.
    'STORE_DEREF': '🔗🔑💾', # Stores TOS into a cell variable - link, key, save.
    'STORE_ATTR': '💾.',  # Implements TOS1.namei = TOS - save icon with a dot.
    'STORE_SUBSCR': '📑✏️', # Implements TOS1[TOS] = TOS2 - document with a pencil for writing to subscript.
    'STORE_MAP': '🗺️➕', # Store a key-value pair in a map (old, pre 3.5 for **kwargs) - map with plus.

    # Delete Operations
    'DELETE_NAME': '🏷️🗑️',  # Deletes namei - name label with a trash can.
    'DELETE_GLOBAL': '🌍🗑️',  # Deletes global namei - globe with a trash can.
    'DELETE_FAST': '💨🗑️',  # Deletes local variable - fast/dash with a trash can.
    'DELETE_DEREF': '🔗🔑🗑️', # Deletes a cell variable - link, key, trash.
    'DELETE_ATTR': '🗑️.',  # Implements del TOS.namei - trash icon with a dot.
    'DELETE_SUBSCR': '📑🗑️', # Implements del TOS1[TOS] - document with a trash can.

    # Function/Method Calls
    'CALL_FUNCTION': '📞🗣️',  # Calls a function (pre 3.11) - phone, speaking head. (Often has arg count)
    'CALL_FUNCTION_KW': '📞🔑🗣️', # Calls function with keyword args (pre 3.11) - phone, key, speaking head.
    'CALL_FUNCTION_EX': '📞📦🗣️', # Calls function with *args, **kwargs (pre 3.11) - phone, box, speaking head.
    'CALL_METHOD': '📞🏷️🗣️', # Calls a method (pre 3.11) - phone, label, speaking head. (Replaced by CALL for 3.11+)
    'CALL': '📞',          # Calls a callable (Python 3.11+) - simple phone.
    'PRECALL': '➡️📞',      # Performs pre-call checks (Python 3.11+) - arrow to phone.
    'KW_NAMES': '🔑🏷️📜',   # Stores keyword argument names (Python 3.6+) - key, label, scroll.

    # Making Functions/Classes
    'MAKE_FUNCTION': '🧑‍🍳📜',  # Creates a new function object - chef with a recipe/scroll.
    'MAKE_CELL': '🔗⚙️', # Creates a new cell object (for closures) - link and gear. (Python 3.8+)
    'SETUP_ANNOTATIONS': '📝🧐', # Sets up __annotations__ dict - memo with a monocle for inspection. (Python 3.6+)

    # Importing
    'IMPORT_NAME': '📥🌍',  # Imports a module - inbox tray with a globe.
    'IMPORT_FROM': '📥🏷️',  # Imports an attribute from a module - inbox tray with a label.
    'IMPORT_STAR': '📥✨',  # Implements from module import * - inbox tray with a star.

    # Jumps
    'JUMP_FORWARD': '➡️',  # Unconditional jump forward - right arrow.
    'JUMP_ABSOLUTE': '🎯➡️', # Unconditional jump to target - target with right arrow. (Often used for loops, pre 3.10 replaced by JUMP_BACKWARD)
    'JUMP_BACKWARD': '⬅️', # Unconditional jump backward (Python 3.10+) - left arrow.
    'JUMP_BACKWARD_NO_INTERRUPT': '⬅️🚫🔔', # JUMP_BACKWARD that doesn't trigger signal checks (3.11+) - left arrow, no bell.


    # Conditional Jumps (Pre 3.11 had POP_JUMP_IF_TRUE/FALSE)
    # Python 3.11+ introduced FORWARD/BACKWARD variants
    'POP_JUMP_IF_TRUE': '⤵️✅', # Pop, if true, jump - down arrow with checkmark. (Pre 3.11)
    'POP_JUMP_IF_FALSE': '⤵️❌', # Pop, if false, jump - down arrow with cross mark. (Pre 3.11)
    'POP_JUMP_FORWARD_IF_TRUE': '⤵️✅➡️', # Pop, if true, jump forward (3.11+) - down arrow, check, right arrow.
    'POP_JUMP_FORWARD_IF_FALSE': '⤵️❌➡️', # Pop, if false, jump forward (3.11+) - down arrow, cross, right arrow.
    'POP_JUMP_BACKWARD_IF_TRUE': '⤵️✅⬅️', # Pop, if true, jump backward (3.11+) - down arrow, check, left arrow.
    'POP_JUMP_BACKWARD_IF_FALSE': '⤵️❌⬅️', # Pop, if false, jump backward (3.11+) - down arrow, cross, left arrow.
    'POP_JUMP_FORWARD_IF_NONE': '⤵️👻➡️', # Pop, if None, jump forward (3.11. beta) - down, ghost, right.
    'POP_JUMP_BACKWARD_IF_NONE': '⤵️👻⬅️',# Pop, if None, jump backward (3.11. beta) - down, ghost, left.
    'POP_JUMP_FORWARD_IF_NOT_NONE': '⤵️🚫👻➡️', # Pop, if not None, jump forward (3.11. beta) - down, no ghost, right.
    'POP_JUMP_BACKWARD_IF_NOT_NONE': '⤵️🚫👻⬅️',# Pop, if not None, jump backward (3.11. beta) - down, no ghost, left.


    'JUMP_IF_TRUE_OR_POP': '➡️✅🗑️', # If true, jump, else pop - arrow, check, or trash.
    'JUMP_IF_FALSE_OR_POP': '➡️❌🗑️', # If false, jump, else pop - arrow, cross, or trash.

    # Comparisons
    'COMPARE_OP': '⚖️',  # Performs a comparison - scales of justice.
    'CONTAINS_OP': '🔍IN', # Implements 'in' and 'not in' - magnifying glass with "IN".
    'IS_OP': '🆔❓', # Implements 'is' and 'is not' - ID card with question mark.

    # Exceptions and Blocks
    'POP_BLOCK': '🧱⬇️',  # Remove a block from the block stack - brick falling down.
    'RAISE_VARARGS': '💥📢',  # Raises an exception - explosion with a loudspeaker.
    'SETUP_FINALLY': '🛡️🏁',  # Sets up a try-finally block - shield for protection, finish line for finally.
    'SETUP_WITH': '🤝🛡️', # Sets up a with block - handshake for context manager, shield for protection.
    'WITH_EXCEPT_START': '🤝💔🔍', # Calls __exit__ for `with` block, prepares for exception handling (3.9+) - handshake, broken heart, search.
    'POP_EXCEPT': '🤕🗑️',  # Pops an exception handler block - injured face, trash can.
    'END_FINALLY': '🏁✅', # Terminates a finally clause (old, pre 3.8) - finish line, check. (Replaced by RERAISE or jump)
    'RERAISE': '💥🔁', # Re-raises an exception (Python 3.9+) - explosion, repeat.
    'SETUP_ASYNC_WITH': '🤝⏳🛡️', # Sets up an async with block (3.5+) - handshake, hourglass, shield.
    'BEFORE_ASYNC_WITH': '▶️⏳🤝', # Before an async with block (3.8+) - play, hourglass, handshake.
    'GET_AWAITABLE': '⏳👀', # Gets an awaitable for `await` (3.5+) - hourglass, eyes.
    'GET_AITER': '🚶🔄⏳', # Gets an async iterator for `async for` (3.5+) - walking, loop, hourglass.
    'GET_ANEXT': '⏭️⏳', # Gets next item from async iterator (3.5+) - next track, hourglass.
    'END_ASYNC_FOR': '🏁🔚⏳', # Terminates an async for loop (3.8+) - finish line, end, hourglass.

    # Coroutine/Generator related (Python 3.11+)
    'RESUME': '▶️📜', # Resumes a generator or coroutine (Python 3.11+) - play button, scroll (for state).
    'RETURN_GENERATOR': '🎁🧑‍🍳🏁', # Returns a new generator object from a function (3.11+) - gift, chef, finish.
    'SEND': '📨🎁', # Sends a value into a generator (3.11+) - incoming envelope, gift.

    # Return Opcodes
    'RETURN_VALUE': '🏁🎁',  # Returns with TOS to caller - finish line with a gift/value.
    'RETURN_CONST': '🏁🧱', # Returns a constant value (Python 3.12+) - finish line with a brick.

    # Miscellaneous
    'FORMAT_VALUE': '📝✨',  # Formats a value for f-strings - memo with sparkles.
    'UNPACK_SEQUENCE': '📦➡️📜',  # Unpacks a sequence into individual stack items - box arrow to scroll (multiple items).
    'UNPACK_EX': '📦✨➡️📜',  # Unpacks sequence with a *target - box with sparkle to scroll.
    'LOAD_BUILD_CLASS': '🏗️🏛️', # Pushes builtins.__build_class__ - crane and classical building.
    'COPY_FREE_VARS': '🔗📝©️', # Copies free variables to closure (3.11+) - link, memo, copyright.

    # --- Opcodes that might be less common or very specific versions ---
    'EXTENDED_ARG': '➕➕', # Prefix for opcodes taking an argument > 65535 (or >255 pre 3.6) - extra pluses.
                               # This is technically not an instruction executed on its own.
    'CACHE': ' C ',          # Placeholder for adaptive specializations (internal, Python 3.11+) - "C" for Cache.
    'LOAD_ASSERTION_ERROR': '❗😱🧱', # Pushes AssertionError (Python 3.5+) - exclamation, shocked face, brick (for error object).
    'LIST_TO_TUPLE': '📝➡️📜', # Converts a list to a tuple (Python 3.9+) - memo to scroll.
    'LIST_EXTEND': '📝➕➕', # Extends a list (Python 3.9+) - memo, double plus.
    'SET_UPDATE': '🧩➕➕', # Updates a set (Python 3.9+) - puzzle, double plus.
    'DICT_UPDATE': '🗺️➕➕', # Updates a dict (Python 3.9+) - map, double plus.
    'DICT_MERGE': '🗺️🤝🗺️', # Merges dicts (Python 3.9+, for ** merging) - map, handshake, map.
    'GET_LEN': '📏', # Pushes len(TOS) (Python 3.10+) - ruler.
    'MATCH_MAPPING': '🗺️❓', # Part of match statement (Python 3.10+) - map, question mark.
    'MATCH_SEQUENCE': '📜❓', # Part of match statement (Python 3.10+) - scroll, question mark.
    'MATCH_KEYS': '🔑❓', # Part of match statement (Python 3.10+) - key, question mark.
    'MATCH_CLASS': '🏛️❓', # Part of match statement (Python 3.10+) - building, question mark.
    'PRINT_EXPR': '💬📄', # Prints expression in interactive mode - speech bubble, page.
    'LOAD_METHOD_CACHED': '📞🏷️. C', # (3.12+ internal) - Call method with cache.
    'LOAD_ATTR_CACHED': '🏷️. C', # (3.12+ internal) - Load attribute with cache.
    'SEND_GEN': '📨🎁💨', # (Old, pre 3.11) Send value into generator.

    # Python 3.12 specific experimental opcodes (may change/disappear)
    # Generally, these are for specialization/inlining
    'LOAD_FAST_LOAD_FAST': '💨📦💨📦', # Load two fast locals
    'STORE_FAST_LOAD_FAST': '💨💾💨📦',# Store then load fast local
    'STORE_FAST_STORE_FAST': '💨💾💨💾',# Store two fast locals
    'LOAD_FAST_AND_CLEAR': '💨📦🧹', # Load local and clear it from stack (for list comps)
    'LOAD_SUPER_ATTR': '🦸‍♂️🏷️.', # Load attribute from super() (3.12+)

    # Python 3.13+ (Speculative based on trends or very new features)
    'CLEANUP_THROW': '🧹💥🔚', # (3.13+) related to `defer` or new exception handling.
    'PUSH_EXC_INFO': '🤕➡️', # (3.13+) Push exception info for new except* handling.
    'CHECK_EXC_MATCH': '🤕❓✅', # (3.13+) Check if exception matches for except*.
    'CHECK_EG_MATCH': '🤕⚡❓✅', # (3.13+) Check exception group match for except*.

    'BEFORE_WITH': '▶️🤝',  # Before a `with` block's __enter__ call (Python 3.11+) - play button, handshake.
    'BINARY_SLICE': '🔪[::]',
    # Implements TOS2 = TOS1[TOS:TOS3] (Python 3.13, replaces BUILD_SLICE + BINARY_SUBSCR in some cases) - knife, slice notation.
    'END_FOR': '🏁➡️🔚',
    # Cleans up after a `for` loop when iterator is exhausted (Python 3.12+) - finish, right arrow (jump over loop body), end. (Replaces parts of FOR_ITER)
    'END_SEND': '🏁📨🔚',
    # Cleans up when sending a value into a generator (Python 3.12+) - finish, incoming envelope, end.
    'EXIT_INIT_CHECK': '🚪✅❓',
    # Check after __init__ if an exception occurred (Python 3.13, for `defer`) - door, check, question.
    'FORMAT_SIMPLE': '✍️📄',  # Simple f-string formatting (no spec) (Python 3.12+) - writing, page.
    'FORMAT_WITH_SPEC': '✍️📄⚙️',
    # F-string formatting with a format spec (Python 3.12+) - writing, page, gear (for spec processing).
    'RESERVED': '🔒🚫',  # Reserved for internal use, should not be encountered - lock, prohibition sign.
    'GET_YIELD_FROM_ITER': '🚶🔄🎁',
    # Implements `iter(TOS)` for `yield from` (pre 3.5, now usually GET_ITER) - walk, loop, gift.
    'INTERPRETER_EXIT': '🚪🛑',  # Signals the interpreter to exit (Python 3.13+) - door, stop sign.
    'LOAD_LOCALS': '🏠📦',  # Pushes the `locals()` dictionary (Python 3.12+) - house (local scope), box.
    'STORE_SLICE': '💾[::]',
    # Implements TOS1[TOS:TOS3] = TOS4 (Python 3.13, replaces BUILD_SLICE + STORE_SUBSCR) - save, slice notation.
    'TO_BOOL': '➡️️️🇧',  # Converts TOS to a boolean (Python 3.11+) - arrow, B (for Boolean).
    'CALL_INTRINSIC_1': '⚙️📞➡️1️⃣',
    # Calls an internal, fast function with one argument (Python 3.12+) - gear, call, arrow, one.
    'CALL_INTRINSIC_2': '⚙️📞➡️2️⃣',
    # Calls an internal, fast function with two arguments (Python 3.13+) - gear, call, arrow, two.
    'CALL_KW': '📞🔑🗣️⚡',
    # Calls function with keyword args (Python 3.13, matches old CALL_FUNCTION_KW, maybe specialized) - phone, key, speaking head.
    'CONVERT_VALUE': '🔄✨📄',
    # Perform ``!s``, ``!r``, or ``!a`` conversion in f-strings (Python 3.12+) -🔄✨📄 - conversion, sparkle, page.
    'COPY': '©️➡️',  # Copies the Nth item from top of stack to top (Python 3.11+) - copyright (copy), arrow.
    'ENTER_EXECUTOR': '⚡🏃💨',
    # Enters an executor (for JIT compilation, Python 3.13+) - lightning, running person, dash.
    'LIST_APPEND': '📝➕',  # Appends TOS to list at TOS1 (Python 3.9+) - memo (list), plus.
    'LOAD_FAST_CHECK': '💨📦✅',  # Loads a local variable, checking it's initialized (Python 3.6+) - fast, box, check.
    'LOAD_FROM_DICT_OR_DEREF': '🗺️/🔗📦',  # Load from locals dict or dereference cell (Python 3.11+) - map or link, box.
    'LOAD_FROM_DICT_OR_GLOBALS': '🗺️/🌍📦',  # Load from locals dict or globals (Python 3.11+) - map or globe, box.
    'MAP_ADD': '🗺️➕📌',
    # Adds TOS1:TOS to dict at TOS2 (Python 3.8+, for dict comprehensions) - map, plus, pin (for key/value).
    'POP_JUMP_IF_NONE': '⤵️👻❓',
    # Pop, if None, jump (Python 3.11+) - down arrow, ghost (None), question. (Supersedes POP_JUMP_FORWARD/BACKWARD_IF_NONE)
    'POP_JUMP_IF_NOT_NONE': '⤵️🚫👻❓',
    # Pop, if not None, jump (Python 3.11+) - down arrow, no ghost, question. (Supersedes POP_JUMP_FORWARD/BACKWARD_IF_NOT_NONE)
    'SET_ADD': '🧩➕',  # Adds TOS to set at TOS1 (Python 3.8+) - puzzle (set), plus.
    'SET_FUNCTION_ATTRIBUTE': '🧑‍🍳🏷️✏️',
    # Set an attribute on a function object (e.g. __defaults__, __kwdefaults__) (Python 3.x) - chef, label, pencil.
    'SWAP': '↔️',  # Swaps the Nth item with TOS (Python 3.11+) - left-right arrow.

    # Instrumented Opcodes (Python 3.12+ PEP 669) - Using 🩺 (stethoscope) for "instrumented"
    'INSTRUMENTED_RESUME': '🩺▶️📜',  # Instrumented version of RESUME.
    'INSTRUMENTED_END_FOR': '🩺🏁➡️🔚',  # Instrumented version of END_FOR.
    'INSTRUMENTED_END_SEND': '🩺🏁📨🔚',  # Instrumented version of END_SEND.
    'INSTRUMENTED_RETURN_VALUE': '🩺🏁🎁',  # Instrumented version of RETURN_VALUE.
    'INSTRUMENTED_RETURN_CONST': '🩺🏁🧱',  # Instrumented version of RETURN_CONST.
    'INSTRUMENTED_YIELD_VALUE': '🩺🎁🔚',  # Instrumented version of YIELD_VALUE.
    'INSTRUMENTED_LOAD_SUPER_ATTR': '🩺🦸‍♂️🏷️.',  # Instrumented version of LOAD_SUPER_ATTR.
    'INSTRUMENTED_FOR_ITER': '🩺🔁🏷️',  # Instrumented version of FOR_ITER.
    'INSTRUMENTED_CALL': '🩺📞',  # Instrumented version of CALL.
    'INSTRUMENTED_CALL_KW': '🩺📞🔑🗣️⚡',  # Instrumented version of CALL_KW (or old CALL_FUNCTION_KW).
    'INSTRUMENTED_CALL_FUNCTION_EX': '🩺📞📦🗣️',  # Instrumented version of CALL_FUNCTION_EX.
    'INSTRUMENTED_INSTRUCTION': '🩺🔩',  # Generic instrumented instruction marker.
    'INSTRUMENTED_JUMP_FORWARD': '🩺➡️',  # Instrumented version of JUMP_FORWARD.
    'INSTRUMENTED_JUMP_BACKWARD': '🩺⬅️',  # Instrumented version of JUMP_BACKWARD.
    'INSTRUMENTED_POP_JUMP_IF_TRUE': '🩺⤵️✅',  # Instrumented version of POP_JUMP_IF_TRUE variants.
    'INSTRUMENTED_POP_JUMP_IF_FALSE': '🩺⤵️❌',  # Instrumented version of POP_JUMP_IF_FALSE variants.
    'INSTRUMENTED_POP_JUMP_IF_NONE': '🩺⤵️👻❓',  # Instrumented version of POP_JUMP_IF_NONE.
    'INSTRUMENTED_POP_JUMP_IF_NOT_NONE': '🩺⤵️🚫👻❓',  # Instrumented version of POP_JUMP_IF_NOT_NONE.
    'INSTRUMENTED_LINE': '🩺📏#️⃣',  # Indicates a line number event for instrumentation. Stethoscope, ruler, number sign.

    'JUMP': '↪️',
    # Unconditional jump (Python 3.13+, generic, replaces JUMP_FORWARD/ABSOLUTE/BACKWARD) - generic jump arrow.
    'JUMP_NO_INTERRUPT': '↪️🚫🔔',  # Unconditional jump, no interrupt check (Python 3.13+) - jump arrow, no bell.
    'LOAD_SUPER_METHOD': '🦸‍♂️📞🏷️',
    # Loads method from super() (Python 3.12+, for `super().meth`) - superman, phone, label.
    'LOAD_ZERO_SUPER_ATTR': '🦸‍♂️0️⃣🏷️.',
    # Loads attribute from super() with no args (Python 3.12+) - superman, zero, label, dot.
    'LOAD_ZERO_SUPER_METHOD': '🦸‍♂️0️⃣📞🏷️',
    # Loads method from super() with no args (Python 3.12+) - superman, zero, phone, label.
    'SETUP_CLEANUP': '🧹🛡️',  # Sets up a try-except/finally for cleanup (Python 3.13+, for `defer`) - broom, shield.
    'STORE_FAST_MAYBE_NULL': '💨💾👻❓',
    # Store to a fast local that might not be initialized (internal, Python 3.13+) - fast, save, ghost, question.



}

# --- Fill in any missing opcodes from the current Python version ---
# This is more for completeness if running this script, the above list should be fairly comprehensive
# for common Python versions (3.8-3.12).
# For opcodes that are purely internal or pseudo-instructions like CACHE or EXTENDED_ARG,
# a simple representation is usually fine.

missing_opcodes_emojis = {
    # Example of how you might add one if `current_opnames` found something new:
    # 'A_NEW_OPCODE': '✨🆕✨', # A newly discovered opcode - sparkles, new, sparkles.
}

# Add any opcodes specific to the current Python version that aren't in the main map
for op_name in current_opnames:
    if op_name not in DEFAULT_EMOJI_MAP and op_name not in ['EXTENDED_ARG', 'CACHE']: # We handle these separately
        if op_name in missing_opcodes_emojis:
            DEFAULT_EMOJI_MAP[op_name] = missing_opcodes_emojis[op_name]
        else:
            # A generic placeholder if we encounter something truly unexpected
            DEFAULT_EMOJI_MAP[op_name] = '❓🔧' # Question mark and wrench for "unknown/needs work"
            print(f"Warning: Opcode '{op_name}' is in current Python version but not in the emoji map. Added generic emoji.")

# Ensure EXTENDED_ARG and CACHE are present if in opmap, as they are special
if 'EXTENDED_ARG' in dis.opmap and 'EXTENDED_ARG' not in DEFAULT_EMOJI_MAP:
    DEFAULT_EMOJI_MAP['EXTENDED_ARG'] = '➕➕'
if 'CACHE' in dis.opmap and 'CACHE' not in DEFAULT_EMOJI_MAP:
    DEFAULT_EMOJI_MAP['CACHE'] = ' C '


# --- You can then use this map ---
if __name__ == '__main__':
    # please find the dupe values in DEFAULT_EMOJI_MAP and print them
    for key, value in DEFAULT_EMOJI_MAP.items():
        if list(DEFAULT_EMOJI_MAP.values()).count(value) > 1:
            for k, v in DEFAULT_EMOJI_MAP.items():
                if v == value and k != key:
                    print(f"Duplicate emoji '{value}' for opcodes '{key}' and '{k}'")
                    break
            print(f"Missing emoji for opcode '{key}'")

    # Example:
    import dis
    def my_func(a, b):
      return a + b

    for instruction in dis.get_instructions(my_func):
      emoji = DEFAULT_EMOJI_MAP.get(instruction.opname, '❓')
      print(f"{emoji}  {instruction.opname:<25} {instruction.argval if instruction.argval is not None else ''}")

    # Print the generated map (optional)
    for op, emj in sorted(DEFAULT_EMOJI_MAP.items()):
       print(f"'{op}': '{emj}',")
