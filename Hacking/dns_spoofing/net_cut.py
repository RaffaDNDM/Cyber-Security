import netfilterqueue

def process_packet(packet):
    print(packet) 

#Packets are blocked and not forwarded
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
