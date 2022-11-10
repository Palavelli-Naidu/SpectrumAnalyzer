 const int x=1024; // 2^13
int data[x];


void setup()
{
  Serial.begin(115200);
}

void loop() 
{
  
    for(int i=0;i<x;i++)
    {
      data[i]=analogRead(A0);
     
      
    }

    for(int i=0;i<x;i++)
    {
     Serial.println(data[i]); 
    }
  
  delay(5000);
  }
