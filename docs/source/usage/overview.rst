Overview
========

This package is meant to be used as a CLI script. After installation, it is started with the command ``my-multitool``. When not giving a argument, or when given the ``--help`` argument, the script will display help on how to use the script:

.. code-block:: bash

    ~ $ my-multitool
                                                                                                                                                                
     Usage: my-multitool [OPTIONS] COMMAND [ARGS]...                                                                                                      
                                                                                                                                                                    
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                     │
    │ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation.              │
    │                                                              [default: None]                                                                                 │
    │ --help                                                       Show this message and exit.                                                                     │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ contexts                                                                 Context management                                                                  │
    │ database                                                                 Database management                                                                 │
    │ users                                                                    User management                                                                     │
    │ version                                                                  Display version information.                                                        │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

As you can see in the overview, you can install command completion with the ``--install-completion`` and ``--show-completion`` scripts. The ``contexts`` and ``database`` subcommands can be used for specific tasks:

-   ``contexts``: manage configuration contexts for the CLI script. Read more about this on the page about `Contexts <contexts.html>`_.
-   ``database``: manage a database in the current context. Read more about this on the page about `Databases <databases.html>`_.
-   ``users``: manage the users in the database. Read more about this on the page about `Users <users.html>`_.
-   ``version``: display the version of this tool and the used libraries.

Version information
-------------------

To get version information, enter the `version` subcommand:

.. code-block::

    $ my-multitool version
                            
      Library        Version    
     ────────────────────────── 
      My Model       1.3.0      
      My Data        1.1.0      
      My Multitool   1.0.1
      Pydantic       2.5.2      
      SQLModel       0.0.14     
      SQLAlchemy     2.0.23     
      Typer          0.9.0 