import sys
import os
import time
from seatheap import SeatHeap
from minheap import MinHeap
from rbtree import RedBlackTree

def main():
    if len(sys.argv) < 2:
        print("Input file not specified.")
        return

    input_filename = sys.argv[1]
    output_filename = input_filename.split(".")[0] + "_output_file.txt"

    with open(input_filename, "r") as f_in, open(output_filename, "w") as f_out:
        # Initialize data structures
        seat_heap = SeatHeap()  # Heap to manage available seats
        waitlist = MinHeap()  # Heap to manage the waitlist
        reservations = RedBlackTree()  # Red-Black Tree to manage reservations
        user_to_seat = {}  # Mapping from userID to seatID
        next_seat_number = 1  # Next seat number to be assigned
        timestamp = 0  # Timestamp to manage waitlist ordering
        user_in_waitlist = {}  # Keep track of users in waitlist

        for line in f_in:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("Initialize("):
                param = line[line.find("(") + 1 : line.find(")")]
                try:
                    seatCount = int(param)
                    # Add seat numbers to the available seat heap
                    for seatID in range(next_seat_number, next_seat_number + seatCount):
                        seat_heap.push(seatID)
                    next_seat_number += seatCount
                    f_out.write(
                        f"{seatCount} Seats are made available for reservation\n"
                    )
                except ValueError:
                    f_out.write(
                        "Invalid input. Please provide a valid number of seats.\n"
                    )
            elif line.startswith("Available"):
                # Output the number of available seats and length of waitlist
                f_out.write(
                    f"Total Seats Available : {len(seat_heap.heap)}, Waitlist : {len(waitlist)}\n"
                )
            elif line.startswith("Reserve("):
                params = line[line.find("(") + 1 : line.find(")")].split(",")
                userID = int(params[0].strip())
                userPriority = int(params[1].strip())
                if userID in user_to_seat:
                    # User already has a reservation
                    continue  # As per instructions, users cannot reserve twice
                elif userID in user_in_waitlist:
                    # User already in waitlist
                    continue  # Do nothing
                else:
                    if len(seat_heap) > 0:
                        seatID = seat_heap.pop()
                        reservations.insert(seatID, userID)
                        user_to_seat[userID] = seatID
                        f_out.write(f"User {userID} reserved seat {seatID}\n")
                    else:
                        timestamp += 1
                        waitlist.push(userPriority, timestamp, userID)
                        user_in_waitlist[userID] = True
                        f_out.write(f"User {userID} is added to the waiting list\n")
            elif line.startswith("Cancel("):
                params = line[line.find("(") + 1 : line.find(")")].split(",")
                seatID = int(params[0].strip())
                userID = int(params[1].strip())
                if userID in user_to_seat:
                    if user_to_seat[userID] != seatID:
                        f_out.write(
                            f"User {userID} has no reservation for seat {seatID} to cancel\n"
                        )
                    else:
                        # Cancel reservation
                        reservations.delete_node(seatID)
                        del user_to_seat[userID]
                        if len(waitlist) > 0:
                            next_user = waitlist.pop()
                            seat_num = seatID
                            reservations.insert(seat_num, next_user.userID)
                            user_to_seat[next_user.userID] = seat_num
                            del user_in_waitlist[next_user.userID]
                            f_out.write(f"User {userID} canceled their reservation\n")
                            f_out.write(
                                f"User {next_user.userID} reserved seat {seat_num}\n"
                            )
                        else:
                            seat_heap.push(seatID)
                            f_out.write(f"User {userID} canceled their reservation\n")
                else:
                    f_out.write(f"User {userID} has no reservation to cancel\n")
            elif line.startswith("ExitWaitlist("):
                param = line[line.find("(") + 1 : line.find(")")]
                userID = int(param.strip())
                if userID in user_in_waitlist:
                    waitlist.remove(userID)
                    del user_in_waitlist[userID]
                    f_out.write(f"User {userID} is removed from the waiting list\n")
                else:
                    f_out.write(f"User {userID} is not in waitlist\n")
            elif line.startswith("UpdatePriority("):
                params = line[line.find("(") + 1 : line.find(")")].split(",")
                userID = int(params[0].strip())
                userPriority = int(params[1].strip())
                if userID in user_in_waitlist:
                    waitlist.update_priority(userID, userPriority)
                    f_out.write(
                        f"User {userID} priority has been updated to {userPriority}\n"
                    )
                else:
                    f_out.write(f"User {userID} priority is not updated\n")
            elif line.startswith("AddSeats("):
                param = line[line.find("(") + 1 : line.find(")")]
                try:
                    count = int(param)
                    for seatID in range(next_seat_number, next_seat_number + count):
                        seat_heap.push(seatID)
                    next_seat_number += count
                    if len(waitlist) == 0:
                        f_out.write(
                            f"Additional {count} Seats are made available for reservation\n"
                        )
                    else:
                        f_out.write(
                            f"Additional {count} Seats are made available for reservation\n"
                        )
                        while len(seat_heap) > 0 and len(waitlist) > 0:
                            seatID = seat_heap.pop()
                            next_user = waitlist.pop()
                            reservations.insert(seatID, next_user.userID)
                            user_to_seat[next_user.userID] = seatID
                            del user_in_waitlist[next_user.userID]
                            f_out.write(
                                f"User {next_user.userID} reserved seat {seatID}\n"
                            )
                except ValueError:
                    f_out.write(
                        "Invalid input. Please provide a valid number of seats.\n"
                    )
            elif line.startswith("PrintReservations"):
                res = reservations.inorder()
                for seatID, userID in res:
                    f_out.write(f"Seat {seatID}, User {userID}\n")
            elif line.startswith("ReleaseSeats("):
                params = line[line.find("(") + 1 : line.find(")")].split(",")
                try:
                    userID1 = int(params[0].strip())
                    userID2 = int(params[1].strip())
                    if userID2 < userID1:
                        raise ValueError
                    users_to_release = set(range(userID1, userID2 + 1))

                    # First, remove users in the release range from the waitlist
                    for userID in users_to_release:
                        if userID in user_in_waitlist:
                            waitlist.remove(userID)
                            del user_in_waitlist[userID]

                    assignment_messages = []
                    for userID in users_to_release:
                        if userID in user_to_seat:
                            seatID = user_to_seat[userID]
                            reservations.delete_node(seatID)
                            del user_to_seat[userID]
                            # Now assign the seat to next user not in the release range
                            while len(waitlist) > 0:
                                next_user = waitlist.pop()
                                del user_in_waitlist[next_user.userID]
                                if next_user.userID in users_to_release:
                                    # Skip users in the release range
                                    continue
                                else:
                                    reservations.insert(seatID, next_user.userID)
                                    user_to_seat[next_user.userID] = seatID
                                    assignment_messages.append(
                                        f"User {next_user.userID} reserved seat {seatID}\n"
                                    )
                                    break  # Exit while loop for this seat
                            else:
                                seat_heap.push(seatID)
                    if len(assignment_messages) == 0:
                        f_out.write(
                            f"Reservations of the Users in the range [{userID1}, {userID2}] are released\n"
                        )
                    else:
                        f_out.write(
                            f"Reservations of the Users in the range [{userID1}, {userID2}] are released\n"
                        )
                    for msg in assignment_messages:
                        f_out.write(msg)
                except ValueError:
                    f_out.write(
                        "Invalid input. Please provide a valid range of users.\n"
                    )

            elif line.startswith("Quit"):
                f_out.write("Program Terminated!!\n")
                break
            else:
                continue  # Ignore unrecognized commands


if __name__ == "__main__":
    main()
