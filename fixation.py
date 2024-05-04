import pandas as pd
import numpy as np


""" Parses complex timestamp formats into seconds"""
def parse_timestamp(timestamp):
    parts = timestamp.split('.')
    time_part, milli_part = parts[0], parts[1].split('/')[0]
    h, m, s = map(int, time_part.split(':')[-3:])
    total_seconds = h * 3600 + m * 60 + s + int(milli_part) / 1000
    return total_seconds


""" Calculates the velocity between consecutive eye positions"""
def calculate_velocity(data):
    diff_x = np.diff(data['pupilX'])
    diff_y = np.diff(data['pupilY'])
    diff_t = np.diff(data['timestamp_seconds'])
    distances = np.sqrt(diff_x**2 + diff_y**2)
    velocities = distances / diff_t
    velocities = np.insert(velocities, 0, np.nan)
    return velocities


""" Identifies fixation periods based on a velocity threshold"""
def identify_fixations(data, threshold):
    data['is_fixation'] = data['velocity'] < threshold
    data['fixation_block'] = (data['is_fixation'].shift(1) != data['is_fixation']).cumsum()
    fixations = data[data['is_fixation']]
    return fixations


""" Summarizes fixation periods, filtering out those that are too short and adjusting timestamps"""
def summarize_fixations(fixations, min_duration=0.01):
    # Group the data by fixation blocks and get the first timestamp of each block as the start of a fixation
    fixation_starts = fixations.groupby('fixation_block')['timestamp_seconds'].first().reset_index(drop=True)

    # Group the data by fixation blocks and get the last timestamp of each block as the end of a fixation
    fixation_ends = fixations.groupby('fixation_block')['timestamp_seconds'].last().reset_index(drop=True)

    fixation_segments = pd.DataFrame({'Onset': fixation_starts, 'Offset': fixation_ends})
    fixation_segments['Duration'] = fixation_segments['Offset'] - fixation_segments['Onset']

    # Filter out fixations that are shorter than the minimum duration threshold
    fixation_segments = fixation_segments[fixation_segments['Duration'] >= min_duration]

    fixation_segments = fixation_segments[['Onset', 'Offset']]  # Drop Duration for final output
    return fixation_segments


"""Main (read child_eye and parent_ eye)"""
def process_eye_data(file_path, output_file, start_frame, end_frame, velocity_threshold=20):
    """Processes eye-tracking data to identify and summarize fixations within a specific frame range."""
    data = pd.read_csv(file_path, skiprows=16, delimiter=' ', usecols=[0, 3, 7, 8],
                       names=['Frame', 'timestamp', 'pupilX', 'pupilY'], engine='python')

    # Filter data to include only frames within the specified range
    data = data[(data['Frame'] >= start_frame) & (data['Frame'] <= end_frame)]

    data['timestamp_seconds'] = data['timestamp'].apply(parse_timestamp)
    data['velocity'] = calculate_velocity(data)
    fixations = identify_fixations(data, velocity_threshold)
    fixation_segments = summarize_fixations(fixations)
    fixation_segments.to_csv(output_file, index=False)
    print(f'Fixation segments saved to {output_file}')


"""# Run main entry"""
if __name__ == "__main__":
    input_file_path = input("Enter the path to the eye tracking data file: ")
    output_file_path = input("Enter the path for the output CSV file: ")
    start_frame = int(input("Enter thr Start frame of the data segment: ")) + 1
    end_frame = int(input("Enter thr End frame of the data segment: "))
    process_eye_data(input_file_path, output_file_path, start_frame, end_frame)

