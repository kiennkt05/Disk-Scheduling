from typing import List

def FCFS(arr, head, direction, disk_size):
 
    distance, memory = 0, [head]
    for cur_track in arr:
        distance += abs(cur_track - head)
        head = cur_track
        memory.append(cur_track)
     
    return distance, memory

def SSTF(arr, head, direction, disk_size):
    arr.append(head)  # Add the head to the array
    arr.sort()  # Sort the array
    head_index = arr.index(head)  # Locate the head in the sorted array

    visited = [False] * len(arr)  # Track visited elements
    visited[head_index] = True  # Mark the head as visited

    distance = 0
    memory = [head]
    left, right = head_index - 1, head_index + 1  # Initialize pointers for left and right neighbors

    for _ in range(len(arr) - 1):  # Iterate through all tracks except the head
        left_distance = abs(arr[left] - head) if left >= 0 and not visited[left] else float('inf')
        right_distance = abs(arr[right] - head) if right < len(arr) and not visited[right] else float('inf')

        # Choose the closest unvisited track
        if left_distance < right_distance:
            distance += left_distance
            head = arr[left]
            memory.append(head)
            visited[left] = True
            left -= 1
        else:
            distance += right_distance
            head = arr[right]
            memory.append(head)
            visited[right] = True
            right += 1

    return distance, memory

def SCAN(arr, head, direction, disk_size):
    size = len(arr)
    distance, cur_track = 0, 0
    left, right, memory = [], [], [head]

    if (direction == "Left"):
        left.append(0)
    elif (direction == "Right"):
        right.append(disk_size - 1)

    for i in range(size):
        if (arr[i] < head):
            left.append(arr[i])
        if (arr[i] > head):
            right.append(arr[i])
    left.sort()
    right.sort()

    run = 2
    while (run != 0):
        if (direction == "Left"):
            for i in range(len(left) - 1, -1, -1):
                cur_track = left[i]

                # Appending current track to seek sequence
                memory.append(cur_track)

                distance += abs(cur_track - head)
                head = cur_track
            
            direction = "Right"
    
        elif (direction == "Right"):
            for i in range(len(right)):
                cur_track = right[i]
                
                # Appending current track to seek sequence
                memory.append(cur_track)

                distance += abs(cur_track - head)
                head = cur_track
            
            direction = "Left"
        
        run -= 1

    return distance, memory

def CSCAN(arr, head, direction, disk_size):
    size = len(arr)
    distance, memory = 0, [head]
    cur_track = 0
    left, right = [], []

    left.append(0), right.append(disk_size - 1)
    for i in range(size):
        if arr[i] < head:
            left.append(arr[i])
        elif arr[i] > head:
            right.append(arr[i])
    left.sort(), right.sort()

    if direction == "Right":
        # Move right, then jump to the leftmost and continue
        for i in range(len(right)):
            cur_track = right[i]
            memory.append(cur_track)
            distance += abs(cur_track - head)
            head = cur_track

        # Jump to the leftmost boundary
        head = 0
        distance += (disk_size - 1)

        for i in range(len(left)):
            cur_track = left[i]
            memory.append(cur_track)
            distance += abs(cur_track - head)
            head = cur_track

    elif direction == "Left":
        # Move left, then jump to the rightmost and continue
        for i in range(len(left) - 1, -1, -1):
            cur_track = left[i]
            memory.append(cur_track)
            distance += abs(cur_track - head)
            head = cur_track

        # Jump to the rightmost boundary
        head = disk_size - 1
        distance += (disk_size - 1)

        for i in range(len(right) - 1, -1, -1):
            cur_track = right[i]
            memory.append(cur_track)
            distance += abs(cur_track - head)
            head = cur_track

    return distance, memory

def LOOK(arr, head, direction, disk_size):
    size = len(arr)
    distance, memory = 0, [head]
    cur_track = 0
    left, right = [], []

    for i in range(size):
        if arr[i] < head:
            left.append(arr[i])
        elif arr[i] > head:
            right.append(arr[i])
    left.sort(), right.sort()

    run = 2
    while run:
        if direction == 'Left':
            for i in range(len(left) - 1, -1, -1):
                cur_track = left[i]
                memory.append(cur_track)
                distance += head - cur_track
                head = cur_track
            direction = 'Right'
        elif direction == 'Right':
            for i in range(len(right)):
                cur_track = right[i]
                memory.append(cur_track)
                distance += cur_track - head
                head = cur_track
            direction = 'Left'
        
        run -= 1

    return distance, memory

def CLOOK(arr, head, direction, disk_size):
    size = len(arr)
    distance, memory = 0, [head]
    cur_track = 0
    left, right = [], []

    for i in range(size):
        if arr[i] < head:
            left.append(arr[i])
        elif arr[i] > head:
            right.append(arr[i])
    left.sort(), right.sort()

    if direction == "Right":
        # Move right, then jump to the leftmost request and continue
        for i in range(len(right)):
            cur_track = right[i]
            memory.append(cur_track)
            distance += abs(cur_track - head)
            head = cur_track

        if left:
            # Jump to the leftmost request
            distance += abs(head - left[0])
            head = left[0]

            for i in range(len(left)):
                cur_track = left[i]
                memory.append(cur_track)
                distance += abs(cur_track - head)
                head = cur_track

    elif direction == "Left":
        # Move left, then jump to the rightmost request and continue
        for i in range(len(left) - 1, -1, -1):
            cur_track = left[i]
            memory.append(cur_track)
            distance += abs(cur_track - head)
            head = cur_track

        if right:
            # Jump to the rightmost request
            distance += abs(head - right[-1])
            head = right[-1]

            for i in range(len(right) - 1, -1, -1):
                cur_track = right[i]
                memory.append(cur_track)
                distance += abs(cur_track - head)
                head = cur_track

    return distance, memory

