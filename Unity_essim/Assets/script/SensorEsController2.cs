using UnityEngine;
//using System.IO.Ports;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;

[System.Serializable]
public class AxleInfo_ses {
    public WheelCollider Wheel;
    public bool motor;
    public bool steering;
}
     
public class SensorEsController : MonoBehaviour {
    public List<AxleInfo_ses> AxleInfo_sess; 
    public float maxMotorTorque;
    public float maxSteeringAngle;

    // Communication with Arduino
    //SerialPort data_stream = new SerialPort("/dev/cu.usbmodem21101", 115200);
    //public string receivedstring;



     
    // 対応する視覚的なホイールを見つけます
    // Transform を正しく適用します
    public void ApplyLocalPositionToVisuals(WheelCollider collider)
    {
        if (collider.transform.childCount == 0) {
            return;
        }
     
        Transform visualWheel = collider.transform.GetChild(0);
     
        Vector3 position;
        Quaternion rotation;
        collider.GetWorldPose(out position, out rotation);
     
        visualWheel.transform.position = position;
        visualWheel.transform.rotation = rotation;
    }
     
    public void FixedUpdate()
    {
        float motor = maxMotorTorque * Input.GetAxis("Vertical");
        float steering = maxSteeringAngle * Input.GetAxis("Horizontal");

        /*receivedstring = data_stream.ReadLine();
        string[] datas = receivedstring.Split(',');
        movementX = float.Parse(datas[0]);
        movementY = float.Parse(datas[1]);

        float motor = maxMotorTorque * movementX;
        float steering = maxSteeringAngle * movementY;
        */

     
        foreach (AxleInfo_ses AxleInfo_ses in AxleInfo_sess) {
            if (AxleInfo_ses.steering) {
                AxleInfo_ses.Wheel.steerAngle = steering;
            }
            if (AxleInfo_ses.motor) {
                AxleInfo_ses.Wheel.motorTorque = motor;
            }
            ApplyLocalPositionToVisuals(AxleInfo_ses.Wheel);
        }
    }
}