using UnityEngine;
using System.IO.Ports;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;

[System.Serializable]
public class AxleInfo_es
{
    public WheelCollider Wheel;
    public bool motor;
    public bool steering;
}

public class SimpleEsController : MonoBehaviour
{
    public List<AxleInfo_es> AxleInfo_ess;
    public float maxMotorTorque;
    public float maxSteeringAngle;

    // Movement along X and Y axes.
    public float accellation;
    public float brake;
    public float movementX;
    public float movementY;

    // Communication with Arduino
    SerialPort data_stream = new SerialPort("/dev/cu.usbmodem1201", 115200);
    public string receivedstring;
    public bool running = false;
    void Start()
    {
        running = true;

        // ListAvailablePorts();
        // StartCoroutine(GetSerialData());
    }

    void OnDestroy()
    {
        running = false;
    }

    // 対応する視覚的なホイールを見つけます
    // Transform を正しく適用します
    public void ApplyLocalPositionToVisuals(WheelCollider collider)
    {
        if (collider.transform.childCount == 0)
        {
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



        // float motor = maxMotorTorque * movementX;
        // float steering = maxSteeringAngle * movementY;
        Debug.Log("debug:" + accellation + ", " + brake + ", " + movementX + ", " + movementY);


        foreach (AxleInfo_es AxleInfo_es in AxleInfo_ess)
        {
            if (AxleInfo_es.steering)
            {
                AxleInfo_es.Wheel.steerAngle = steering;
            }
            if (AxleInfo_es.motor)
            {
                AxleInfo_es.Wheel.motorTorque = motor;
            }
            ApplyLocalPositionToVisuals(AxleInfo_es.Wheel);
        }
    }

    void ListAvailablePorts()
    {
        string[] ports = SerialPort.GetPortNames();
        Debug.Log("Available Ports:");
        foreach (string port in ports)
        {
            Debug.Log(port);
        }
    }

    IEnumerator GetSerialData()
    {
        data_stream.RtsEnable = true;
        data_stream.DtrEnable = true;
        
        data_stream.Open();
        Debug.Log("startCorutine");
        while (running)
        {
        // Debug.Log(data_stream.BytesToRead);
            while (data_stream.BytesToRead > 0)
            {
                receivedstring = data_stream.ReadLine();
                if (receivedstring.Length == 0) continue;
                string[] datas = receivedstring.Split(',');
                if (datas.Length != 3) continue;
                float.TryParse(datas[0], out accellation);
                float.TryParse(datas[1], out brake);
                float.TryParse(datas[2], out movementY);

                movementX = accellation - brake > 0? accellation - brake : 0;
        // Debug.Log("debug:" + movementX + ", " + movementY);
            }

            yield return null;
        }
        data_stream.Close();
    }
}