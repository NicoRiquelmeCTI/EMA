#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Blog: https://peppe8o.com
# Date: Sep 17th, 2022
# Version: 1.0

# Python3 script to interface basic Blynk rest API with Raspberry PI

import requests

token="TXxZCeqcfno9bau_hf-J9MUM2NU2HR0N"

def write(token,pin,value):
	api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
	response = requests.get(api_url)
	if "200" in str(response):
		print("Value successfully updated")
	else:
		print("Could not find the device token or wrong pin format")

def read(token,pin):
	api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
	response = requests.get(api_url)
	return response.content.decode()

while True:
	# Example: write the virtual PIN v1 to set it to 100:
	write(token,"v13","190")



