# Lab 6 on Network Programming 
## Objectives
* Studying the UDP transport protocol and comparing it with TCP;
* Studying the methods of capturing data transmitted over the network and analyzing them;
* Developing a client application to work with an existing application.
## Implementation of the tasks
In order to elaborate this laboratory work, Wireshark application has been used. Wireshark is a widely-used network protocol analyzer. Once Wireshark and two different instances of the chat application have been launched, I have firstly identified the packages. In order to do that, I have used a filter: `udp.port == 42424`. <br><br>
![alt text](https://github.com/victoriagalanciuc/PR-labs/blob/master/Lab%20%236/img/screenshot_1.png "Screenshot")
<br><br>
Now that we have identified our packages, it's time to start analyzing them. When a user logs in, we have the following package structure: <br><br>
![alt text](https://github.com/victoriagalanciuc/PR-labs/blob/master/Lab%20%236/img/screenshot_2.png "Screenshot") 
<br>
Actually, what we can see is the hexadecimal representation of the package content on the left side and the ASCII representation on the right side. Using a Base64 decoder, I was able to convert the data and once I did, what I obtained looked like this: <br>
`1526929006079|c3709f0a-a827-4803-bfd9-f7e8a00b5c41|:all|ezp0eXBlIDpvbmxpbmUsIDp1c2VybmFtZSAidm9sZGVtb3J0In0=` <br>
Now looking into the data that I have obtained after decoding, I have noticed that it is made from more parts separated by a vertical line.
* `1526929006079` -> Mon May 21 2018 18:56:46 <br>
* `c3709f0a-a827-4803-bfd9-f7e8a00b5c41` : UUID (universally unique identifier)assigned to the logged user.
* `:all` : When a new user logs in, "all" other users see the new one. This field is a filter that ensures that the package that has been received has to be broadcasted to all the connected users.
* `ezp0eXBlIDpvbmxpbmUsIDp1c2VybmFtZSAidm9sZGVtb3J0In0=`: Once I decoded this part (again) I have obtained: `{:type :online, :username "voldemort"}`  <br>
Now, when we send a message, we can see two new packages, because one message is the message sent to the user and the second one is the response from the user that he received the message. Following the same procedure as above, we have obtained the decoded data: <br>
`1526931838792|0cdfebca-02fe-4fa5-acdc-9941fa2937ff|f0907c64-81b0-4ad7-9dc5-4ad4edde83e7|ezp0eXBlIDpjaGF0LCA6dHh0ICJhYnJhY2FkYWJyYSJ9`, which could be easily analyzed (since we have already done that before). Just like in the previous step, the result is composed from more parts, the last one having to be decoded again. 
* `1526931838792` -> Mon May 21 2018 19:43:58
* `0cdfebca-02fe-4fa5-acdc-9941fa2937ff` : sender UUID 
* `f0907c64-81b0-4ad7-9dc5-4ad4edde83e7` : receiver UUID
* `ezp0eXBlIDpjaGF0LCA6dHh0ICJhYnJhY2FkYWJyYSJ9`, when decoded results in: `{:type :chat, :txt "abracadabra"}` aka the message that had been sent.
Finally, when we decode the second package, we obtain the same structure, only when we decode the last part we obtain the status of delivery: `{:type :delivered}` <br> <br>
![alt text](https://github.com/victoriagalanciuc/PR-labs/blob/master/Lab%20%236/img/screenshot_3.png "Screenshot") 

