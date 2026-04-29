import os
import sys

def main():
    print("\033[H\033[J", end="")
    print("="*60)
    print("                余震：坍塌的巴别塔                ")
    print("              (Aftershock: Babel)               ")
    print("="*60)
    print("\n[加载核心模块中...]")

    try:
        import chapter1
    except ImportError as e:
        print(f"加载失败: {e}")
        sys.exit(1)

    print("\n请选择游戏难度:")
    print("1. 简单模式 (默认物资、回复量)")
    print("2. 困难模式 (物资爆率减少，状态回复量降低 30%)")

    while True:
        ans = input("\n请输入数字 (1/2): ").strip()
        if ans == "1":
            diff = "easy"
            break
        elif ans == "2":
            diff = "hard"
            break
        else:
            print("无效输入，请输入 1 或 2。")

    print("\n按回车键开始游戏...")
    input()

    chapter1.start_chapter1(difficulty=diff)

if __name__ == "__main__":
    main()
