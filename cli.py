import sys
import select
import time
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    print("\033[H\033[J", end="")

def calculate_timeout(text):
    length = len(text)
    calculated_time = int(length / 5.0) + 3
    return max(10, calculated_time)

def _get_input_windows(timeout):
    import msvcrt
    start_time = time.time()
    input_str = ""

    while True:
        elapsed = time.time() - start_time
        remaining = int(timeout - elapsed)

        print(f"\r(剩余 {remaining:02d} 秒) > {input_str} \033[K", end="", flush=True)

        if remaining <= 0:
            print("\n")
            return None

        if msvcrt.kbhit():
            char = msvcrt.getwche()
            if char == '\r' or char == '\n':
                print()
                return input_str
            elif char == '\x08':
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    print(" \x08", end="", flush=True)
            else:
                input_str += char
        time.sleep(0.1)

def _get_input_unix(timeout):
    start_time = time.time()
    input_str = ""

    import tty
    import termios
    fd = sys.stdin.fileno()
    is_tty = sys.stdin.isatty()
    old_settings = None
    if is_tty:
        old_settings = termios.tcgetattr(fd)

    try:
        if is_tty:
            tty.setcbreak(sys.stdin.fileno())

        while True:
            elapsed = time.time() - start_time
            remaining = int(timeout - elapsed)

            print(f"\r(剩余 {remaining:02d} 秒) > {input_str}\033[K", end="", flush=True)

            if remaining <= 0:
                print("\n")
                return None

            i, o, e = select.select([sys.stdin], [], [], 0.1)
            if i:
                char = sys.stdin.read(1)
                if not char:
                    print("\n收到 EOF，退出游戏。")
                    sys.exit(0)
                if char == '\n' or char == '\r':
                    print()
                    return input_str
                elif char in ('\b', '\x7f'):
                    if len(input_str) > 0:
                        input_str = input_str[:-1]
                else:
                    input_str += char
    finally:
        if is_tty and old_settings:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def prompt_with_timeout(choices_str, player=None, description_text="", override_timeout=None):
    full_text = description_text + "\n" + choices_str

    if override_timeout is not None:
        timeout = override_timeout
    else:
        timeout = calculate_timeout(full_text)

    if description_text:
        print(f"\n{Colors.OKCYAN}{description_text}{Colors.ENDC}")
    print(f"\n{choices_str}")

    while True:
        if os.name == 'nt':
            user_input = _get_input_windows(timeout)
        else:
            user_input = _get_input_unix(timeout)

        if user_input is None:
            return None

        user_input = user_input.strip()

        if user_input.lower() == 'inv':
            if player:
                from inv_system import interactive_inventory
                interactive_inventory(player)
            else:
                print(f"\n{Colors.WARNING}无法访问背包。{Colors.ENDC}\n")

            print(f"\n{choices_str}")
            print(f"{Colors.WARNING}(背包已关闭，重新开始计时){Colors.ENDC}")
            continue

        return user_input

def display_hud(player, time_system):
    print("=" * 50)
    print(f"{Colors.BOLD}[{time_system.get_time_string()}]{Colors.ENDC}")
    player.print_status()
    print(f"{Colors.OKBLUE}提示: 输入数字进行选择，输入 'inv' 打开背包{Colors.ENDC}")
    print("=" * 50)
