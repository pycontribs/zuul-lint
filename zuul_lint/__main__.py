"""ZuuL Lint.

A linter for Zuul configuration files.
"""
import argparse
import json
import pathlib
import sys

import pkg_resources
import yaml
from jsonschema import Draft7Validator


def encrypted_pkcs1_oaep_constructor(loader, node):
    """Construct a sequence from a YAML node representing an encrypted PKCS#1 OAEP key.

    Args:
    ----
        loader: A YAML loader object.
        node: A YAML node representing the encrypted key.

    Returns:
    -------
        A sequence of bytes representing the encrypted key.
    """
    return loader.construct_sequence(node)


# Register the custom yaml constructor
yaml.SafeLoader.add_constructor(
    "!encrypted/pkcs1-oaep", encrypted_pkcs1_oaep_constructor,
)


def zuul_schema():
    """Load the Zuul schema from a JSON file.

    Returns
    -------
        A dictionary representing the Zuul schema.
    """
    x = pathlib.Path(__file__).parent / "zuul-schema.json"
    with pathlib.Path.open(x, encoding="utf-8") as f:
        return json.load(f)


def lint(f, schema):
    """Validate a YAML file against a JSON schema.

    Args:
    ----
        f: A string representing the path to the YAML file to validate.
        schema: A JSON schema to validate against.

    Returns:
    -------
        The number of validation errors encountered.
    """
    print(f)
    errors = 0
    # we use Draft7Validator() because validate() can give misleading errors,
    # see https://github.com/Julian/jsonschema/issues/646
    v = Draft7Validator(schema)

    with pathlib.Path.open(pathlib.Path(f), encoding="utf-8") as yaml_in:
        try:
            obj = yaml.safe_load(yaml_in)
            va_errors = v.iter_errors(obj)
            for e in va_errors:
                print(e, file=sys.stderr)
                errors += 1
        except yaml.YAMLError as e:
            print(e)
            errors += 1
    return errors


def main():
    """Parse command-line arguments and run the Zuul linter on the specified file(s).

    Returns
    -------
        None.
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
        print(f"Failed with {errors} errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
