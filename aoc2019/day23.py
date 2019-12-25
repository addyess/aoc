import logging
from queue import Queue, Empty
import concurrent.futures as cf
import time

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('day23')
logger.setLevel(logging.INFO)

try:
    from aoc2019.computer import Machine
except ImportError:
    from computer import Machine


class NAT:
    def __init__(self, network):
        self.network = network
        self.result1 = None
        self.result2 = None
        self.empty = True
        self.rxqueue = Queue(1)

    def run(self):
        while True:
            time.sleep(5)
            idle = all(_.empty for _ in self.network.nics.values())
            if idle:
                x, y = self.rxqueue.get_nowait()
                if self.result2 and self.result2[1] == y:
                    logger.info(f"Result 2: {y}")
                    exit(0)
                self.result2 = x, y
                logger.debug(f"Idle Pkt {(x, y)}")
                self.network.nics[0].enqueue(self.result2)

    def enqueue(self, packet):
        if not self.result1:
            self.result1 = packet
            logger.info(f"Result 1: {packet[1]}")
        if not self.rxqueue.empty():
            _ = self.rxqueue.get()
        self.rxqueue.put(packet)


class Switch:
    def __init__(self):
        self.nics = {255: NAT(self)}

    @property
    def nat(self):
        return self.nics[255]

    def register(self, nic):
        self.nics[nic.addr[0]] = nic

    def recv(self, addr, packet):
        self.nics[addr].enqueue(packet)


class Nic:
    def __init__(self, addr, network):
        self.addr = addr, True
        self.network = network
        self.network.register(self)
        self.empty = True
        self.rxqueue = Queue()
        self.rxpkt = tuple()
        self.txbuf = tuple()

    def __iter__(self):
        return self

    def enqueue(self, pkt):
        self.empty = False
        self.rxqueue.put(pkt)

    def __next__(self):
        time.sleep(0)
        if self.addr[1]:
            self.addr = self.addr[0], False
            return self.addr[0]

        if self.rxpkt:
            pkt, self.rxpkt = self.rxpkt, tuple()
            return pkt[0]
        try:
            pkt = self.rxqueue.get_nowait()
        except Empty:
            self.empty = True
            return -1
        logger.debug(f"to {self.addr[0]}: {pkt}")
        self.rxpkt = pkt[1],
        return pkt[0]

    def send(self, val):
        self.txbuf = self.txbuf + (val,)
        if len(self.txbuf) == 3:
            (addr, x, y), self.txbuf = self.txbuf, tuple()
            logger.debug(f"fr {self.addr[0]}->{addr}: {(x, y)}")
            self.network.recv(addr, (x, y))


def main():
    with open('day23.txt') as fin:
        ins = fin.read()

    switch = Switch()
    network = [Nic(_, switch) for _ in range(0, 50)]
    machines = [Machine.decode(ins, _, _) for _ in network] + [switch.nat]

    with cf.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        [executor.submit(_.run) for _ in machines]


main()
