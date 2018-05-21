# Lab 6 on Network Programming 
## Objectives
* Studying the UDP transport protocol and comparing it with TCP;
* Studying the methods of capturing data transmitted over the network and analyzing them;
* Developing a client application to work with an existing application.
## Implementation of the tasks
In order to elaborate this laboratory work, Wireshark application has been used. Wireshark is a widely-used network protocol analyzer. Once Wireshark and two different instances of the chat application have been launched, I have firstly identified the packages. In order to do that, I have used a filter: `udp.port == 42424`. 
![alt text](https://github.com/victoriagalanciuc/PR-labs/blob/master/Lab%20%236/img/screenshot_1.png "Screenshot")
<br>
Now that we have identified our packages, it's time to start analyzing them. When a user logs in, we have the following package structure: <br>
![alt text](https://github.com/victoriagalanciuc/PR-labs/blob/master/Lab%20%236/img/screenshot_2.png "Screenshot") 
<br>
Actually, what we can see is the hexadecimal representation of the package content on the left side and the ASCII representation on the right side. Using a Base64 decoder, I was able to convert the data and once I did, what I obtained looked like this: <br>
`1526929006079|c3709f0a-a827-4803-bfd9-f7e8a00b5c41|:all|ezp0eXBlIDpvbmxpbmUsIDp1c2VybmFtZSAidm9sZGVtb3J0In0=` <br>
Now looking into the data that I have obtained after decoding, I have noticed that it is made from more parts separated by a vertical line.
* `1526929006079` -> Mon May 21 2018 18:56:46 <br>
* `c3709f0a-a827-4803-bfd9-f7e8a00b5c41` : UUID (universally unique identifier)assigned to the logged user.
* `:all` : When a new user logs in, "all" other users see the new one. This field is a filter that ensures that the package that has been received has to be broadcasted to all the connected users.
* `ezp0eXBlIDpvbmxpbmUsIDp1c2VybmFtZSAidm9sZGVtb3J0In0=`: Once I decoded this part (again) I have obtained: `{:type :online, :username "voldemort"}`  