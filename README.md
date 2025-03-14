# Network Simulator for Reliable Data Transmission

This project implements a **network simulator** for two fundamental **reliable data transfer protocols**: **Stop-and-Wait** and **Go-Back-N**. The simulator introduces **packet loss and corruption** to mimic real-world network behavior and tests how these protocols handle retransmissions and acknowledgments.

## Quickstart Guide

### Running the Simulator
1. Copy all the contents from this repository.
2. Open a terminal and navigate to the folder containing `network_simulator.py`.
3. Run the program using:
   ```bash
   python network_simulator.py
   ```
4. You will be prompted to select a protocol:
   - Enter **1** for **Stop-and-Wait**
   - Enter **2** for **Go-Back-N**

### How It Works
- **Stop-and-Wait Protocol**: Sends one packet at a time and waits for an acknowledgment before sending the next.
- **Go-Back-N Protocol**: Uses a sliding window to send multiple packets before requiring an acknowledgment.

## Core Concepts
- **Packet Loss & Corruption**: Randomly simulated to test protocol robustness.
- **Timeout Handling**: Ensures retransmissions if packets are lost.
- **Acknowledgments (ACKs) and Negative Acknowledgments (NACKs)**: Used for communication between sender and receiver.

## Preview of Protocol Behavior

### **Stop-and-Wait**
- Sends a packet and waits for an acknowledgment.
- Retransmits if an acknowledgment is lost or corrupted.
- Uses a simple **0/1 sequence number** system.

### **Go-Back-N**
- Uses a **window size** to send multiple packets before requiring an acknowledgment.
- If an error occurs, the sender retransmits the entire window.

## Notes:
- This simulator is useful for understanding **reliable data transfer** in networking.
- The implementation can be extended to **Selective Repeat** or **TCP-like mechanisms**.

## Example Usage
```bash
Select the protocol to test:
1. Stop-and-Wait
2. Go-Back-N
Enter 1 or 2: 1
=== Testing Stop-and-Wait Protocol ===
[Sender][Stop-and-Wait] Sending: Packet(seq=0, data=Message 1)
[Receiver][Stop-and-Wait] Received expected packet: Packet(seq=0, data=Message 1). Sending ACK.
[Sender][Stop-and-Wait] Received ACK: ACK(0). Moving to next packet.
...
```

## Future Enhancements
- Implement **Selective Repeat** for better error handling.
- Add **Graphical Visualization** to illustrate packet flow.
- Integrate **real network sockets** for client-server testing.

---



