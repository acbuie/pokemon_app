import sys
import time
import re
import requests

from bs4 import BeautifulSoup

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    """
    Printing function to print odd characters sometimes seen in the pokemon names.
    """
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        def f(obj): return str(obj).encode(
            enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class StopWatch:
    
    def __init__(self):
        self._start_time = None
        self._start_lap_time = None
        self.lap_times = []

    def start(self):
        """Start a new timer."""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        # Start both clocks
        self._start_time = time.perf_counter()
        self._start_lap_time = time.perf_counter()

    def lap(self, store = True):
        """Reset the lap time, but not the initial start time."""
        lap_elapsed_time = time.perf_counter() - self._start_lap_time
        
        if store:
            self.lap_times.append(lap_elapsed_time)
            self._start_lap_time = time.perf_counter()
        else:
            self._start_lap_time = time.perf_counter()
            return lap_elapsed_time

    @property
    def average_lap(self):
        try:
            average_lap = sum(self.lap_times) / len(self.lap_times)
            return average_lap
        except ZeroDivisionError:
            print('Division by zero')

    def stop(self):
        """Stop the timer, and report the elapsed time."""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        total_elapsed_time = time.perf_counter() - self._start_time
        
        # End both clocks
        self._start_time = None
        self._start_lap_time = None
        
        # Report elapsed time
        return total_elapsed_time

def diff_list(l1, l2):
    """
    Takes two lists and returns items in l1 that are not in l2. 
    """
    return(set(l1) - set(l2))

def find_substring(
    marker1, marker2, string, manual_pattern, manual = False):
    """
    Returns the first occurence of a substring between two markers in a string. 
    Will return None if no matches are found. 

    # Consider changing this to **kwargs to clean up
    If manual = True, then user can input own string pattern (for 
    complex characters). Otherwise, input an empty string here. 
    """
    pattern = f'{marker1}(.*?){marker2}'
    if manual_pattern is True:
        pattern = manual_pattern

    search_result = re.search(pattern, string)
    if search_result is not None:
        return search_result.group(1)
    else:
        return None

def make_soup(url, parser):
    """
    Takes a url and a html parser and returns a BeautifulSoup soup object.
    """
    
    source = requests.get(url).text
    soup = BeautifulSoup(source, parser)
    
    return soup
    
