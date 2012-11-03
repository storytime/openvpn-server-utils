OpenVPN-auth
------------

### 1.0   Set the next parameters at your server config file:
    auth-user-pass-verify "/etc/openvpn/openvp_auth.py -v 1 -a" via-file
    script-security 2 

### 2.0   Then change the next parameter USERS_FILE in openvp_auth.py:  
    USERS_FILE = "/etc/openvpn/users"  # user name and password hash will be store here (format - username:hash)

### 3.0 After that execute the script(openvp_auth.py) with the next parameters: -v1 -g user:login
    ./openvp_auth.py -v1 -g user_test:qwerty

### 4. Use credentials from step 3, for OpenVPN clients authentication via user name and password.
4.1 Add to OpenVPN clients configure file the next string:  

    auth-user-pass /path/to/file/with/username_and_password 

4.2 File format:

    cat /path/to/file/with/username_and_password
    ---------------------------------------------------------
    user_test
    qwerty
    ---------------------------------------------------------

### 5.0 Default log file location:
    ---------------------------------------------------------
    /var/log/openvputils.log
    ---------------------------------------------------------