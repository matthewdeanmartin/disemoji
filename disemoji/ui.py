from typing import Dict, Optional

def emoji_print(text: str) -> str:
    """
    Replaces characters in a string with corresponding emojis if a 1:1 mapping exists.
    Leaves emojis and unknown characters unchanged.

    Args:
        text: The input string.

    Returns:
        The string with characters replaced by emojis where possible.
    """
    emoji_map: Dict[str, str] = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣',
        '#': '#️⃣', '*': '*️⃣',
         #
        'a': '🅐', 'b': '🅑', 'c': '🅒', 'd': '🅓', 'e': '🅔',
        'f': '🅕', 'g': '🅖', 'h': '🅗', 'i': '🅘', 'j': '🅙',
        'k': '🅚', 'l': '🅛', 'm': '🅜', 'n': '🅝', 'o': '🅞',
        'p': '🅟', 'q': '🅠', 'r': '🅡', 's': '🅢', 't': '🅣',
        'u': '🅤', 'v': '🅥', 'w': '🅦', 'x': '🅧', 'y': '🅨',
        'z': '🅩',
        'A': '🅐', 'B': '🅑', 'C': '🅒', 'D': '🅓', 'E': '🅔',
        'F': '🅕', 'G': '🅖', 'H': '🅗', 'I': '🅘', 'J': '🅙',
        'K': '🅚', 'L': '🅛', 'M': '🅜', 'N': '🅝', 'O': '🅞',
        'P': '🅟', 'Q': '🅠', 'R': '🅡', 'S': '🅢', 'T': '🅣',
        'U': '🅤', 'V': '🅥', 'W': '🅦', 'X': '🅧', 'Y': '🅨',
        'Z': '🅩',
        '!': '❗', '?': '❓',
        ' ': '⬛'
    }
    result = ""
    for char in text:
        if char in emoji_map:
            result += emoji_map[char]
        else:
            result += char
    print(result)
    return result

if __name__ == '__main__':
    test_string1 = "Hello 123!"
    emoji_string1 = emoji_print(test_string1)
    print(f"Original: {test_string1}")
    print(f"Emoji:    {emoji_string1}")

    test_string2 = "abc#xyz*09?"
    emoji_string2 = emoji_print(test_string2)
    print(f"\nOriginal: {test_string2}")
    print(f"Emoji:    {emoji_string2}")

    test_string3 = "This has some emojis already ➡️ and some unknown $"
    emoji_string3 = emoji_print(test_string3)
    print(f"\nOriginal: {test_string3}")
    print(f"Emoji:    {emoji_string3}")