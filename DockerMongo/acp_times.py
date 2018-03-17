import arrow

maxSpeed = {200: 34, 400: 32, 600: 30, 1000: 28, 1300: 26}
minSpeed = {600: 15, 1000: 11.428, 1300: 13.333}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    distance = float(brevet_dist_km)
    distance = distance * 1.2
    
    if control_dist_km > distance:
        return '-1' 


    for control_boundary, max_speed in maxSpeed.items():
        if control_dist_km < control_boundary:
            return calculate_time(control_dist_km, max_speed, brevet_start_time)



def close_time(control_dist_km, brevet_dist_km, brevet_start_time):

    for control_boundary, min_speed in minSpeed.items():
        if control_dist_km < control_boundary:
            return calculate_time(control_dist_km, min_speed, brevet_start_time)



def calculate_time(dist, speed, start_time):

    total_time = dist / speed
    hour_fraction_part = total_time - int(total_time)
    minutes_after_hour = int(hour_fraction_part * 60)
    total_hours = int(total_time - hour_fraction_part)

    start_time = start_time.replace(hours=total_hours, minutes=minutes_after_hour)

    return start_time
