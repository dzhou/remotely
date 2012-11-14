Remotely
========
Remotely is a simple and secure remote code execution api that supports both 
asynchronous and blocking execution. 

Remotely can be used for:

- distributing tasks to other boxes in parallel
- running coding under other versions of python
- accessing libraries not available on the current box
  such as using win32com from linux
- accessing resources (files etc) on another box


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

The asynchronous (non-blocking) version runs the function as a separate process 
on the remote server and supports simple job management functions (join and kill).

::

    from remotely import RemoteClient
    rc = RemoteClient("API_KEY", SERVER, PORT)
    pid = rc.run(foo, arg1, arg2=key2)
    output = rc.join(pid)
    output = rc.kill(pid)

