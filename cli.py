from .evaluator import evaluate


def repl():
    history = []
    print("Simple CLI calculator. Type 'quit' or 'exit' to leave. 'history' to show past expressions.")
    while True:
        try:
            s = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not s:
            continue
        key = s.lower()
        if key in ("quit", "exit"):
            break
        if key == "history":
            for i, (expr, res) in enumerate(history, 1):
                print(f"{i}: {expr} = {res}")
            continue
        try:
            res = evaluate(s)
        except Exception as e:
            print("Error:", e)
            continue
        history.append((s, res))
        print(res)


if __name__ == "__main__":
    repl()
