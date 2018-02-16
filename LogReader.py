# This functions will read log files and do a certain action within these log files.
class LogReader:
    """
    This class is used to make a class which can perform some standard procedures with log files.
    """
    def __init__(self, logfile):
        """
        The init method will open the file and count the number of lines. This will be necessary in the following
        functions. The input 'logfile' must be the logfile.txt file which is in the same directory as this python code.
        """
        self.log = open(logfile, 'r')
        self.count_lines(logfile)

    def count_lines(self, logfile):
        """
        counts the lines in the log file and return this to the init method. This method also prints the total number
        of lines.
        """
        with open(logfile) as f:
            for self.lines, l in enumerate(f):
                pass

    def extract_string(self, word):
        """
        This function returns a certain string which is given with a certain word in it.
        :param word:  The word which is used to find the right string.
        """
        self.sentence = []

        for n in range(self.lines):
            sentence = self.log.readline()

            if word in sentence:
                self.sentence.append(sentence)

    def extract_value(self, word):
        """
        This function returns a certain value of the extracted string if necessary.
        :param word:  The word which is used to find the right string (which comes after this word). Note: Due to
        split(), every (group of) character(s) with a space before and after will be seen as a word.
        """
        self.value_list = []
        for i in range(len(self.sentence)):
            sentence = self.sentence[i].split()
            index = sentence.index(word)
            value_raw = sentence[index+1]
            value = value_raw.replace("\"", "").replace("-", "")     # This will removes the useless characters
            self.value_list.append(value)


