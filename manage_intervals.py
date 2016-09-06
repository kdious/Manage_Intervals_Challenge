#!/usr/bin/python

"""
File:           manage_intervals.py

Author:         Kevin Dious (kdious@gmail.com)

Description:    This program is designed to manage a list
                of intervals.

                [[1, 3], [4, 6]] is a valid object gives two intervals.
                [[1, 3], [3, 6]] is not a valid object because it is not
                disjoint. [[1, 6]] is the intended result.

                Empty array [] means no interval, it is the default/start state.

                The program supports the following functions/routines:

                add from to:        Adds a new interval to the list
                remove from to:     Removes an interval from the list
                clear:              Clears the interval list
                enableDebugging:    Enables extra debugging logs
                disableDebugging:   Disables debugging logs
                displayList:        Display the current interval list
                exit:               Exits the program
                help:               Displays a list of commands

Other details:  This program uses a Python list to store the start and end
                values of each interval in a single list.  Since each interval
                has two entries (a "start" and "end" value), the interval
                list will always have an even number of entries.

                Python list objects are similar to a C++ vector or a
                Java ArrayList object in that the list entries are stored
                in a dynamic array.  This means that insertions and deletions
                in the list require copying of all members after the
                insertion/deletion point (the members after the insertion/deletion
                point are shifted).  Therefore, insertion and deletion operations
                are O(n) where n is the number of members in the interval list.

                One improvement to this implementation would be to use a
                linked list rather than a Python list object for storing the
                intervals.  This would make insertion/deletion operations O(1)
                instead of O(n).  However, Python does not have a built-in
                linked list type, so this would require implementing a separate
                linked list type.  Also, using a linked list would increase the
                complexity fo the algorithm somewhat in that you have to handle
                the next references (and the previous references if using a
                doubly linked list).  Moreover, a linked list would require
                slightly more overhead since you have to take into account the
                next node refereces (and previous node references if using a
                doubly linked list).

                Using the built-in Python list seems reasonable assuming that the
                total possible inputs for the interval start and ending points is
                small.  For example, if the intervals represented hours in a day
                then each hour can be represented by a number between 0-23, and at
                most there would be 24 possible entries in the intervals list
                representing at most 12 possible intervals.

                Finally, as written, this implementation can handle both positive
                and negative inputs for interval start and end values.
"""

import cmd
import logging

