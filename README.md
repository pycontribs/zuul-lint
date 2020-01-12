# zuul-lint

## Validate from the command line

```
pip install zuul-lint

zuul-lint .zuul.yaml
```

## Validate with pre-commit

Add the code below to your `.pre-commit-config.yaml` file:

```yaml
  - repo: https://github.com/pycontribs/zuul-lint.git
    rev: "0.1"
    hooks:
      - id: zuul-lint
```


## Validate with VS Code

To ease editing Zuul CI configuration file we added experimental support for
a Zuul JSON Schema. This should enable validation and auto-completion in
code editors.

For example on [VSCode](1) you can use the [YAML](2) extension to use such a schema
validation by adding the following to `settings.json`:


```json
"yaml.schemas": {
    "https://raw.githubusercontent.com/pycontribs/zuul-lint/master/zuul_lint/zuul-schema.json": ["*zuul.d/*.yaml", "*/.zuul.yaml"]
    },
"yaml.customTags": [
    "!encrypted/pkcs1-oaep array"
],
"sortJSON.orderOverride": ["title", "name", "$schema", "version", "description", "type"],
"sortJSON.orderUnderride": ["definitions"]

```

[1]: https://code.visualstudio.com/
[2]: https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml
