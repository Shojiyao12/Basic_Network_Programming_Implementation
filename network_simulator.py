import random
import time

# Set probabilities for packet loss and corruption
PACKET_LOSS_PROB = 0.6
PACKET_CORRUPT_PROB = 0.6
TIMEOUT = 2
WINDOW_SIZE = 4
TOTAL_PACKETS = 10

def simulate_packet_loss_or_corruption():
    loss = random.random()
    corrupt = random.random()

    if loss > corrupt:
        if loss > PACKET_LOSS_PROB:
            return "loss"
    elif corrupt > loss:
        if corrupt > PACKET_CORRUPT_PROB:
            return "corruption"
    return None

def simulate_timeout():
    time.sleep(TIMEOUT)

# Packet class
class Packet:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data

    def __repr__(self):
        return f"Packet(seq={self.seq_num}, data={self.data})"

# ==========================
# Stop-and-Wait Protocol
# ==========================

# Stop-and-Wait Sender
class StopAndWaitSender:
    def __init__(self):
        self.seq_num = 0

    def send_packet(self, packet):
        print(f"[Sender][Stop-and-Wait] Sending: {packet}")
        return packet

    def receive_ack(self, ack_num):
        outcome = simulate_packet_loss_or_corruption()
        if outcome == "corruption":
            print(f"[Network] ACK corrupted: ACK({ack_num})")
            # Now print the corrupted ACK value properly instead of None
            print(f"[Sender][Stop-and-Wait] Received corrupted or wrong ACK: ACK({ack_num}). Retransmitting...")
            return False  # Simulate wrong ACK
        elif ack_num == self.seq_num:
            print(f"[Sender][Stop-and-Wait] Received ACK: ACK({ack_num}). Moving to next packet.")
            self.seq_num = 1 - self.seq_num  # Toggle sequence number between 0 and 1
            return True
        else:
            print(f"[Sender][Stop-and-Wait] Received corrupted or wrong ACK: ACK({ack_num}). Retransmitting...")
            return False

# Stop-and-Wait Receiver
class StopAndWaitReceiver:
    def __init__(self):
        self.expected_seq_num = 0

    def receive_packet(self, packet):
        outcome = simulate_packet_loss_or_corruption()
        if outcome == "loss":
            print(f"[Network] Packet lost: {packet}")
            return None
        elif outcome == "corruption":
            print(f"[Network] Packet corrupted: {packet}")
            return None

        if packet.seq_num == self.expected_seq_num:
            print(f"[Receiver][Stop-and-Wait] Received expected packet: {packet}. Sending ACK.")
            ack_num = packet.seq_num
            self.expected_seq_num = 1 - self.expected_seq_num  # Toggle between 0 and 1
            return ack_num
        else:
            print(f"[Receiver][Stop-and-Wait] Received out-of-order packet: {packet}. Sending NACK.")
            return 1 - self.expected_seq_num  # Send NACK (opposite of the expected seq num)

# Stop-and-Wait Protocol Logic
class StopAndWaitProtocol:
    def __init__(self):
        self.sender = StopAndWaitSender()
        self.receiver = StopAndWaitReceiver()

    def run(self):
        for i in range(TOTAL_PACKETS):
            packet = Packet(self.sender.seq_num, f"Message {i + 1}")
            sent_packet = self.sender.send_packet(packet)

            ack_num = self.receiver.receive_packet(sent_packet)
            if ack_num is None:
                print(f"[Sender][Stop-and-Wait] Timeout waiting for ACK. Retransmitting: {packet}")
                simulate_timeout()
                sent_packet = self.sender.send_packet(packet)
                ack_num = self.receiver.receive_packet(sent_packet)

            if ack_num is not None:
                ack_received = self.sender.receive_ack(ack_num)
                if not ack_received:
                    simulate_timeout()
                    sent_packet = self.sender.send_packet(packet)
                    ack_num = self.receiver.receive_packet(sent_packet)
                    self.sender.receive_ack(ack_num)

# ==========================
# Go-Back-N Protocol
# ==========================

