from __future__ import annotations

import argparse
import sys

from agents.idea_agent import main as run_idea_agent_main


def main() -> None:
    parser = argparse.ArgumentParser(description="Top-level agent dispatcher")
    parser.add_argument(
        "--agent",
        choices=["idea_agent"],
        default="idea_agent",
        help="Agent to run",
    )
    args, remaining = parser.parse_known_args()

    if args.agent == "idea_agent":
        original_argv = sys.argv
        try:
            sys.argv = [original_argv[0], *remaining]
            run_idea_agent_main()
        finally:
            sys.argv = original_argv
        return

    raise ValueError(f"Unsupported agent: {args.agent}")


if __name__ == "__main__":
    main()
