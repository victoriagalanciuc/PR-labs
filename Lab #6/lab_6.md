# Lab 6 on Network Programming 
## Objectives
* Studying the UDP transport protocol and comparing it with TCP;
* Studying the methods of capturing data transmitted over the network and analyzing them;
* Developing a client application to work with an existing application.
## Implementation of the tasks
In order to elaborate this laboratory work, Wireshark application has been used. Wireshark is a widely-used network protocol analyzer. Once Wireshark and two different instances of the chat application have been launched, I have firstly identified the packages. In order to do that, I have used a filter: `udp.port == 42424`