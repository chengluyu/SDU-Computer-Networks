#include <random>
#include <iostream>
#include <queue>
#include <vector>

struct Packet {
    double arrivalTime, serviceTime;
};

class Generator {
    std::random_device randomDevice_;
    std::mt19937 engine_;
    std::exponential_distribution<> arrivalTimeDistri_;
    std::exponential_distribution<> serviceTimeDistri_;
    double nextArrivalTime_;
public:
    Generator() : randomDevice_(), engine_(randomDevice_()),
                  arrivalTimeDistri_(0.5), serviceTimeDistri_(0.65) {
        nextArrivalTime_ = arrivalTimeDistri_(engine_);
    }

    inline double nextArrivalTime() const {
        return nextArrivalTime_;
    }

    Packet next() {
        Packet packet { nextArrivalTime_, serviceTimeDistri_(engine_) };
        nextArrivalTime_ += arrivalTimeDistri_(engine_);
        return packet;
    }
};

void singleQueueSimulation(const signed totalPacketCount) {
    const unsigned checkPointCount = 1000000;

    double currentTime = 0.0;
    double currentPacketFinishedTime = 0.0;
    unsigned simulatedPacketCount = 0;

    std::vector<double> waitingTimeSamples;
    waitingTimeSamples.reserve(totalPacketCount);
    
    std::queue<Packet> queue;
    Generator generator;

    while (simulatedPacketCount < totalPacketCount) {
        if (currentPacketFinishedTime < generator.nextArrivalTime()) {

            simulatedPacketCount++;
            if (simulatedPacketCount % checkPointCount == 0) {
                std::cout << "Simulated " << simulatedPacketCount << " packets\n";
            }
            
            if (queue.empty()) {
                Packet packet = generator.next();
                currentTime = packet.arrivalTime;
                currentPacketFinishedTime = packet.serviceTime + currentTime;
                waitingTimeSamples.push_back(0.0);
            } else {
                Packet packet = queue.front();
                queue.pop();
                currentTime = currentPacketFinishedTime;
                waitingTimeSamples.push_back(currentTime - packet.arrivalTime);
            }
        } else {
            Packet packet = generator.next();
            currentTime = packet.arrivalTime;
            queue.push(packet);
        }
    }
}

int main() {
    singleQueueSimulation(10000000);
    return 0;
}