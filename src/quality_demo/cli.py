"""Command-line runner translating options to standard pytest invocations."""

import argparse
import sys

import pytest


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for the quality-demo CLI."""
    parser = argparse.ArgumentParser(
        prog="quality-demo",
        description="Run test suite against Restful Booker Platform.",
    )
    parser.add_argument(
        "--target",
        default="demo",
        help="Configuration target name matching config/<target>.toml (default: demo)",
    )
    parser.add_argument(
        "--markers",
        "-m",
        default=None,
        help="Pytest marker expression (e.g. 'smoke', 'api', 'bdd', 'not writes_data')",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser tests in headed mode",
    )
    parser.add_argument(
        "--workers",
        "-n",
        type=int,
        choices=[1, 2],
        default=1,
        help="Number of parallel worker processes (1 or 2, default: 1)",
    )
    parser.add_argument(
        "--allure-output",
        default=None,
        help="Directory path to output raw Allure results",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned pytest arguments without running tests or launching browsers",
    )
    return parser


def build_pytest_args(args: argparse.Namespace) -> list[str]:
    """Translate CLI options into pytest argument list."""
    pytest_args: list[str] = []

    if args.target:
        pytest_args.extend(["--target", args.target])

    if args.markers:
        pytest_args.extend(["-m", args.markers])

    if args.headed:
        pytest_args.append("--headed")

    if args.workers > 1:
        pytest_args.extend(["-n", str(args.workers)])

    if args.allure_output:
        pytest_args.extend(["--alluredir", args.allure_output])

    return pytest_args


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    parsed_args = parser.parse_args(argv)

    pytest_args = build_pytest_args(parsed_args)

    if parsed_args.dry_run:
        print("Dry run: pytest command arguments:")
        print("pytest " + " ".join(pytest_args))
        return 0

    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
