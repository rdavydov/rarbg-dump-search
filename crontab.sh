service cron start
crontab -l > mycron
echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> mycron # not always needed, depends on your system

# The 2>&1 at the end of the command redirects the standard error (stderr) output to the same location as the standard output (stdout).
# With the >> redirection operator used in the command (>> /path/to/uvicorn.log), the output will be appended to the existing log file each time the command is executed.
# In this expression, */12 in the second field means "every 12 hours".
# The pkill -f command sends a signal to the process to terminate it.
# By default, pkill sends the SIGTERM signal, which allows the process to perform a graceful shutdown by handling the signal and cleaning up resources before exiting.

echo "0 */12 * * * /root/rarbg-dump/restart.sh" >> mycron

crontab mycron
rm mycron