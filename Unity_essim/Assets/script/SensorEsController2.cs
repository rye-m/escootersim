// using UnityEngine;
// //using System.IO.Ports;
// using System.Collections;
// using System.Collections.Generic;
// using Unity.VisualScripting;

// [System.Serializable]
// public class AxleInfo_ses {
//     public WheelCollider Wheel;
//     public bool motor;
//     public bool steering;
// }
     
// public class SensorEsController : MonoBehaviour {
//     public List<AxleInfo_ses> AxleInfo_sess; 
//     public float maxMotorTorque;
//     public float maxSteeringAngle;

//     // Communication with Arduino
//     //SerialPort data_stream = new SerialPort("/dev/cu.usbmodem21101", 115200);
//     //public string receivedstring;



     
//     // 対応する視覚的なホイールを見つけます
//     // Transform を正しく適用します
//     public void ApplyLocalPositionToVisuals(WheelCollider collider)
//     {
//         if (collider.transform.childCount == 0) {
//             return;
//         }
     
//         Transform visualWheel = collider.transform.GetChild(0);
     
//         Vector3 position;
//         Quaternion rotation;
//         collider.GetWorldPose(out position, out rotation);
     
//         visualWheel.transform.position = position;
//         visualWheel.transform.rotation = rotation;
//     }
     
//     public void FixedUpdate()
//     {
//         float motor = maxMotorTorque * Input.GetAxis("Vertical");
//         float steering = maxSteeringAngle * Input.GetAxis("Horizontal");

//         /*receivedstring = data_stream.ReadLine();
//         string[] datas = receivedstring.Split(',');
//         movementX = float.Parse(datas[0]);
//         movementY = float.Parse(datas[1]);

//         float motor = maxMotorTorque * movementX;
//         float steering = maxSteeringAngle * movementY;
//         */

     
//         foreach (AxleInfo_ses AxleInfo_ses in AxleInfo_sess) {
//             if (AxleInfo_ses.steering) {
//                 AxleInfo_ses.Wheel.steerAngle = steering;
//             }
//             if (AxleInfo_ses.motor) {
//                 AxleInfo_ses.Wheel.motorTorque = motor;
//             }
//             ApplyLocalPositionToVisuals(AxleInfo_ses.Wheel);
//         }
//     }
// }

// using UnityEngine;
// using System.IO.Ports;
// using System.Collections;
// using System.Collections.Generic;
// using Unity.VisualScripting;

// [System.Serializable]
// public class AxleInfo_es
// {
//     public WheelCollider Wheel;
//     public bool motor;
//     public bool steering;
// }

// public class SimpleEsController : MonoBehaviour
// {
//     public List<AxleInfo_es> AxleInfo_ess;
//     public float maxMotorTorque;
//     public float maxSteeringAngle;

//     // Movement along X and Y axes.
//     public float movementX;
//     public float movementY;

//     // Communication with Arduino
//     SerialPort data_stream = new SerialPort("/dev/cu.usbmodem1401", 115200);
//     public string receivedstring;
//     public bool running = false;
//     void Start()
//     {
//         running = true;

//         // ListAvailablePorts();
//         StartCoroutine(GetSerialData());
//     }

//     void OnDestroy()
//     {
//         running = false;
//     }

//     // 対応する視覚的なホイールを見つけます
//     // Transform を正しく適用します
//     public void ApplyLocalPositionToVisuals(WheelCollider collider)
//     {
//         if (collider.transform.childCount == 0)
//         {
//             return;
//         }

//         Transform visualWheel = collider.transform.GetChild(0);

//         Vector3 position;
//         Quaternion rotation;
//         collider.GetWorldPose(out position, out rotation);

//         visualWheel.transform.position = position;
//         visualWheel.transform.rotation = rotation;
//     }

//     public void Update()
//     {
//         // float motor = maxMotorTorque * Input.GetAxis("Vertical");
//         // float steering = maxSteeringAngle * Input.GetAxis("Horizontal");



