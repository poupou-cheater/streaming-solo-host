to use it on all the wifi you need 


netstat -an | findstr :8000
netsh advfirewall firewall add rule name="Flask Web Host 8000" dir=in action=allow protocol=TCP localport=8000 profile=private
netsh advfirewall firewall add rule name="Flask Web Host 8000 Public" dir=in action=allow protocol=TCP localport=8000 profile=public