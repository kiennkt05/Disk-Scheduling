from typing import List

def FCFS(arr, head):
 
    distance, memory = 0, [head]
    for cur_track in arr:
        distance += abs(cur_track - head)
        head = cur_track
        memory.append(cur_track)
     
    return distance, memory

def SSTF(arr, head):
    def calculateDifference(queue, head, diff):
        for i in range(len(diff)):
            diff[i][0] = abs(queue[i] - head)
    
    def findMin(diff):
        index = -1
        minimum = 999999999
        for i in range(len(diff)):
            if (not diff[i][1] and minimum > diff[i][0]):
                minimum = diff[i][0]
                index = i
        return index

    if len(arr) == 0:
        return
    
    diff = [0] * len(arr)

    for i in range(len(arr)):
        diff[i] = [0,0]

    distance, memory = 0, [0] * (len(arr) + 1)
    for i in range(len(arr)):
        memory[i] = head
        calculateDifference(arr, head, diff)
        index = findMin(diff)

        diff[index][1] = True
        distance += diff[index][0]
        head = arr[index]
    memory[-1] = head
    return distance, memory

def SCAN(arr, head, direction):

    seek_count = 0
    distance, cur_track = 0, 0
    left = []
    right = []
    seek_sequence = []

    # Appending end values
    # which has to be visited
    # before reversing the direction
    if (direction == "left"):
        left.append(0)
    elif (direction == "right"):
        right.append(disk_size - 1)

    for i in range(size):
        if (arr[i] < head):
            left.append(arr[i])
        if (arr[i] > head):
            right.append(arr[i])

    # Sorting left and right vectors
    left.sort()
    right.sort()

    # Run the while loop two times.
    # one by one scanning right
    # and left of the head
    run = 2
    while (run != 0):
        if (direction == "left"):
            for i in range(len(left) - 1, -1, -1):
                cur_track = left[i]

                # Appending current track to 
                # seek sequence
                seek_sequence.append(cur_track)

                # Calculate absolute distance
                distance = abs(cur_track - head)

                # Increase the total count
                seek_count += distance

                # Accessed track is now the new head
                head = cur_track
            
            direction = "right"
    
        elif (direction == "right"):
            for i in range(len(right)):
                cur_track = right[i]
                
                # Appending current track to seek 
                # sequence
                seek_sequence.append(cur_track)

                # Calculate absolute distance
                distance = abs(cur_track - head)

                # Increase the total count
                seek_count += distance

                # Accessed track is now new head
                head = cur_track
            
            direction = "left"
        
        run -= 1

    print("Total number of seek operations =", 
          seek_count)

    print("Seek Sequence is")

    for i in range(len(seek_sequence)):
        print(seek_sequence[i])

def SCAN(arr, head):
    
    distance, memory = 0, [head]

    return distance, memory

def CSCAN(arr, head):
    
    distance, memory = 0, [head]

    return distance, memory

def LOOK(arr, head):
    
    distance, memory = 0, [head]

    return distance, memory

def CLOOK(arr, head):
    
    distance, memory = 0, [head]

    return distance, memory

