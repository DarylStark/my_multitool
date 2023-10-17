Contexts
========

The script uses context to give the user access to multiple environment. You can, for instance, create a context for the production environment, one for the acceptence environment, one for the testing environment and one for the development environment. This way, you can use this tool for multiple environments without switching machines or by fiddling with configuration files.

A context has three fields:

-   ``name``: the name of the context. For instance: ``production`` or ``instance01``
-   ``db_string``: the database URL for SQLAlchemy. For instance: ``sqlite:///:memory:/``.
-   ``warning``: indicates if for this contexts warnings should be displayed when doing something destructive.

When starting the application for the first time, a default context with the name ``context`` is created. The database URL for this context is a SQLite in-memory database. All context related commands are placed in the ``contexts`` subcommand:

.. code-block::

    ~ $ my-multitool contexts --help
                                                                                                                                                                
     Usage: my-multitool contexts [OPTIONS] COMMAND [ARGS]...                                                                                             
                                                                                                                                                                    
     Context management                                                                                                                                             
                                                                                                                                                                    
    ╭─ Options ───────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                         │
    ╰─────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────╮
    │ create                          Create a context.                   │
    │ delete                          Delete a context.                   │
    │ list                            List configured contexts.           │
    │ set                             Update a configured context.        │
    │ use                             Use a context.                      │
    ╰─────────────────────────────────────────────────────────────────────╯

The following paragraphs explain the different options.

Listing configured Contexts
---------------------------

To list all configured contexts, you use the ``list`` command in the ``contexts`` subcommand:

.. code-block::

    ~ $ my-multitool contexts list
                                    
      *   Name      Database string                    Warning
     ───────────────────────────────────────────────────────────
      *   default   sqlite:///:memory:  
          prod      mysql:///username:***@10.1.1.1/

The asterisk in front of the ``default`` context indicates that this is the selected context. Every command that you execute with the tool, will be executed on that context and on the selected database. If there is a password in the database string, the application will mask it with three asterisks. There is no way to display the password after configuring it, except for looking in the configurationfile itself. The last column, ``Warning``, indicates if the ``waring`` flag for this context is set.

Creating a Context
------------------

To create a context, you use the ``create`` command of the ``contexts`` command. You have to specify the *name* and the *database string* as arguments to the command. If you give the ``--warning`` flag to the command, the ``warning`` flag for the context will be set.

After creating the context, you can see it with the ``contexts list`` command.

.. code-block::

    ~ $ my-multitool contexts create my_context sqlite:///home/vscode/db.sql
    Context with name "my_context" is created

You can also specify a ``--service-user``, ``--service-pass`` and ``--root-user`` to define credentials within the context that should be used for working with users in the database.

Editing a Context
-----------------

To edit a context, you use the ``set`` command. After the command, you give the name of the context you want to edit. After that you can tell the command what you want to edit with the following optional arguments:

-   ``--new-name``; to specify a new name for the context.
-   ``--db-string``: a new DB string for the context.
-   ``--warning``: to enable the warning flag for the context.
-   ``--no-warning``: to disable the warning flag for the context.
-   ``--service-user``: the user to use when creating a service connection.
-   ``--service-pass``: the password to use when creating a service connection.
-   ``--root-user``: the root user to use when working with users.

For example, to rename the context with name ``my_context`` to ``test_context``, you have to use the following command:

.. code-block::

    ~ $ my-multitool contexts set my_context --new-name test_context
    Context with name "my_context" is updated

To update the database string for the context:

.. code-block::

    ~ $ my-multitool contexts set test_context --db-string sqlite:///:memory:/
    Context with name "my_context" is updated

Deleting a Context
------------------

Deleting a Context can be done with the ``delete`` command from the ``contexts`` subcommand. As a positional argument, you give the name of the context you want to delete:

.. code-block::

    ~ $ my-multitool contexts delete test_context
    Context with name "test_context" is deleted

Selecting a Context for use
---------------------------

Once you created a context, you can select it for use. That means that all actions you perform with the script are done on the database that is selected in the current context. To select a context, you specify the name of the context after the ``use`` command:

.. code-block::

    ~ $ my-multitool contexts use test_context
    Now using "test_context"

If you look at the list of configured context after selecting a new context, it will be marked with a asterisk.