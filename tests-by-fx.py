import os
import re
import argparse
from collections import defaultdict

# ANSI color codes
YELLOW = "\033[0;93m"
RESET = "\033[0m"

# Define test directory
TEST_DIR = "."

# Dictionary to store test counts per fixture
test_counts = defaultdict(int)

# Set to track unique test entries across all fixtures
unique_tests = set()

def find_marked_tests(marker):
    """Find all tests marked with @pytest.mark.<marker> and print results"""
    print(f"---\npytest marker: {marker}\n")
    count = 0  # Count for this marker

    # Regex to match exactly `@pytest.mark.<marker>` (ignores `skipif`, etc.)
    marker_pattern = re.compile(rf"@pytest\.mark\.{marker}(\(|\s|$)")

    for root, _, files in os.walk(TEST_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    if marker_pattern.search(line):  # Exact marker match
                        test_name = None
                        reason = None

                        # Look for the next function definition after the marker
                        for j in range(i + 1, len(lines)):
                            match = re.match(r"def (test_\w+)\(", lines[j])
                            if match:
                                test_name = match.group(1)
                                break

                        # Extract reason if available
                        reason_match = re.search(r'reason="(.*?)"', line)
                        if reason_match:
                            reason = reason_match.group(1)

                        # Store unique test entry
                        if test_name:
                            test_entry = f"{file_path}::{test_name}"
                            unique_tests.add(test_entry)

                            # Print test entry with the appropriate icon
                            formatted_reason = f" - {YELLOW}{reason}{RESET}" if reason else ""
                            icon = "🧪" if reason else "✅"
                            print(f"{icon} {test_entry}{formatted_reason}")

                            count += 1

    test_counts[marker] += count  # Store count per fixture
    return count  # Return count so we can print it only once


def group_by_fixture():
    """Find all tests grouped by marker and display total"""
    markers = ["pipeline", "smoke", "xfail", "skip"]
    for marker in markers:
        find_marked_tests(marker)

    # Display summary
    print("\n=== 📊 Test Summary ===")
    total_tests = len(unique_tests)  # Count unique tests only
    for marker, count in test_counts.items():
        print(f"🔹 {marker}: {count} tests")
    print(f"🔥 Grand Total (Unique): {total_tests} tests\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Group tests by fixture markers and then show totals.")
    parser.add_argument("marker", choices=["pipeline", "smoke", "xfail", "skip", "all"], help="Specify the pytest marker to search for.")
    
    args = parser.parse_args()

    if args.marker == "all":
        group_by_fixture()
    else:
        total_count = find_marked_tests(args.marker)  # Only print the total ONCE
        print(f"\n📊 Total {args.marker} tests found: {total_count}\n")
