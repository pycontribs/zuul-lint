from __future__ import print_function
from jsonschema import Draft7Validator
import argparse
import json
import os
import pkg_resources
import sys
import yaml


def zuul_schema():
    x = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zuul-schema.json")
    with open(x, "r") as f:
        return json.load(f)


def lint(f, schema):
    print(f)
    errors = 0
    # we use Draft7Validator() because validate() can give misleading errors,
    # see https://github.com/Julian/jsonschema/issues/646
    v = Draft7Validator(schema)

    with open(f, "r") as yaml_in:
        try:
            obj = yaml.safe_load(yaml_in)
            va_errors = v.iter_errors(obj)
            for e in va_errors:
                print(e, file=sys.stderr)
                errors += 1
        except Exception as e:
            print(e)
            errors += 1
    return errors


def main():
    """Zuul Lint
    """
    parser = argparse.ArgumentParser(prog="zuul-lint")
    parser.add_argument(
        "--version",
        action="version",
        version=pkg_resources.get_distribution("zuul_lint").version,
    )
    parser.add_argument("file", nargs="+", help="file(s) to lint")
    args = parser.parse_args()
    schema = zuul_schema()
    errors = 0
    for f in args.file:
        errors += lint(f, schema=schema)

    if errors:
        sys.stderr.flush()
        print("Failed with %s errors." % errors)
        sys.exit(1)


if __name__ == "__main__":
    main()