//         float motor = maxMotorTorque * movementX;
//         float steering = maxSteeringAngle * movementY;
//         Debug.Log("debug:" + movementX + ", " + movementY);


//         foreach (AxleInfo_es AxleInfo_es in AxleInfo_ess)
//         {
//             if (AxleInfo_es.steering)
//             {
//                 AxleInfo_es.Wheel.steerAngle = steering;
//             }
//             if (AxleInfo_es.motor)
//             {
//                 AxleInfo_es.Wheel.motorTorque = motor;
//             }
//             ApplyLocalPositionToVisuals(AxleInfo_es.Wheel);
//         }
//     }

//     void ListAvailablePorts()
//     {
//         string[] ports = SerialPort.GetPortNames();
//         Debug.Log("Available Ports:");
//         foreach (string port in ports)
//         {
//             Debug.Log(port);
//         }
//     }

//     IEnumerator GetSerialData()
//     {

//         data_stream.Open();
//         Debug.Log("startCorutine");
//         while (running)
//         {
//         Debug.Log(data_stream.BytesToRead);
//             while (data_stream.BytesToRead > 0)
//             {
//                 receivedstring = data_stream.ReadLine();
//                 if (receivedstring.Length == 0) continue;
//                 string[] datas = receivedstring.Split(',');
//                 if (datas.Length != 2) continue;
//                 float.TryParse(datas[0], out movementX);
//                 float.TryParse(datas[1], out movementY);
//         Debug.Log("debug:" + movementX + ", " + movementY);
//             }

//             yield return null;
//         }
//         data_stream.Close();
//     }
// }

// using UnityEngine;
// using System.IO.Ports;
// using System.Collections;
// using System.Collections.Generic;
// using Unity.VisualScripting;

// [System.Serializable]
// public class AxleInfo_ses {
//     public WheelCollider Wheel;
//     public bool motor;
//     public bool steering;
// }


// public class SimpleEsController : MonoBehaviour {
//     public List<AxleInfo_ses> AxleInfo_sess; 
//     public float maxMotorTorque;
//     public float maxSteeringAngle;

//     // Communication with Arduino
//     SerialPort data_stream = new SerialPort("/dev/cu.usbmodem1401", 115200);
//     public string receivedstring;

//     // Movement along X and Y axes.
//     public float movementX;
//     public float movementY;

//     void Start(){
//         data_stream.Open();
//     }
     
//     // 対応する視覚的なホイールを見つけます
//     // Transform を正しく適用します
//     public void ApplyLocalPositionToVisuals(WheelCollider collider)
//     {
//         if (collider.transform.childCount == 0) {
//             return;
//         }
     
//         Transform visualWheel = collider.transform.GetChild(0);
     
//         Vector3 position;
//         Quaternion rotation;
//         collider.GetWorldPose(out position, out rotation);
     
//         visualWheel.transform.position = position;
//         visualWheel.transform.rotation = rotation;
//     }
     
//     public void FixedUpdate()
//     {
//         // float motor = maxMotorTorque * Input.GetAxis("Vertical");
//         // float steering = maxSteeringAngle * Input.GetAxis("Horizontal");
//         receivedstring = data_stream.ReadLine();
//         string[] datas = receivedstring.Split(',');
//         movementX = float.Parse(datas[0]);
//         movementY = float.Parse(datas[1]);

//         float motor = maxMotorTorque * movementX;
//         float steering = maxSteeringAngle * movementY;
        
//         Debug.Log("debug:" + movementX + ", " + movementY);

     
//         foreach (AxleInfo_ses AxleInfo_ses in AxleInfo_sess) {
//             if (AxleInfo_ses.steering) {
//                 AxleInfo_ses.Wheel.steerAngle = steering;
//             }
//             if (AxleInfo_ses.motor) {
//                 AxleInfo_ses.Wheel.motorTorque = motor;
//             }
//             ApplyLocalPositionToVisuals(AxleInfo_ses.Wheel);
//         }
//     }
// }