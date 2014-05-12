import sys
"""
For the statistics in these tests cases, it will often be helpful to have
running statistics. Something comprable to the output of uptime, where you
get the 1 min 5 min and 15 min averages.
"""

class moving_average():
    def __init__(self, wanted_set):
        # Grab the wanted set. Making it a set ensures no duplicates. Sorting
        # it ensures that the output comes like you would expect.
        self.wanted = sorted(set(wanted_set))
        # This is the longest time anything will be averaged over. It is set
        # to one over the largest value so that current_index % longest does
        # not result in the same entry, which has a diff of 0.
        self.longest = max(self.wanted) + 1
        # Initialize the values array. It starts with None in every possible
        # position
        self.values = [None]*self.longest
        # Start with an index of zero and work up from there every time the
        # user adds a new value. I used to let the uer give the current time
        # to act as the index, but that only leads to unanted behavor when they
        # skip one
        self.current_index = 0

    def insert_value(self, value):
        # Generate the next index for where to place a value
        self.current_index = (self.current_index + 1) % self.longest
        self.values[self.current_index] = value
    
    def get_diffs(self):
        current_value = self.values[self.current_index]
        # A list of tuples that will be filled with the
        diff_tuples = []
        for value in self.wanted:
            past_time = self.current_index - value
            past_index = past_time % self.longest
            past_value = self.values[int(past_index)]
            # There are times when this value has not been set yet, so we
            # cannot add its diff to the returned tuples
            if not past_value:
                continue
            diff_value = current_value - past_value
            diff_tuples.append((value, diff_value))
        return diff_tuples

