from compound.coach import Coach

coach = Coach(112, 5, 1)
coach.occupy_seat(1, 1)
print(coach.free_seats)
coach.free_seat(1)
print(coach.free_seats)