# Go-Back-N Sender
class GoBackNSender:
    def __init__(self):
        self.base = 0
        self.next_seq_num = 0
        self.window_size = WINDOW_SIZE
        self.total_packets = TOTAL_PACKETS
        self.packets = [Packet(seq_num, f"Message {seq_num + 1}") for seq_num in range(self.total_packets)]
        self.timers = {}

    def send_packet(self, packet, resend = 0):
        if (resend == 1):
            print(f"[Sender][GBN] Resending: {packet}")
        else:
            print(f"[Sender][GBN] Sending: {packet}")
        self.timers[packet.seq_num] = time.time()

    def resend_window(self):
        print(f"[Sender][GBN] Retransmitting window starting at seq {self.base}")
        for seq_num in range(self.base, min(self.base + self.window_size, self.total_packets)):
            packet = self.packets[seq_num]
            self.send_packet(packet, 1)

    def receive_ack(self, ack_num):
        outcome = simulate_packet_loss_or_corruption()
        if outcome == "corruption":
            print(f"[Network] ACK corrupted: ACK({ack_num})")
            print(f"[Sender][GBN] Received corrupted ACK. Retransmitting window.")
            self.resend_window()
            return
        elif ack_num >= self.base:
            print(f"[Sender][GBN] Received ACK: ACK({ack_num}). Moving window forward.")
            self.base = ack_num + 1
            # Remove acknowledged packets' timers
            for seq in list(self.timers):
                if seq <= ack_num:
                    del self.timers[seq]
        else:
            print(f"[Sender][GBN] Received duplicate ACK: ACK({ack_num}). Ignoring.")

    def check_timeout(self):
        current_time = time.time()
        for seq_num in list(self.timers):
            if current_time - self.timers[seq_num] > TIMEOUT:
                print(f"[Sender][GBN] Timeout for seq {seq_num}. Retransmitting window.")
                self.resend_window()
                break  # Only retransmit once per timeout

# Go-Back-N Receiver
class GoBackNReceiver:
    def __init__(self):
        self.expected_seq_num = 0

    def receive_packet(self, packet):
        outcome = simulate_packet_loss_or_corruption()
        if outcome == "loss":
            print(f"[Network] Packet lost: {packet}")
            return None
        elif outcome == "corruption":
            print(f"[Network] Packet corrupted: {packet}")
            return None

        if packet.seq_num == self.expected_seq_num:
            print(f"[Receiver][GBN] Received expected packet: {packet}. Sending ACK.")
            ack_num = packet.seq_num
            self.expected_seq_num += 1
            return ack_num
        else:
            print(f"[Receiver][GBN] Received out-of-order packet: {packet}. Sending ACK({self.expected_seq_num - 1}).")
            return self.expected_seq_num - 1

# Go-Back-N Protocol Logic
class GoBackNProtocol:
    def __init__(self):
        self.sender = GoBackNSender()
        self.receiver = GoBackNReceiver()

    def run(self):
        """Run the Go-Back-N protocol."""
        while self.sender.base < self.sender.total_packets:
            # Send packets within the window
            while self.sender.next_seq_num < self.sender.base + self.sender.window_size and \
                  self.sender.next_seq_num < self.sender.total_packets:
                packet = self.sender.packets[self.sender.next_seq_num]
                self.sender.send_packet(packet)
                self.sender.next_seq_num += 1

            # Simulate network behavior
            for seq_num in range(self.sender.base, self.sender.next_seq_num):
                packet = self.sender.packets[seq_num]
                ack_num = self.receiver.receive_packet(packet)
                if ack_num is not None:
                    self.sender.receive_ack(ack_num)
                else:
                    # Packet was lost or corrupted; simulate timeout
                    simulate_timeout()
                    self.sender.check_timeout()
                    break  # After timeout, break to resend window

            # Check for timeouts after sending window
            self.sender.check_timeout()

            # If all packets are acknowledged, terminate
            if self.sender.base >= self.sender.total_packets:
                print("=== All packets successfully transmitted. Connection terminated. ===")
                break

# Main function to run the protocols
def main():
    print("Select the protocol to test:")
    print("1. Stop-and-Wait")
    print("2. Go-Back-N")
    
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        print("=== Testing Stop-and-Wait Protocol ===")
        protocol = StopAndWaitProtocol()
    elif choice == "2":
        print("=== Testing Go-Back-N Protocol ===")
        protocol = GoBackNProtocol()
    else:
        print("Invalid selection.")
        return
    
    protocol.run()

if __name__ == "__main__":
    main()
