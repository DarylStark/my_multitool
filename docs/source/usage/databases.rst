Databases
=========

The ``database`` command for the ``my-multitool`` command line utility should be used to manage a database. The database connection string for the database to be managed is configured in the contexts. Contexts are explained on the page :doc:`contexts`.

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
    │ import-json                     Import data from a JSON file.       │
    ╰─────────────────────────────────────────────────────────────────────╯

The following paragraphs explain the different options.

Create the database scheme
--------------------------

To create the database scheme for the selected context, you use the ``create`` subcommand of the ``my-multitool database`` command. The ``create`` command contains a few options:

* ``--echo-sql``: giving this flag will show the SQL commands that are being executed. This can be usefull for troubleshooting.
* ``--drop-tables``: this will drop tables before creating them. This will result in data loss!

.. warning::
    Using the ``--drop-tables`` flag will result in removing all data from the database and will result in data loss. Use this with **extreme** caution.

Examples
^^^^^^^^

To create a database without dropping any data:

.. code-block::

    my-multitool database create

To create a database and dropping all tables first:

.. code-block::

    my-multitool database create --drop-tables

Import data from a JSON file
----------------------------

To import data from a JSON file into the database, you use the ``import-json`` subcommand of the ``my-multitool database`` command. After the command, you give the JSON filename to import. The ``import-json`` command contains one option:

* ``--echo-sql``: giving this flag will show the SQL commands that are being executed. This can be usefull for troubleshooting.

A example JSON file to import is:

.. code-block:: json

    {
        "api_scopes": [
            {
                "id": 1,
                "module": "users",
                "subject": "create"
            },
            {
                "id": 2,
                "module": "users",
                "subject": "retrieve"
            }
        ],
        "users": [
            {
                "id": 1,
                "fullname": "root",
                "username": "root",
                "email": "root@example.com",
                "role": 1,
                "_password": "root_pw",
                "_tags": [
                    {
                        "title": "root_tag_1"
                    }
                ],
                "_api_clients": [
                    {
                        "id": 100,
                        "app_name": "root_api_client_1",
                        "app_publisher": "root_api_client_1_publisher"
                    }
                ],
                "_api_tokens": [
                    {
                        "id": 100
                        "title": "root_api_token_1",
                        "token": "MHxHL4HrmmJHbAR1b0gV4OkpuEsxxmRL",
                        "enabled": false,
                        "api_client_id": 100
                    }
                ],
                "_user_settings": [
                    {
                        "setting": "root_test_setting_1",
                        "value": "test_value_1"
                    }
                ]
            },
            {
                "id": 1,
                "fullname": "Service User - for tests",
                "username": "service.user",
                "email": "service.user@example.com",
                "role": 2,
                "_password": "service_password"
            }
        ],
        "api_token_scopes": [
            {
                "api_token_id": 100,
                "api_scope_id": 1
            }
        ]
    }

Examples
^^^^^^^^

To import data from a JSON file:

.. code-block::

    my-multitool database import-json data.json

To import data from a JSON file and show the SQL commands:

.. code-block::

    my-multitool database import-json data.json --echo-sql
