# Lab 5 on Network Programming 
<br/>
## Elaborarea unei aplicații Client - Server cu scopul studierii protocolului de la nivelul de transport - TCP.

### Comenzile acceptate de server
Comenzile obligatorii care trebuie să le implementeze serverul:

* /help - răspunde cu o listă a comenzilor suportate și o descriere a fiecărei comenzi;
* /hello Text - raspunde cu textul care a fost expediat ca paremetru<
* alte 3 comenzi cu funcțional diferit (e.g. timpul curent, generator de cifre, flip the coin etc)

### Cerințe pentru sistem
Cerințele de bază pentru aplicație sunt:

* O aplicație client care se conectează la server și permite transmiterea comenzilor;
* Comenzile sunt introduse de utilizator de la tastatură;
* Răspunsul primit de la server este afișat utilizatorului.
* O aplicație server care:
  * Acceptă conexiunea de la client la un careva port;
  * Primește comenzile de la client;
  * Transmite un răspuns clientului.

