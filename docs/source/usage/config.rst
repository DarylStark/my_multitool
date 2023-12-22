Config
======

The ``config`` portion of the command line tool gives the user the ability to configure the tool to his wishes. There are two subcommand's for the ``config`` portion of the app:

.. code-block:: bash

    $ my-multitool config --help
                                                                                                                                                                                                               
     Usage: my-multitool config [OPTIONS] COMMAND [ARGS]...                                                                                                                                                        
                                                                                                                                                                                                                   
     Configuration for My Multitool                                                                                                                                                                                
                                                                                                                                                                                                                   
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                                                                                                  │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ contexts                                                                                            Context management                                       │
    │ set-logging-level                                                                                   Set logging level.                                       │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Contexts
--------

The ``contexts`` subcommand gives you the ability to manage contexts. These contexts define on which database to operate. More information about this can be found on the page about `Contexts <contexts.html>`_.

Set logging level
-----------------

The ``set-logging-level`` subcommand gives you the ability to configure the logging level for the application. There are five options: ``debug``, ``info``, ``warning``, ``error`` and ``debug``.

Examples
^^^^^^^^

To set the logging level to ``debug``:

.. code-block:: bash

    $ my-multitool config set-logging-level debug
