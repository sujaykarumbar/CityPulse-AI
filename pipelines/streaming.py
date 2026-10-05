from __future__ import annotations

import argparse
import json

from citypulse.streaming.service import StreamingService


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect CITYPULSE streaming compatibility status.")
    parser.add_argument("command", choices=["status", "topics", "state", "dead-letter"])
    args = parser.parse_args()
    service = StreamingService()
    if args.command == "status":
        result = service.status().model_dump(mode="json")
    elif args.command == "topics":
        result = {"topics": service.status().topics}
    elif args.command == "state":
        result = service.current_state()
    else:
        result = {"dead_letter": [item.model_dump(mode="json") for item in service.broker.dead_letters()]}
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
