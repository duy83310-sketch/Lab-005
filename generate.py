import json
import sys


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    if n < 0:
        raise SystemExit("n must be non-negative")

    with open("web.jsonl", "w", encoding="utf-8") as f:
        for i in range(n):
            j = i % 10
            page = "/home" if j < 4 else (
                "/product" if j < 7 else "/checkout"
            )
            row = {
                "id": i,
                "page": page,
                "status": 500 if j >= 8 else 200,
                "ms": 100 + 10 * j,
            }
            f.write(json.dumps(row, separators=(",", ":")) + "\n")

    print(f"generated: {n} rows in web.jsonl")


if __name__ == "__main__":
    main()
