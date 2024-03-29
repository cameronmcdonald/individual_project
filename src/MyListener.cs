using System;
using System.Net;
using System.Net.Sockets;
using UnityEngine;

public class MyListener : MonoBehaviour
{
    public GameObject objectToMove;  // Reference to your 3D object in Unity

    private UdpClient udpClient;
    private IPEndPoint endPoint;

    void Start()
    {
        // Set up the UDP client to receive data
        udpClient = new UdpClient(25001);
        endPoint = new IPEndPoint(IPAddress.Any, 0);
    }

    void Update()
    {
        try
        {
            // Receive the 3D position data from the UDP socket
            byte[] receivedData = udpClient.Receive(ref endPoint);
            Vector3 newPosition = BytesToVector3(receivedData);

            // Update the position of the 3D object in Unity
            objectToMove.transform.position = newPosition;
        }
        catch (Exception e)
        {
            Debug.LogError("Error receiving data: " + e.Message);
        }
    }

    // Convert byte array to Vector3
    private Vector3 BytesToVector3(byte[] bytes)
    {
        float x = BitConverter.ToSingle(bytes, 0);
        float y = BitConverter.ToSingle(bytes, 4);
        float z = BitConverter.ToSingle(bytes, 8);
        return new Vector3(x, y, z);
    }

    void OnApplicationQuit()
    {
        // Close the UDP client when the application quits
        udpClient.Close();
    }
}