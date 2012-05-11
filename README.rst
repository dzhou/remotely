Remotely
========
Remotely is a simple and secure remote code execution api. 
You start the remotely server on the box where you want to execute code.

::

    $ python remotely_server.py --api_key=YOUR_API_KEY --port=7070
    starting remote exec server on port 7070 ..
    ...

And you use the remotely decorater for any function you want to run remotely.

::

    from remotely import remotely

    @remotely(YOUR_API_KEY, SERVER, PORT)
    def remote_code():
        # do something here
        return result

    # function will be executed on remote server
    remote_code()



