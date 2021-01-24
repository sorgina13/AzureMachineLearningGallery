# FAQ

This document lists frequently asked questions of component, and the recommended solutions.

Please create Github issue to raise your questions if this document does not help with your issue.

1. **What type of inputs and outputs should I use when I create my own component?**
    
    DataFrameDirectory and AnyDirectory are recommended.

    - If your input or output data of component are in pandas.DataFrame format and you would like to connect your component to Designer built-in data processing modules, **DataFrameDirectory** is recommended.
    - If you input or output data are files like model file or file dataset, **AnyDirectory** is recommended.
    - Make sure that the input type of your component is aligned with the output type of the upstream component. The code logic behind these components should also be aligned in perspective of processing data.
    
1. **Can I use component for real-time inference?**

    No. Component does not support real-time inference currently.

1. **Why does my component hang in "Image Build" phase after I submit a pipeline run?**

    A potential cause is you do not set versions of packages in conda dependencies in your component spec. Pip with version >=20.3 will search among multiple versions for packages without versions set, and this will take a long time.
    
    Recommended solution is either you set **pip=20.2** in your conda dependencies, or set versions of pip-installed packages.

1. **Is there a limitation in using Python packages?**

    Theoretically no. You can use base image and conda.yaml to  define any dependencies for your component. You could refer to how to set [running environment](./tutorial/component-spec-topics/running-environment.md) in your component spec.

1. **Can we use complex directories in the python code?**

    Yes. Use [code](./tutorial/component-spec-topics/code-snapshot.md) in your component spec to refer to complex directories.

1. **Do we support single python command or multiple commands in the yaml spec?**

    Currently no. This is one feature in our roadmap.
