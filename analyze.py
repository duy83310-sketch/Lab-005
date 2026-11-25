import csv
import json
import sys
import time
from collections import defaultdict


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "web.jsonl"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "report.csv"
    started = time.perf_counter()
    totals = defaultdict(lambda: [0, 0, 0])
    bad = 0

    with open(input_path, encoding="utf-8") as source:
        for line in source:
            try:
                row = json.loads(line)
                page = row["page"]
                status = row["status"]
                ms = row["ms"]
                if not isinstance(page, str) or not page:
                    raise ValueError("page must be a non-empty string")
                if type(status) is not int or not 100 <= status <= 599:
                    raise ValueError("status must be an HTTP status integer")
                if type(ms) is not int or ms < 0:
                    raise ValueError("ms must be a non-negative integer")
            except (ValueError, KeyError, TypeError):
                bad += 1
                continue

            totals[page][0] += 1
            totals[page][1] += int(500 <= status < 600)
            totals[page][2] += ms

    with open(output_path, "w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination)
        writer.writerow(["page", "hits", "errors", "error_rate", "avg_ms"])
        for page, (hits, errors, total_ms) in sorted(totals.items()):
            writer.writerow(
                [page, hits, errors, errors / hits, total_ms / hits]
            )

    print(f"bad: {bad} seconds: {time.perf_counter() - started:.6f}")


if __name__ == "__main__":
    main()
