To start run 'bash build.sh environ' (supported environments are dev and prod)
This command builds the python scripts into a zip file, makes the zip executable, then runs it in the background and persists the process even when the session closes
To stop run 'ps -ef | grep discordbot' to find the process id, then 'kill -9 PID' to stop it.
Or type $stop in the correct discord channel.

Many of the design and interface decisions made in the code were made to reduce clutter,
such as deleting some messages once they've served their purpose, and limiting some commands to the mod/admin channel