class EditIntervalsProgram(object, cmd.Cmd):

    def __init__(self):
        # Instantiate the cmd.Cmd super class
        super(object, self).__init__()

        # Initialize the initial interval list to an empty list
        self._m_IntervalList = []

        # Set log message format and get a logger instance
        logging.basicConfig(format='%(message)s\n', level=logging.INFO)
        self._m_Logger = logging.getLogger()

    def printIntervals(self):
        """
        Print the intervals list as a properly formatted string
        """

        # Debug message that simply prints the entire interval list
        self._m_Logger.debug("Intervals list: %s", self._m_IntervalList)

        """
        Intervals are stored in a single list in pairs.
        If i % 2 == 0 (i is even), then the list element is the start of an interval.
        If i % 2 == 1 (i is odd), then the list element is the end of an interval.
        For each interval pair, add the pair to the outputString

        Example:
        _m_IntervalList = [1, 3, 5, 8, 10, 12]
        outputString = [(1, 3), (5, 8), (10, 12)]
        """

        """
        Python String objects are immutable and Python does not have a StringBuilder
        type class so use a list to create the output string dynamically and
        then convert the list to a string.
        See: https://pythonadventures.wordpress.com/tag/stringbuffer/
        """

        outputList = ['[']
        for i in range (0, len(self._m_IntervalList), 2):
            outputList.append( \
                '({intervalStart}, {intervalEnd})'.format( \
                intervalStart=self._m_IntervalList[i], \
                intervalEnd=self._m_IntervalList[i + 1] \
            ))
            outputList.append(',')

        # Properly append the final character in outputString
        if len(self._m_IntervalList) == 0:
            # If the list IS empty then simply append ']' so that
            # the resulting string will be '[]'
            outputList.append(']')
        else:
            # If the list IS NOT empty then replace the last ',' with ']' so that
            # the resulting string will be sometihng like '[(1, 2), (3, 4)]'
            outputList[-1] = ']'

        # Create the output string from outputList
        outputString = ''.join(outputList)

        # Display output to screen
        self._m_Logger.info("Intervals: %s", outputString)

    def addInterval(self, start, end):
        # Error case - if start >= end then this is not a valid interval
        if start >= end:
            self._m_Logger.error("Error - start >= end")
            return

        if len(self._m_IntervalList) == 0 or self._m_IntervalList[-1] < start:
            """
            Case #1: empty list

            If there are no entires in the interval list then simply
            append start and end to the end of the intervals list

            Example:
            Current interval list: []
            Call: add(5, 10)
            Updated intervals list after adding start and end: [5, 10]

            Case #2: end of last interval < start

            If the last entry in the intervals list is < start,
            then this interval should be added to the end of the intervals list

            Example:
            Current interval list: [5, 10]
            Call: add(8, 10)
            Updated intervals list after adding start and end: [5, 10, 8, 10]
            """
            self._m_IntervalList.append(start)
            self._m_IntervalList.append(end)
        elif self._m_IntervalList[0] > end:
            """
            Case #3:

            If the first entry in the intervals list is greater than end
            then this interval should be added to the front of the list
            since it is the "lowest" interval.

            Example:
            Current interval list: [5, 10]
            Call: add(2, 3)
            Updated intervals list after adding start and end: [2, 3, 5, 10]
            """
            self._m_IntervalList.insert(0, start)
            self._m_IntervalList.insert(1, end)
        else:
            """
            In this case, the interval must be inserted
            somewhere within the list of existing intervals
            """

            """
            Determine where the start and end values
            should be interted into the interval list
            """
            startInsertionIdx = 0
            endInsertionIdx = 0

            while startInsertionIdx < len(self._m_IntervalList) and self._m_IntervalList[startInsertionIdx] < start:
                startInsertionIdx += 1

            endInsertionIdx = startInsertionIdx

            while endInsertionIdx < len(self._m_IntervalList) and self._m_IntervalList[endInsertionIdx] < end:
                endInsertionIdx += 1

            self._m_Logger.debug(
				"startInsertionIdx = %d, endInsertionIdx = %d, listLen = %d",
				startInsertionIdx,
				endInsertionIdx,
				len(self._m_IntervalList)
			)

            """
            Determine if startInsertionIdx and endInsertionIdx are the
            beginning or end of an existing interval.  Since an interval
            comprises of two entries (a beginning and end), an interval
            is inserted as a pair of entries the intervals list.  If
            startInsertionIdx/endInsertionIdx is even, then it is the
            start of an interval.  If startInsertionIdx/endInsertionIdx
            is odd, then it is the end of an interval.
            """
            isStartIntervalEnd = False
            isEndIntervalEnd = False

            if startInsertionIdx % 2 == 1:
                isStartIntervalEnd = True

            if endInsertionIdx % 2 == 1:
                isEndIntervalEnd = True

            """
            Insert the beginning of the new interval
            (start) into the interval list
            """
            currentIdx = startInsertionIdx

            if start < self._m_IntervalList[currentIdx]:
                """
                Case #1: start does not exist in the interval list

                If the current value at currentIdx is the beginning
                of an interval, then we simply insert start before the
                value at currentIdx.

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: add(4, 5)
                currentIdx = 2
                Updated intervals list after adding start: [2, 3, 4, 8, 10], currentIdx = 3

                Otherwise, the value at currentIdx is the end of an
                interval.  Since this value is the end of an interval
                we do nothing since (no need to insert it again).

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: add(3, 5)
                currentIdx = 1
                Updated intervals list after adding start: [2, 3, 8, 10], currentIdx = 1

                Note: The insertion of end (if necessary) will handle completing the interval
                """
                if isStartIntervalEnd == False:
                    self._m_IntervalList.insert(currentIdx, start)
                    currentIdx += 1
            else:
                """
                Case #2: start is present in the interval list

                If start is the end an existing interval, then we
                simply delete the value at currentIdx.

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: add(8, 10)
                currentIdx = 2
                Updated intervals list after adding start: [2, 3, 10], currentIdx = 2

                Otherwise, we leave the value of start in the
                interval list since it is the beginning of an
                existing interval (no need to insert it again).

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: add(3, 5)
                currentIdx = 1
                Updated intervals list after adding start: [2, 3, 8, 10], currentIdx = 2

                Note: The insertion of end (if necessary) will handle completing the interval
                """
                if isStartIntervalEnd == True:
                    del self._m_IntervalList[currentIdx]
                else:
                    currentIdx += 1

            """
            Delete any entries in the interval list where
            that entry > start AND entry < end

            Example:
            Current interval list: [2, 3, 8, 10, 15, 18]
            Call: add(5, 12)
            currentIdx = 2
            Updated intervals list after adding start and removing interim entries: [2, 3, 5, 15, 18], currentIdx = 3

            Note: The insertion of end (if necessary) will handle completing the interval
            """
            while currentIdx < len(self._m_IntervalList) and self._m_IntervalList[currentIdx] < end:
                del self._m_IntervalList[currentIdx]

            """
            Insert the end of the new interval
            (end) into the interval list
            """
            if end > self._m_IntervalList[-1]:
                """
                Case #1: end is greater than the largest value in the list

                If end is greater than the last value in the list
                then simply append it to the end of the interval list.

                Example:
                Current interval list: [5, 10]
                Call: add(6, 15)
                After inserting start: interval list = [5, 10], currentIdx = 1
                After interting start and end: [5, 15]
                """
                self._m_IntervalList.append(end)
            elif end < self._m_IntervalList[currentIdx]:
                """
                Case #2: end is not present in the list but
                         is < the largest value in the list

                If end < value at currentIdx AND the value at
                currentIdx is the beginning of an interval,
                then end should be inserted before the value
                at currentIdx.

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: add(6, 7)
                currentIdx = 2
                After inserting start: interval list = [2, 3, 6, 8, 10], currentIdx = 3
                After interting end: [2, 3, 6, 7, 8, 10]

                Otherwise, do nothing since end is already
                encompassed within an existing interval.

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: add(8, 9)
                currentIdx = 2
                After inserting start: interval list = [2, 3, 8, 10], currentIdx = 3
                After interting end: [2, 3, 8, 10]
                """
                if isEndIntervalEnd == False:
                    self._m_IntervalList.insert(currentIdx, end)
            else:
                """
                Case #3: end is present in the interval list

                If end is present in the interval list AND
                end is the beginning of an existing interval,
                then delete this value from the interval list
                since end will be encompassed by the new interval.

                Example:
                Current interval list: [5, 10]
                Call: add(2, 5)
                After inserting start (and deleting interim entries): interval list = [2, 10], currentIdx = 1
                After interting end: [2, 10]

                Otherwise, do nothing since end is already
                encompassed within an existing interval.

                Example:
                Current interval list: [5, 10]
                Call: add(5, 8)
                After inserting start (and deleting interim entries): interval list = [5, 10], currentIdx = 1
                After interting end: [5, 10]
                """
                if isEndIntervalEnd == False:
                    del self._m_IntervalList[currentIdx]

    def removeInterval(self, start, end):
        """
        Error case: start >= end, invalid interval
        """
        if start >= end:
            self._m_Logger.error("Error: start >= end")
            return

        """
        Error edge cases
        Case 1: Empty list
        Case 2: Trying to remove an interval that does not exist

        In either of these cases, do nothing.
        """
        if len(self._m_IntervalList) == 0 or self._m_IntervalList[-1] < start:
            return

        else:
            """
            In this case, the interval must be inserted
            somewhere within the list of existing intervals
            """

            """
            Determine where the start and end values
            should be interted into the interval list
            """
            startInsertionIdx = 0
            endInsertionIdx = 0

            while startInsertionIdx < len(self._m_IntervalList) and self._m_IntervalList[startInsertionIdx] < start:
                startInsertionIdx += 1

            endInsertionIdx = startInsertionIdx

            while endInsertionIdx < len(self._m_IntervalList) and self._m_IntervalList[endInsertionIdx] < end:
                endInsertionIdx += 1

            self._m_Logger.debug \
			(
				"startInsertionIdx = %d, endInsertionIdx = %d, listLen = %d",
				startInsertionIdx,
				endInsertionIdx,
				len(self._m_IntervalList)
			)

            isStartIntervalEnd = False
            isEndIntervalEnd = False

            if startInsertionIdx % 2 == 1:
                isStartIntervalEnd = True

            if endInsertionIdx % 2 == 1:
                isEndIntervalEnd = True

            currentIdx = startInsertionIdx

            if start < self._m_IntervalList[currentIdx]:
                """
                Case #1: start does not exist in the interval list

                If the current value at currentIdx is the end
                of an interval, then we simply insert start before the
                value at currentIdx.

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: remove(7, 9)
                currentIdx = 2
                Updated intervals list after adding start: [2, 3, 8, 10], currentIdx = 2
                Updated intervals list after deleting interim values: [2, 3, 10], currentIdx = 2
                Updated intervals list after adding end: [2, 3, 9, 10], currentIdx = 2

                Otherwise, the value at currentIdx is the end of an
                interval.  Since this value is the end of an interval
                we do nothing since (no need to insert it again).

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: remove(9, 10)
                currentIdx = 3
                Updated intervals list after adding start: [2, 3, 8, 9, 10]

                Note: The insertion of end (if necessary) will handle completing the interval
                """
                if isStartIntervalEnd == True:
                    self._m_IntervalList.insert(currentIdx, start)
                    currentIdx += 1
            else:
                """
                Case #2: start does exist in the interval list

                If the current value at currentIdx is the beginning
                of an interval, then we simply delete the value at currentIdx.

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: remove(8, 9)
                currentIdx = 2
                Updated intervals list after adding start: [2, 3, 10], currentIdx = 2

                Otherwise, the value at currentIdx is the end of an
                interval.  Since this value is the end of an interval
                we do nothing since (no need to insert it again).

                Example:
                Current interval list: [2, 3, 8, 10]
                Call: remove(3, 5)
                currentIdx = 1
                Updated intervals list after adding start: [2, 3, 8, 10], currentIdx = 2

                Note: The insertion of end (if necessary) will handle completing the interval
                """
                if isStartIntervalEnd == False:
                    del self._m_IntervalList[currentIdx]
                else:
                    currentIdx += 1

            """
            Delete any entries in the interval list where
            that entry > start and entry < end

            Example:
            Current interval list: [2, 3, 8, 10, 15, 18]
            Call: remove(9, 16)
            After inserting start: interval list = [2, 3, 8, 9, 10, 15, 18], currentIdx = 3
            After adding start and removing interim entries: [2, 3, 8, 9, 18], currentIdx = 3

            Note: The insertion of end (if necessary) will handle completing the interval
            """
            while currentIdx < len(self._m_IntervalList) and self._m_IntervalList[currentIdx] < end:
                del self._m_IntervalList[currentIdx]

            if currentIdx >= len(self._m_IntervalList):
                """
                Case #1: end is greater than the largest value in the list

                If end is greater than the last value in the list
                then do nothing.

                Example:
                Current interval list: [5, 10, 16, 18]
                Call: remove(17, 20)
                After inserting start: interval list = [5, 10, 16, 17, 18], currentIdx = 4
                After removing interim entries: interval list = [5, 10, 16, 17], currentIdx = 4
                No need to do anything with end.
                """
                pass
            elif end < self._m_IntervalList[currentIdx]:
                """
                Case #2: end is not present in the list but
                         is not the largest value in the list

                If end < value at currentIdx AND the value at
                currentIdx is the end of an interval,
                then end should be inserted before the value
                at currentIdx.

                Example:
                Current interval list: [2, 3, 8, 12]
                Call: remove(9, 10)
                currentIdx = 3
                After inserting start: interval list = [2, 3, 8, 9, 12], currentIdx = 4
                After interting end: [2, 3, 8, 9, 10, 12]

                Otherwise, do nothing since end is already
                the end of an existing interval.

                Example:
                Current interval list: [2, 3, 8, 12]
                Call: remove(10, 11)
                currentIdx = 3
                After inserting start: interval list = [2, 3, 8, 10, 11, 12], currentIdx = 4
                After interting end: [2, 3, 8, 10, 11, 12]
                """
                if isEndIntervalEnd == True:
                    self._m_IntervalList.insert(currentIdx, end)
            else:
                """
                Case #3: end is present in the interval list

                If end is present in the interval list AND
                end is the end of an existing interval,
                then delete this value from the interval list
                since end will be encompassed by the new interval.

                Example:
                Current interval list: [5, 10]
                Call: remove(8, 10)
                currentIdx = 1
                After inserting start: interval list = [5, 8, 10], currentIdx = 2
                After interting end: [5, 8]

                Otherwise, do nothing since end is already
                the beginning of an existing interval.

                Example:
                Current interval list: [2, 4, 5, 10]
                Call: remove(3, 5)
                currentIdx = 1
                After inserting start (and deleting interim entries): interval list = [2, 3, 5, 10], currentIdx = 2
                After interting end: [2, 3, 5, 10]
                """
                if isEndIntervalEnd == True:
                    del self._m_IntervalList[currentIdx]

    def clearList(self):
        """
        Empty the interval list and return it
        """
        del self._m_IntervalList[:]

        # Display output to screen
        self.printIntervals()

    def do_add(self, args):
        """
        Add an interval to the interval list
        Usage: add <start> <end>
               <start> must be less than <end>
        """

        """
        Get user input and check for input errors
        """
        cmdArgs = args.split()

        if len(cmdArgs) == 0:
            self._m_Logger.error("Error - No arguments passed\Usage: add <start> <end>")
            return

        elif len(cmdArgs) == 1:
            self._m_Logger.error("Error - Only one argument passed (Need at least 2)\nFormat: add <start> <end>")
            return

        else:
            try:
                start = int(cmdArgs[0])
                end = int(cmdArgs[1])
            except ValueError:
                self._m_Logger.error("Error - Inputs must be integer values")
                return

            if start >= end:
                self._m_Logger.error("Error - start must be < end\Usage: add <start> <end>")
                return

            # Run the command and get output
            self.addInterval(start, end)

            # Display output to screen
            self.printIntervals()

    def do_remove(self, args):
        """
        Remove an interval to the interval list
        Usage: remove <start> <end>
               <start> must be less than <end>
        """

        """
        Get user input and check for input errors
        """
        cmdArgs = args.split()

        if len(cmdArgs) == 0:
            self._m_Logger.error("Error - No arguments passed\Usage: remove <start> <end>")
            return

        elif len(cmdArgs) == 1:
            self._m_Logger.error("Error - Only one argument passed (Need at least 2)\Usage: remove <start> <end>")
            return

        else:
            try:
                start = int(cmdArgs[0])
                end = int(cmdArgs[1])
            except ValueError:
                self._m_Logger.error("Error - Inputs must be integer values")
                return

            if start >= end:
                self._m_Logger.error("Error - start must be < end\Usage: remove <start> <end>")
                return

            # Run the command and get output
            self.removeInterval(start, end)

            # Display output to screen
            self.printIntervals()

    def do_clear(self, args):
        """
        Clear the intervals list
        """

        # Clear the list
        result = self.clearList()

        # Display output to screen
        self._m_Logger.info("Intervals: %s", result)

    def do_displayList(self, args):
        """
        Print the intervals list
        """

        # Display output to screen
        self.printIntervals()

    def do_enableDebugging(self, args):
        """
        Enable debugging mode
        """
        self._m_Logger.setLevel(logging.DEBUG)
        self._m_Logger.info("Debugging mode enabled")

    def do_disableDebugging(self, args):
        """
        Disable debugging mode
        """
        self._m_Logger.setLevel(logging.INFO)
        self._m_Logger.info("Debugging mode disabled")

    def do_exit(self, args):
        """
        Exit the program
        """
        return True


# Main method for script
def main():
    # Instantiate EditIntervalsProgram object
    program = EditIntervalsProgram()

    # Run the program
    program.cmdloop(intro="Manage Intervals program")

# Call main function
if __name__ == "__main__":
    main()
