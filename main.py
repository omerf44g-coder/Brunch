import itertools
import os
import argparse
import sys

try:
    from tqdm import tqdm
except ImportError:
    print("[-] Missing library: 'tqdm'. Please install it by running: pip install tqdm")
    sys.exit(1)


def print_banner():
    banner = """
    ██████╗ ██████╗ ██╗   ██╗██████╗ ███╗   ██╗ ██████╗██╗  ██╗
    ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██║  ██║
    ██████╔╝██████╔╝██║   ██║██║  ██║██╔██╗ ██║██║     ███████║
    ██╔══██╗██╔══██╗██║   ██║██║  ██║██║╚██╗██║██║     ██╔══██║
    ██████╔╝██║  ██║╚██████╔╝██║  ██║██║ ╚████║╚██████╗██║  ██║
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
    """
    print(banner)
    print("          Advanced Word-Based Passlist Generator")
    print("          Created by: [ÖMER FARUK GÜNER]")
    print("          --------------------------------------\n")


def apply_leet_speak(word):
    """Generates common leet speak variations of a given word."""
    variations = {word.lower(), word.capitalize(), word.upper()}

    leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
    leet_word = word.lower()
    for char, leet_char in leet_map.items():
        leet_word = leet_word.replace(char, leet_char)

    variations.add(leet_word)
    variations.add(leet_word.capitalize())
    return list(variations)


def generate_wordlist(words, output_file, min_len, max_len, use_leet, use_suffix):
    suffixes = ['']
    if use_suffix:
        suffixes.extend(['!', '.', '?', '_', '123', '2025', '2026'])

    base_words = list(set([w.strip() for w in words if w.strip()]))

    print(f"\n[*] Target file: {output_file}")
    print("[*] Calculating and writing combinations (This may take a while)...\n")

    count = 0
    with open(output_file, "w", encoding="utf-8") as f, tqdm(desc="Passwords Generated", unit=" pass") as pbar:

        for r in range(1, len(base_words) + 1):

            for combo in itertools.permutations(base_words, r):

                if use_leet:
                    case_variations = [apply_leet_speak(word) for word in combo]
                else:
                    case_variations = [[word.lower(), word.capitalize()] for word in combo]

                for case_combo in itertools.product(*case_variations):
                    base_password = "".join(case_combo)

                    for suffix in suffixes:
                        final_password = base_password + suffix

                        if min_len <= len(final_password) <= max_len:
                            f.write(final_password + "\n")
                            count += 1
                            pbar.update(1)

    print(f"\n[+] SUCCESS! A total of {count} passwords have been saved to '{os.path.abspath(output_file)}'.")


def interactive_mode():
    print_banner()
    print("[1] Specify the number of words")
    print("[2] Enter words continuously (Press 'Enter' on a blank line or 'Ctrl+C' to finish)")
    print("[3] Read words from a text file (.txt)")

    choice = input("\nSelect an option (1/2/3): ")
    words = []

    if choice == "1":
        try:
            num_words = int(input("\nHow many words will you enter?: "))
            for i in range(num_words):
                w = input(f"Word {i + 1}: ")
                if w.strip(): words.append(w.strip())
        except ValueError:
            print("[-] Error: Please enter a valid number.")
            return

    elif choice == "2":
        print("\nEnter words one by one. Press 'Enter' on a blank line or 'Ctrl+C' to finish.")
        while True:
            try:
                w = input("> ")
                if not w.strip():  # Kullanıcı boş enter yaparsa çık
                    break
                words.append(w.strip())
            except KeyboardInterrupt:  # Kullanıcı Ctrl+C yaparsa çık
                print("\n[*] Input stopped by user.")
                break

    elif choice == "3":
        file_path = input("\nEnter the path to your text file (e.g., words.txt): ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                words = [line.strip() for line in file if line.strip()]
            print(f"[+] Successfully loaded {len(words)} words from '{file_path}'.")
        except FileNotFoundError:
            print(f"[-] Error: File '{file_path}' not found.")
            return
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            return

    else:
        print("[-] Invalid choice.")
        return

    if not words:
        print("[-] Error: No words provided.")
        return

    output_file = input("\nOutput file name (Default: wordlist.txt): ").strip() or "wordlist.txt"

    try:
        min_len = int(input("Minimum password length (Default: 4): ").strip() or "4")
        max_len = int(input("Maximum password length (Default: 64): ").strip() or "64")
    except ValueError:
        print("[-] Error: Invalid number. Using default values.")
        min_len, max_len = 4, 64

    use_leet = input("Enable Leet Speak variations (e.g., a->@)? (y/N): ").strip().lower() == 'y'
    use_suffix = input("Enable common suffixes (e.g., !, 2026, .)? (y/N): ").strip().lower() == 'y'

    generate_wordlist(words, output_file, min_len, max_len, use_leet, use_suffix)


def main():
    parser = argparse.ArgumentParser(description="Brunch: Advanced Word-Based Passlist Generator")
    parser.add_argument("-w", "--words", help="Comma-separated list of words (e.g., admin,123,cyber)")
    parser.add_argument("-f", "--file", help="Path to a text file containing words (one per line)")
    parser.add_argument("-o", "--output", help="Output file name", default="wordlist.txt")
    parser.add_argument("--min", type=int, help="Minimum password length", default=4)
    parser.add_argument("--max", type=int, help="Maximum password length", default=64)
    parser.add_argument("--leet", action="store_true", help="Enable leet speak variations")
    parser.add_argument("--suffix", action="store_true", help="Enable common suffixes (!, 2026, etc.)")

    if len(sys.argv) == 1:
        interactive_mode()
    else:
        args = parser.parse_args()

        word_list = []
        if args.words:
            word_list.extend([w.strip() for w in args.words.split(",") if w.strip()])

        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as file:
                    word_list.extend([line.strip() for line in file if line.strip()])
            except Exception as e:
                print(f"[-] Error reading file '{args.file}': {e}")
                sys.exit(1)

        if not word_list:
            print("[-] Error: You must provide words using -w or -f in CLI mode.")
            sys.exit(1)

        generate_wordlist(word_list, args.output, args.min, args.max, args.leet, args.suffix)


if __name__ == "__main__":
    main()