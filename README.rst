Remotely
========
Remotely is a simple and secure remote code execution api.
You start the remotely server on the box where you want to execute code.

::

    from remotely import create_remotely_server
    server = create_remotely_server("YOUR_API_KEY", PORT)
    server.serve_forever()
    ...

And you use the remotely decorater for any function you want to run remotely.

::

    from remotely import remotely

    @remotely("YOUR_API_KEY", SERVER, PORT)
    def remote_code():
        # import required packages
        # do something here
        return result

    # function will be executed on the remote server
    remote_code()

What you can use remotely for:

- to run code under another version of python
- to access libraries not available on the current box 
  (for example use win32com from linux)
- to access resources (files etc) on another box 

