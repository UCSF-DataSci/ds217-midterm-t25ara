#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.
import pandas as pd
import random
def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    # TODO: Read file, split on '=', create dict
    config = {} #making empty dictionary 
    with open(filepath,'r') as file:
        for line in file:
            line = line.strip()
            key, value = line.split('=', 1) #splitting on first =
            value = int(value) #converting string to integer 
            config[key] = value #adding key and value to dictionary 
    return(config)
            
                
                 

def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    # TODO: Implement with if/elif/else
    results = {
        'sample_data_rows': False,
        'sample_data_min': False,
        'sample_data_max': False
    }

    try:
        rows = int(config['sample_data_rows'])
        min_val = int(config['sample_data_min'])
        max_val = int(config['sample_data_max'])
    except (ValueError, TypeError, KeyError):
        # If conversion or missing key error occurs, return defaults
        return results

    # Check sample_data_rows
    if isinstance(rows, int) and rows > 0:
        results['sample_data_rows'] = True
    else:
        results['sample_data_rows'] = False

    # Check sample_data_min
    if isinstance(min_val, int) and min_val >= 1:
        results['sample_data_min'] = True
    else:
        results['sample_data_min'] = False

    # Check sample_data_max
    if isinstance(max_val, int):
        if max_val > min_val:
            results['sample_data_max'] = True
        else:
            results['sample_data_max'] = False
    else:
        results['sample_data_max'] = False

    return results

def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    # TODO: Parse config values (convert strings to int)
    # TODO: Generate random numbers and save to file
    # TODO: Use random module with config-specified range
    rows = int(config['sample_data_rows'])
    min = int(config['sample_data_min'])
    max = int(config['sample_data_max'])
    import random
    numbers = [random.randint(min,max) for _ in range(rows)]
    with open(filename, 'w') as f:
        for number in numbers:
            f.write(f"{number}\n")
    print(f"sample data generated with numbers between {min} and {max} with {rows} rows")

def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    # TODO: Calculate stats
    n = len(data)
    sortdata = sorted(data)
    if n % 2 == 0:
        # even number of elements 
        median = (sortdata[n//2 - 1] + sortdata[n//2]) / 2
    else:
        # odd number of element
        median = sortdata[n//2]

    results = {}
    results['mean'] = sum(data)/len(data)
    results['median'] = median
    results['sum'] = sum(data)
    results['count'] = len(data)
    return results



if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    config = parse_config('q2_config.txt')
    validation = validate_config(config)
    generate_sample_data('data/sample_data.csv',config)
    with open('data/sample_data.csv', 'r') as file:
        data = [int(line.strip()) for line in file]
    stats = calculate_statistics(data)
    # TODO: Save statistics to output/statistics.txt
    with open('output/statistics.txt', 'w') as file:
        for key, value in stats.items():
            file.write(f"{key}: {value}\n") 