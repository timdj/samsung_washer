### Getting token from Samsung Ecobubble washer

#### Connect to wifi
First connect your washer to wifi by using the Samsung Smarthings. I couldn't get mine to work in there because it failed after connecting. It was however connected to the wifi
 
#### Get samsung client certificate 
This can be retrieved by decompiling the samsung android. However someone else has already done the hard work and you can find **ac14k_m.pem** at

https://github.com/cicciovo/homebridge-samsung-airconditioner

or
 
https://github.com/SebuZet/samsungrac/tree/master/custom_components/climate_ip
 
#### Start listening at port 8889
To retrieve a token we need to request one from the washer trough port 8888.
It will return a token to port 8889. We need the client ssl 

use server.py to start a listening server on port 8889 and leave this terminal open

```
python3 server.py
```

#### Request a new device token
1. Turn on washer and make sure it is connected to the wifi
2. In another terminal send a token request 
    ```
    curl -k -H "Content-Type: application/json" -H "DeviceToken: xxxxxxxxxxx" --cert ac14k_m.pem --insecure -X POST https://192.168.XXX.XXX:8888/devicetoken/request 
    ```
3. Press smart control button on washer

You should now receive a token back in your terminal. If this doesn't work try turning the washer off and on in between step 2 and 3

#### Test the token
```
curl -k -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR NEW TOKEN>" --cert ac14k_m.pem --insecure -X GET https://192.168.xxx.xxx:8888/devices/0
```

#### Hassio
In home assistant I use the following configuration to be able to get a notification when the washer is done.
```
- platform: command_line
  command: 'curl -m 8 -k -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR NEW TOKEN>" --cert /config/ac14k_m.pem --insecure -X GET https://192.168.XXX.XXX:8888/devices/0/operation'
  name: "Samsung washer"
  value_template: '{{ value_json.Operation.state }}'
```

##### Credits.
Most of this info I got trough the work on samsungAC at
https://github.com/openhab/openhab1-addons/issues/2863
