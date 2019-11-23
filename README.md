To start run 'bash build.sh environ' (supported environments are dev and prod)
This command builds the python scripts into a zip file, makes the zip executable, then runs it in the background and persists the process even when the session closes
To stop run 'ps -ef | grep discordbot' to find the process id, then 'kill -9 PID' to stop it.
Or type $stop in the correct discord channel.

Many of the design and interface decisions made in the code were made to reduce clutter,
such as deleting some messages once they've served their purpose, and limiting some commands to the mod/admin channel

Required Files/Folders:
config: Stores all of the start config settings(including the key required to start the bot). This cannot be changed at runtime so if it is changed the program must be
restarted. It also supports any custom environment if you also pass it as an argument on start. An example is provided in config-example.
client_secret.json: Stores the key used to connect to the Google Sheet API. You will need to create your own as free access has limited bandwidth.
files/: This folder contains the files that can be created and modified at runtime.


