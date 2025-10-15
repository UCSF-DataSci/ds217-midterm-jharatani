# TODO: Add shebang line: 
# #!/usr/bin/env python3

# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.


def parse_config(filepath: str) -> dict:
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config
    
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
    results = {}

    if isinstance(config.get('sample_data_rows'), int) and config['sample_data_rows'] > 0:
        results['sample_data_rows'] = True
    else:
        results['sample_data_rows'] = False

    if isinstance(config.get('sample_data_min'), int) and config['sample_data_min'] >= 1:
        results['sample_data_min'] = True
    else:
        results['sample_data_min'] = False

    if isinstance(config.get('sample_data_max'), int):
        if config['sample_data_max'] > config.get('sample_data_min', 0):
            results['sample_data_max'] = True
        else:
            results['sample_data_max'] = False
    else:
        results['sample_data_max'] = False

    
    return results

import random

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
        >>> config = {}
        config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        config = config.astype('int64')
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    # TODO: Parse config values (convert strings to int)

    rows = int(config.get('sample_data_rows', 100))
    min_val = int(config.get('sample_data_min', 1))
    max_val = int(config.get('sample_data_max', 100)) 

    # TODO: Generate random numbers and save to file
    # TODO: Use random module with config-specified range

    with open(filename, 'w') as file:
            for _ in range(rows):
                number = random.randint(min_val, max_val)
                file.write(f"{number}\n")

    print(f"Sample data written to {filename}")

    


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

    statistics = {"mean": None, "median": None, "sum": None, "count": None}
    n = len(data)
    if n == 0:
        return statistics
    else:
        statistics["count"] = n
        statistics["sum"] = sum(data)
        statistics["mean"] = statistics["sum"] / n

        # Calculate median  
        statistics["median"] = None
        if n % 2 == 1:
            statistics["median"] = sorted(data)[n // 2]
        else:
            mid1 = sorted(data)[n // 2 - 1]
            mid2 = sorted(data)[n // 2]
            statistics["median"] = (mid1 + mid2) / 2   

    return statistics



if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)

    config = parse_config('q2_config.txt')
    validate = validate_config(config)
    generate_sample_data('data/sample_data.csv', config)
    read_data = []
    with open('data/sample_data.csv', 'r') as file:
        for line in file:
            read_data.append(int(line.strip()))
    stats = calculate_statistics(read_data)
    print(stats)
    with open('output/statistics.txt', 'w') as file:
        for key, value in stats.items():
            file.write(f"{key}: {value}\n")
    
    print("Success")
    
    # TODO: Read the generated file and calculate statistics
    # TODO: Save statistics to output/statistics.txt

