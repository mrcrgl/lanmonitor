lanmonitor
==========

Simple Django app to record network activity on a Raspberry

----------

I'd like to track tcp connections on my home network. Just interested 
in those things which slow down my mobile phone or what type of 
important task is my computer doing while in stand-by.

# Environment

I have a RaspberryPi with wifi, already configured as access point at home.

Todo:
- Set up dnsmasq with log-queries enabled (get *requested* domain name)
- Configure DHCPD for clients
- Capture packets
-- `tcpdump -n 'tcp[13]=18'` will return all SYNACK packets (should be fine)
- GeoIP to determine the server location
- Simple frontend to display the data
