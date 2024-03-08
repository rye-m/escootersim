using UnityEngine;
using System.IO.Ports;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;

[System.Serializable]
public class AxleInfo_es {
    public WheelCollider Wheel;
    public bool motor;
    public bool steering;
}
     
public class SimpleEsController : MonoBehaviour {
    public List<AxleInfo_es> AxleInfo_ess; 
    public float maxMotorTorque;
    public float maxSteeringAngle;

    // Movement along X and Y axes.
    private float movementX;
    private float movementY;

    // Communication with Arduino
    SerialPort data_stream = new SerialPort("/dev/cu.usbmodem1101", 115200);
    public string receivedstring;

    void Start()
        {
            data_stream.Open(); //Initiate the Serial stream
        }


     
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
     
    public void Update()
    {
        float motor = maxMotorTorque * Input.GetAxis("Vertical");
        float steering = maxSteeringAngle * Input.GetAxis("Horizontal");

        receivedstring = data_stream.ReadLine();
        string[] datas = receivedstring.Split(',');
        movementX = float.Parse(datas[0]);
        movementY = float.Parse(datas[1]);

        //float motor = maxMotorTorque * movementX;
        //float steering = maxSteeringAngle * movementY;
        //Debug.Log("debug:" + movementX + ", " + movementY);

     
        foreach (AxleInfo_es AxleInfo_es in AxleInfo_ess) {
            if (AxleInfo_es.steering) {
                AxleInfo_es.Wheel.steerAngle = steering;
            }
            if (AxleInfo_es.motor) {
                AxleInfo_es.Wheel.motorTorque = motor;
            }
            ApplyLocalPositionToVisuals(AxleInfo_es.Wheel);
        }
    }
}