# Reinforcement Learning Implementation

## World Rules
![image](https://github.com/user-attachments/assets/af178d5a-e94d-4c6a-bb2e-df11e6e46ff7)

## Problem
![image](https://github.com/user-attachments/assets/f98a1cd9-332d-4655-8354-7fbab8f1994e)

## Proposed Solution
We can use value iteration to compute the Expected value T*, which represents the minimum # of rounds remaining expected to corral the bull on x with (posB, posC). We can then initialize a structure to allow for storage of all 26,082 states and set all the states to infinity except for those with the bull at position (6,6), where the T* value for these states is 0. Based on this, we will iteratively calculate the T* value for each combination of (posB, posR) by considering possible moves for the bull and robot and the behavior of the bull (charging or uniformly moving in any valid direction) and then update this new T* value. We can iterate over this process until the T* values converge with respect to a specific threshold and output the given configuration T* value.
