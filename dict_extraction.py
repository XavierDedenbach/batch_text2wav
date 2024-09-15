import chardet

class Extractor:
    """
    A class used to extract English words from a file.

    Attributes:
    ----------
    input_file : str
        The path to the input file.
    output_file : str
        The path to the output file.
    """

    def __init__(self, input_file, output_file):
        """
        Initializes the Extractor object.

        Parameters:
        ----------
        input_file : str
            The path to the input file.
        output_file : str
            The path to the output file.
        """
        self.input_file = input_file
        self.output_file = output_file

    def detect_encoding(self):
        """
        Detects the encoding of the input file.

        Returns:
        -------
        str
            The detected encoding of the input file.
        """
        # Open the input file in binary mode to detect encoding
        with open(self.input_file, 'rb') as f:
            # Use chardet to detect the encoding
            result = chardet.detect(f.read())
            # Return the detected encoding
            return result['encoding']

    def extract_english_words(self):
        """
        Extracts English words from the input file and writes them to the output file.

        Note:
        ----
        This method assumes that the input file is a tab-separated file where the first column contains the English words.
        """
        # Detect the encoding of the input file
        encoding = self.detect_encoding()
        # Open the input file in read mode with the detected encoding
        with open(self.input_file, 'r', encoding=encoding, errors='ignore') as f:
            # Read all lines from the input file
            lines = f.readlines()
        # Open the output file in write mode with UTF-8 encoding
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # Iterate over each line in the input file
            for line in lines:
                # Split the line into parts using the tab character as the delimiter
                parts = line.split('\t')
                # If the line has at least one part, write the first part to the output file
                if len(parts) > 0:
                    f.write(parts[0].strip() + '\n')

    def run(self):
        self.extract_english_words()

if __name__ == '__main__':
    extractor = Extractor('dict.tsv', 'just_english.txt')
    extractor.run()