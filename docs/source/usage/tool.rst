Tool
====

The ``tool`` command for the ``my-multitool`` utility can be used to get information about the tool itself. The following subcommands are defined:

-   ``version``: get version information for the tool.

Version information
-------------------

Get version information about the tool and all used libraries that matter:

.. code-block::

    $ my-multitool tool version
                            
      Library        Version    
     ────────────────────────── 
      My Model       1.3.0      
      My Data        1.1.0      
      My Multitool   1.0.1-dev  
      Pydantic       2.5.2      
      SQLModel       0.0.14     
      SQLAlchemy     2.0.23     
      Typer          0.9.0 