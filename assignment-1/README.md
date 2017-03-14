# Assignment 1

Multi-queue simulation

## Description

A transmission system subject to 3 inputs and only one server. All inputs are characterized by Poisson process and the service time follows an exponential distribution.

## Goal

Explore a scheduling scheme which is able to allocate the service fairly to each of the input in terms of any performance measurement; obtaining the mean queue length, mean waiting time, queue length distribution and waiting time distribution for each queue. Any necessary explaination and statement should be included in the report.

## Implementation

### Utility Classes

* The `Packet` class represent a data packet, which has two fields: `arrival_time` and `service_time`.
* The `Generator` class is responsible for generating packets by exponential distribution.
* The `Line` class, representing a waiting line, consists two parts: a `Queue`(imported from `queue` module) and a `Generator`.
* The `MultipleQueue` class manages a sequence a lines.

### Single Queue Model

TBD.

### Multiple Queue Model

TBD.
