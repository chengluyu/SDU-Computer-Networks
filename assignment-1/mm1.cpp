#include <fstream>
#include <iostream>
#include <queue>
#include <random>
#include <string>
#include <vector>

enum Constant {
    kTotalPacketCount = 10000000,
    kCheckPoint = 100000
};

// Each packet has two properties: arrival time and serve time
struct Packet {
    double arriveTime, serveTime;
};

// A exponential variable generator by given lambda
class ExponentialVariableGenerator {
    std::random_device rd;
    std::mt19937 gen;
    std::exponential_distribution<> dist;
public:
    ExponentialVariableGenerator(double lambda) : rd(), gen(rd()), dist(lambda) { }
    
    inline double next() {
        return dist(gen);
    }
};

// Simulation queue
class Queue {
    std::queue<Packet> queue_;
    
    ExponentialVariableGenerator packetServeTimeGen_, arriveTimeGen_;
    double nextArriveTime_;
    
    // Create a new packet by exponential distribution
    inline Packet generatePacket(double arriveTime) {
        return Packet { arriveTime, packetServeTimeGen_.next() };
    }
    
public:
    // Initialize the simulation queue with certain arguments
    Queue() : packetServeTimeGen_(0.65), arriveTimeGen_(0.5), nextArriveTime_(0.0) { }
    
    // Create a new packet, then push it into the queue
    void emit(double time) {
        queue_.push(generatePacket(time));
        nextArriveTime_ = time + arriveTimeGen_.next();
    }
    
    // Returns how many packets in the queue
    inline int size() const {
        return static_cast<int>(queue_.size());
    }
    
    inline double getNextArriveTime() {
        return nextArriveTime_;
    }
    
    // Returns whether there is any packet in the queue
    inline bool hasNextPacket() const {
        return !queue_.empty();
    }
    /**/
    Packet getNextPacket() {
        Packet retValue = queue_.front();
        queue_.pop();
        return retValue;
    }
};

class Logger {
    std::vector<double> waitingTimeSamples_;
    std::vector<int> queueLengthSamples_;
public:
    Logger() = default;
    
    inline void logWaitingTime(double time) {
        waitingTimeSamples_.push_back(time);
    }
    
    inline void logQueueLength(int length) {
        queueLengthSamples_.push_back(length);
    }
    
    void dumpToFile() {
        std::ios::sync_with_stdio(false);

        std::ofstream waitingTimeWriter { "waiting-time.txt" };
        for (double val : waitingTimeSamples_) {
            waitingTimeWriter << val << '\n';
        }
        waitingTimeWriter.close();
        
        std::ofstream queueLengthWriter { "queue-length.txt" };
        for (int val : queueLengthSamples_) {
            waitingTimeWriter << val << '\n';
        }
        queueLengthWriter.close();
    }
};


int main() {
    Logger logger;
    
    double currentTime = 0.0, currentPacketFinishTime = 0.0;
    int simulatedPacketCount = 0;
    
    Queue queue;
    
    // Simulate until we reach the goal
    while (simulatedPacketCount < kTotalPacketCount) {
        // This packet will be served before next packet arrives
        if (currentPacketFinishTime < queue.getNextArriveTime()) {
            // Has next packet
            if (queue.hasNextPacket()) {
                // Get next packet from the queue
                Packet packet = queue.getNextPacket();

                // Increase the counter
                simulatedPacketCount++;

                // Encounter a checkpoint, do print progress
                if (simulatedPacketCount % kCheckPoint == 0) {
                    std::cout << "Simulated " << simulatedPacketCount << " packets.\n";
                }
                
                // Packet has been served, update current time
                currentTime = currentPacketFinishTime;

                // Append to waiting time
                logger.logWaitingTime(currentPacketFinishTime - packet.arriveTime);

                currentPacketFinishTime = currentTime + packet.serveTime;
            }
            // No packets in the queue
            else {
                logger.logQueueLength(queue.size());
                // Emit a packet
                queue.emit(currentTime);
                // Move forward time to the arrival time of next packet
                currentTime = queue.getNextArriveTime();
            }
        }
        // Next packet arrives before this packet is served
        else {
            logger.logQueueLength(queue.size());
            // Emit a packet
            queue.emit(currentTime);
            // Time jump
            currentTime = queue.getNextArriveTime();
        }
    }
    
    std::cout << "Done.\n";

    logger.dumpToFile();
    return 0;
}
