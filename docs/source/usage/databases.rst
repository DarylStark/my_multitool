Databases
=========

The ``database`` command for the ``my-multitool`` command line utility should be used to manage a database. The database connection string for the database to be maneged is configured in the contexts. Contexts are explained on the page :doc:`contexts`.

All database related commands are placed in the ``database`` subcommand:

..code-block::

    ~ $ my-multitool database --help
                                                                                                                                                                                                                                                                                                                                                                    
     Usage: my-multitool database [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                                                                    
     Database management                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                                                    
    ╭─ Options ───────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                         │
    ╰─────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────────────────────╮
    │ create                          Create the database schema.         │
    ╰─────────────────────────────────────────────────────────────────────╯

The following paragraphs explain the different options.

Create the database scheme
--------------------------

To create the database scheme for the selected context, you use the ``create`` subcommand of the ``my-multitool database`` command. The ``create`` command contains a few options:

* ``--echo-sql``: giving this flag will show the SQL commands that are being executed. This can be usefull for troubleshooting.
* ``--drop-tables``: this will drop tables before creating them. This will result in data loss!
* ``--create-data``: this will create (test-) data in the database. Before doing this, the tables will be dropped. This will result in data loss!

.. warning::
    Using the ``--drop-tables`` or ``--create-data`` flags will result in removing all data from the database and will result in data loss. Use this with caution.

Examples
^^^^^^^^

To create a database without dropping any data:

.. code-block::

    my-multitool database create

To create a database with creating data (and dropping all existing data):

.. code-block::

    my-multitool database create --create-data