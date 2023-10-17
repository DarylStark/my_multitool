Users
=====

The ``users`` command for the ``my-multitool`` utility can be used to manage users. To make this work, a ``Service user``, ``Service password`` and ``Root user`` should be configured in the active context. There are two methods for ``users``:

-   ``list``: lists all users.
-   ``set-password``: set a password for a user.

List all users
--------------

To list all users in the database, use the ``list`` subcommand:

.. code-block::

    $ my-multitool users list
                                                                       
     #   Fullname                   Username        Role   Second factor  
    ───────────────────────────────────────────────────────────────────── 
     1   root                       root            1      No             
     2   Normal user 1              normal.user.1   3      No             
     3   Normal user 2              normal.user.2   3      No             
     4   Service User - for tests   service.user    2      No   

Change a password
-----------------

To change the password for a user, you use the ``set-password`` subcommand. After the subcommand, you have to enter the username of the user. The script will ask you the password.

.. code-block::

     $ my-multitool users set-password normal.user.2
      Password: 
      Repeat: 

After this, the password is reset.