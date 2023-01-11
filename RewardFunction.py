B_progress = 0
import math

def reward_function(params):
    '''
    In @params object:
    {
        "all_wheels_on_track": Boolean,    # flag to indicate if the vehicle is on the track
        "x": float,                        # vehicle's x-coordinate in meters
        "y": float,                        # vehicle's y-coordinate in meters
        "distance_from_center": float,     # distance in meters from the track center
        "is_left_of_center": Boolean,      # Flag to indicate if the vehicle is on the left side to the track center or not.
        "heading": float,                  # vehicle's yaw in degrees
        "progress": float,                 # percentage of track completed
        "steps": int,                      # number steps completed
        "speed": float,                    # vehicle's speed in meters per second (m/s)
        "streering_angle": float,          # vehicle's steering angle in degrees
        "track_width": float,              # width of the track
        "waypoints": [[float, float], a?| ], # list of [x,y] as milestones along the track center
        "closest_waypoints": [int, int]    # indices of the two nearest waypoints.
    }
    '''

    entersteering = [17, 75, 99]
    left = [*range(22, 48), *range(62, 105)]
    right = [*range(48, 60)]

    global B_progress

    # Read input parameters
    track_width = params['track_width']  # max 0.76m
    distance_from_center = params['distance_from_center']  # max 0.76/2 = 0.38
    is_left_of_center = params['is_left_of_center']
    closest_waypoints = params['closest_waypoints']

    # Add progress
    N_progress = params['progress']

    # Add Speed
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    SPEED_THRESHOLD = 2.0

    # Add angle
    # Only need the absolute steering angle
    steering = abs(params['steering_angle'])
    waypoints = params['waypoints']
    heading = params['heading']
    reward = 1e-3


    def RewardOnTrack(CurrentReward, on_track):
        # Speed ctrl
        if not on_track:        # (False) if any of its wheels are outside of the track borders
            CurrentReward = 0.01
        else:                   # (True) if all of the wheels are inside the two track borders
            CurrentReward = 0.1

        return CurrentReward

    def RewardDistanceFromCenter(CurrentReward, TrackWidth, DistanceFromCenter):
        # Calculate 3 markers that are at varying distances away from the center line
        marker_1 = 0.1 * TrackWidth    # 0.076
        marker_2 = 0.25 * TrackWidth   # 0.19m
        marker_3 = 0.5 * TrackWidth    # 0.38m

        # Give higher reward if the car is closer to center line and vice versa
        if DistanceFromCenter <= marker_1:    # 0.076m
            CurrentReward += 1
        elif DistanceFromCenter <= marker_2:  # 0.19m
            CurrentReward += 0.25
        elif DistanceFromCenter <= marker_3:  # 0.38m
            CurrentReward += 0.0005
        else:
            CurrentReward = 1e-5  # likely crashed/ close to off track

        return CurrentReward

    def RewardSteering(CurrentReward, Steering):
        # Steering penality threshold, change the number based on your action space setting
        ABS_STEERING_THRESHOLD = 10

        # Penalize reward if the agent is steering too much
        if Steering < ABS_STEERING_THRESHOLD:
            CurrentReward *= 5

        if closest_waypoints[0] in entersteering:
            Steering > 20
            CurrentReward += 2

        return CurrentReward

    def RewardStraightLine(CurrentReward, steering, speed):
        if steering < 10 and speed > 2:
            CurrentReward *= 2
        elif steering > 20 and speed > 2:
            CurrentReward *= 0.5

        return CurrentReward

    def RewardProgress(CurrentReward, B_progress, N_progress):
        if (N_progress//10) > (B_progress//10):
            CurrentReward *= 2
            B_progress = N_progress

        return CurrentReward

    def RewardSpeed(CurrentReward, speed):
        if speed < SPEED_THRESHOLD:    # Penalize if the car goes too slow
            CurrentReward += 0.3

            if closest_waypoints[0] in left and is_left_of_center:
                CurrentReward += 0.5
            elif closest_waypoints[0] in right and not is_left_of_center:
                CurrentReward += 0.3
            else:
                CurrentReward -= 0.5

        else:    # High reward if the car stays on track and goes fast
            CurrentReward += 3.5

            if closest_waypoints[0] in left and is_left_of_center:
                CurrentReward += 0.5
            elif closest_waypoints[0] in right and not is_left_of_center:
                CurrentReward += 0.3
            else:
                CurrentReward -= 0.5

        return CurrentReward

    def RewardDirection(current_reward, waypoints, closest_waypoints, heading):
        '''
        Calculate the direction of the center line based on the closest waypoints
        '''
        DIRECTION_THRESHOLD = 20.0

        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        direction = math.atan2(
            next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        # Convert to degrees
        direction = math.degrees(direction)

        # Cacluate difference between track direction and car heading angle
        direction_diff = abs(direction - heading)

        # Penalize if the difference is too large
        if direction_diff > DIRECTION_THRESHOLD:
            current_reward *= 0.8
        else:
            current_reward *= 1.1

        return current_reward

    reward = RewardOnTrack(reward, all_wheels_on_track)
    reward = RewardDistanceFromCenter(reward, track_width, distance_from_center)
    reward = RewardDirection(reward, waypoints, closest_waypoints, heading)
    reward = RewardSteering(reward, steering)
    reward = RewardStraightLine(reward, steering, speed)
    reward = RewardProgress(reward, B_progress, N_progress)
    reward = RewardSpeed(reward, speed)

    return float(reward)
