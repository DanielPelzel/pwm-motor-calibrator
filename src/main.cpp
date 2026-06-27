#include <Arduino.h>
#include "config.h"


int currentFreq = PWM_FREQ;
int currentRes = PWM_RES;


void setup() {
    Serial.begin(115200);
    ledcSetup(PWM_CH_A, PWM_FREQ, PWM_RES);
    ledcAttachPin(ENA, PWM_CH_A);

    pinMode(In1, OUTPUT);
    pinMode(In2, OUTPUT);

    digitalWrite(In1, HIGH);
    digitalWrite(In2, LOW);

}

void loop() {
    if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n');

        if (cmd.startsWith("PWM:")) {
            int value = cmd.substring(4).toInt();
            ledcWrite(PWM_CH_A, value);
        }
        else if (cmd.startsWith("FREQ:")) {
            int freq = cmd.substring(5).toInt();
            ledcSetup(PWM_CH_A, freq, currentRes);
            currentFreq = freq;
        }
        else if (cmd.startsWith("RES:")) {
            int res = cmd.substring(4).toInt();
            ledcSetup(PWM_CH_A, currentFreq, res);
            currentRes = res;
        }


        }

    }


