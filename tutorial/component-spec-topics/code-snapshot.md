# Code snapshot

*Code snapshot* is used to allow the component author to change the default snapshot folder. 
For example, for the following folder structure:

```
src/
  library1/
    hello.py
  library2/
    greetings.py
  component_entry/
    conda.yaml
    component_spec.yaml
    run.py
```

The snapshot package will look like:

```
conda.yaml
component_spec.yaml
run.py
```

If we specify `code: ..` in component spec, setting the snapshot folder to the `src/` level, the snapshot will look like:

```
library1/
  hello.py
library2/
  greetings.py
component_entry/
  conda.yaml
  component_spec.yaml
  run.py
```

Here are some notes for the usage of *code snapshot*:
* Specify the relative path start from the folder containing the component spec yaml file. The code snapshot should be parent folders of the component spec file since component spec file should always be included in the snapshot file. Thus, the possible value for `code` must be one or more sections of `../`s. For the above folder structure example, specify `../` will set the snapshot folder to `src/`. For other folder structures which need to include further more top levels of parent folders, use `../../`, `../../../`, etc. accordingly.
* Use the relative path start from the snapshot folder for any file references in the spec file. For the above example, conda file should be `component_entry/conda.yaml` and entry script should be `component_entry/run.py` inside the component spec file.


## Examples

[Refer to here for an example component](./samples/code-snapshot/).
