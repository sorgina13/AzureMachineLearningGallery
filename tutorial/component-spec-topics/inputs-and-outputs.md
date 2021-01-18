# Inputs and outputs

The component could have inputs and outputs.

An input could either be an *Input Port* or a *Parameter*. Output could only be an *Output Port*.

Input ports and output ports typically refers to a path. In Designer, they will be displayed as a *port* on the component. They could be have arbitrary type names such as `CsvFile`, `ImageFolder` to describe the underlying data. A component's output port could be connected to another component's input port, given they have the same type name.

Parameters are input values passed to the component while executing. In Designer, they are displayed on the right panel of the component. Parameter could only have scalar values such as `Integer`, `String`, `Boolean`, `Enum`. Each parameter could have additional attributes such as `default`, `min`, `max`, etc.

Refer to [the component spec](../component-spec-definition.md) for full description.

To define component inputs and outputs:
* Add `inputs` and `outputs` section to the component spec to specify the component interface.
* Add reference to the inputs and outputs in `command` section. A reference looks like `{inputs.name_of_parameter}`, which will be replaced by the value of the parameter when invoking the component.

## Optional Inputs and Parameters

Use `optional` to make an input port or a parameter optional.
In the snippet bellow, two input ports and the parameter "Optional string parameter" are optional.

```yaml
inputs:
  input_path:
    type: AnyDirectory
    optional: true
  optional_input_path:
    type: AnyDirectory
    optional: true
  string_parameter:
    type: String
    default: string value
    description: A parameter accepts a string value.
  optional_string_parameter:
    type: String
    optional: true
    description: A optional parameter accepts a string value.
```

In the `command` part, put optional parameter into []:
```yaml
command: >-
  python optional_input.py
    --input-path  {inputs.input_path},
    [--optional-input-path, {inputs.optional_input_path}],
    --string-param, {inputs.string_parameter},
    [--optional-string-param, {inputs.optional_string_parameter}]
```

When invoking the component, the command line will look like:

```bash
# When the optional input is linked, and the optional parameter is set.
python optional_input.py --input-path /aaa/bbb --optional-input-path /xxx/yyy --string-param abc --optional-string-param def

# When the optional input is linked, and the optional parameter is not set.
python optional_input.py --input-path /aaa/bbb --optional-input-path /xxx/yyy --string-param abc

# When the optional input is not linked, and the optional parameter is set.
python optional_input.py --input-path /aaa/bbb --string-param abc --optional-string-param def

# When the optional input is not linked, and the optional parameter is not set.
python optional_input.py --input-path /aaa/bbb --string-param abc
```

## Sample component

[A component with optional inputs and parameters](./samples/inputs-and-outputs/README.md)