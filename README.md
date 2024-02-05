# Govee Control

Super simple GUI for my Govee Lights using `PySimpleGUI`.

* I've attached a MacOS application that just runs a script that runs the gui so it can go on the dock. The script sources the virtual environment then runs the Python script.
	* You need the virtual environment for the script to work.
* You also need an API key. The contents of `api_key.toml` should look like:

```
key = "API KEY HERE"
```
* Unfortunately there's pretty strict rate limiting of 10 requests per minute. You'll probably hit the rate limit often in testing, but in practice its okay. Hopefully they change this eventually.

## Dependencies
```
requests
PySimpleGUI
```