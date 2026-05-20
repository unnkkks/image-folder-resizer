"""Generate tests and coverage SVG badges from CI report files."""

from pathlib import Path

from genbadge.main import get_coverage_badge, get_coverage_stats, get_test_stats, get_tests_badge

ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / "badges"


def main() -> None:
    """Generate badge SVG files from junit.xml and coverage.xml."""
    BADGES.mkdir(exist_ok=True)

    tests = get_test_stats(ROOT / "junit.xml")
    get_tests_badge(tests, "tests").write_to(BADGES / "tests.svg")

    coverage = get_coverage_stats(ROOT / "coverage.xml")
    get_coverage_badge(coverage, "coverage").write_to(BADGES / "coverage.svg")


if __name__ == "__main__":
    main()
