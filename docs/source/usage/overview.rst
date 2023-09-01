Overview
========

This package is meant to be used as a CLI script. After installation, it is started with the command ``my-multitool``. When not giving a argument, or when given the ``--help`` argument, the script will display help on how to use the script:

.. code-block:: bash

    ~ $ my_multitool
                                                                                                                                                                
     Usage: my_multitool [OPTIONS] COMMAND [ARGS]...                                                                                                      
                                                                                                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                     │
    │ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation.              │
    │                                                              [default: None]                                                                                 │
    │ --help                                                       Show this message and exit.                                                                     │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ contexts                                          Context management                                                                                         │
    │ database                                          Database management                                                                                        │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

As you can see in the overview, you can install command completion with the ``--install-completion`` and ``--show-completion`` scripts. The ``contexts`` and ``database`` subcommands can be used for specific tasks:

-   ``contexts``: manage configuration contexts for the CLI script. Read more about this on the page about `Contexts <contexts.html>`_.
-   ``database``: manage a database in the current context. Read more about this on the page about `Databases <databases.html>`_.