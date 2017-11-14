/*
  Simple POST client for ArduinoHttpClient library
  Connects to server once every five seconds, sends a POST request
  and a request body

 

  created 14 Feb 2016
  by Tom Igoe
  
  this example is in the public domain
 */
#include <ArduinoHttpClient.h>
#include <WiFi101.h>
#include "arduino_secrets.h"

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
/////// Wifi Settings ///////
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;


char serverAddress[] = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze";  // server address
int port = 80;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;
String response;
int statusCode = 0;

void setup() {
  Serial.begin(9600);
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
  }

  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void loop() {
  Serial.println("making POST request");
  //client.sendHeader("Content-Type", "application/json");
  client.sendHeader("accept", "application/json");
  client.sendHeader("user-agent", "watson-developer-cloud-python-0.26.1");
  client.sendHeader("Authorization", "Basic N2NhZjJhNWYtYjQzZi00MTc5LWJjYWYtNDhjNjM5MDI2ZDk5Ong3MTVhQnZ3MWFZQw==");
  String contentType = "application/json";
  String postData = "{\"fallback_to_raw\": true, \"text\": \"Hello World!\", \"clean\": true, \"return_analyzed_text\": false, \"features\": {\"emotion\": {}}}";

  client.post("?version=2017-02-27", contentType, postData);

  // read the status code and body of the response
  statusCode = client.responseStatusCode();
  response = client.responseBody();

  Serial.print("Status code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);

  Serial.println("Wait five seconds");
  delay(5000);
}
