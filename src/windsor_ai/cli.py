import argparse
import os
import sys
import json
import csv
from typing import List

from .client import Client
from .models import Filter
from .exceptions import WindsorAIError


def parse_filter(filter_string: str) -> Filter:
    """
    Parses a string in the format field:operator:value into a Filter object.
    Example: campaign:contains:google
    """
    try:
        parts = filter_string.split(":", 2)
        if len(parts) != 3:
            raise ValueError
        field, operator, value = parts
        return Filter(field, operator, value)
    except ValueError:
        print(
            f"Error: Filter '{filter_string}' is invalid. Format must be 'field:operator:value'"
        )
        sys.exit(1)


def output_results(data: List[dict], output_format: str, output_file: str = ""):
    """Handles formatting and writing results to stdout or file."""
    if not data:
        print("No data found.", file=sys.stderr)
        return

    content = ""

    if output_format == "json":
        content = json.dumps(data, indent=2)
    elif output_format == "csv":
        # Determine headers dynamically from all keys present in data
        keys = set()
        for item in data:
            keys.update(item.keys())
        sorted_keys = sorted(list(keys))

        if output_file:
            # Write directly to file to handle large datasets better
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=sorted_keys)
                writer.writeheader()
                writer.writerows(data)
            return
        else:
            # Write to string for stdout
            import io

            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=sorted_keys)
            writer.writeheader()
            writer.writerows(data)
            content = output.getvalue()

    if output_file:
        if output_format == "json":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
    else:
        print(content)


def main():
    parser = argparse.ArgumentParser(
        description="Windsor.ai CLI Wrapper", prog="windsor"
    )

    # Global Arguments
    parser.add_argument(
        "--api-key",
        help="Windsor API Key. Can also be set via WINDSOR_API_KEY env var.",
        default=os.environ.get("WINDSOR_API_KEY"),
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list-connectors
    subparsers.add_parser("list-connectors", help="List all available connector IDs")

    # Command: fields
    fields_parser = subparsers.add_parser(
        "fields", help="Get available fields for a connector"
    )
    fields_parser.add_argument(
        "connector", help="The connector ID (e.g., facebook, google_ads)"
    )

    # Command: query
    query_parser = subparsers.add_parser("query", help="Fetch data from connectors")
    query_parser.add_argument(
        "--connector", default="all", help="Connector ID (default: all)"
    )
    query_parser.add_argument(
        "--fields", help="Comma-separated list of fields (e.g., date,campaign,clicks)"
    )
    query_parser.add_argument(
        "--date-preset", help="Date preset (e.g., last_7d, last_30d)"
    )
    query_parser.add_argument("--date-from", help="Start date (YYYY-MM-DD)")
    query_parser.add_argument("--date-to", help="End date (YYYY-MM-DD)")
    query_parser.add_argument(
        "--filter",
        action="append",
        help="Filter rule: 'field:operator:value' (Can be used multiple times)",
    )
    query_parser.add_argument(
        "--format", choices=["json", "csv"], default="json", help="Output format"
    )
    query_parser.add_argument("--out", help="Output file path (optional)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not args.api_key:
        print(
            "Error: API Key is missing. Set WINDSOR_API_KEY environment variable or use --api-key.",
            file=sys.stderr,
        )
        sys.exit(1)

    client = Client(args.api_key)

    try:
        if args.command == "list-connectors":
            connectors = client.list_connectors
            print(json.dumps(connectors, indent=2))

        elif args.command == "fields":
            fields = client.get_connector_fields(args.connector)
            print(json.dumps(fields, indent=2))

        elif args.command == "query":
            # Process arguments
            field_list = args.fields.split(",") if args.fields else None

            filters = []
            if args.filter:
                for f_str in args.filter:
                    filters.append(parse_filter(f_str))

            # For massive CSV exports, consider using client.stream_connectors
            response = client.connectors(
                connector=args.connector,
                fields=field_list,
                date_preset=args.date_preset,
                date_from=args.date_from,
                date_to=args.date_to,
                filters=filters,
            )

            output_results(response.get("data", []), args.format, args.out)

    except WindsorAIError as e:
        print(f"API Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
