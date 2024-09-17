import chardet
import random

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
   
    def extract_lexemes(self):
        """
        Extracts English words and their IPA spellings from the input file and writes them to the output file in the desired format.

        Note:
        ----
        This method assumes that the input file is a tab-separated file where the first column contains the English words and the second column contains the IPA spellings.
        """
        # Detect the encoding of the input file
        encoding = self.detect_encoding()
        # Open the input file in read mode with the detected encoding
        with open(self.input_file, 'r', encoding=encoding, errors='ignore') as f:
            # Read all lines from the input file
            lines = f.readlines()
        # Open the output file in write mode with UTF-8 encoding
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # Write the header to the output file
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<lexicon version="1.0"\n')
            f.write('      xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"\n')
            f.write('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
            f.write('      xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon\n')
            f.write('        http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"\n')
            f.write('      alphabet="ipa" xml:lang="en-US">\n')
            
            # Iterate over each line in the input file
            for line in lines:
                # Split the line into parts using the tab character as the delimiter
                parts = line.split('\t')
                # If the line has at least two parts, write the lexeme to the output file
                if len(parts) > 1:
                    english_word = parts[0].strip()
                    ipa_spelling = parts[1].strip()
                    f.write('  <lexeme>\n')
                    f.write('    <grapheme>{}</grapheme>\n'.format(english_word))
                    f.write('    <phoneme>{}</phoneme>\n'.format(ipa_spelling))
                    f.write('  </lexeme>\n')
            
            # Close the lexicon tag
            f.write('</lexicon>\n')

        """     def generate_words(self, word_list, num_words):
        # Ensure each letter is represented
        letter_words = {}
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            letter_words[letter] = [word for word in word_list if word.startswith(letter)]
        
        # Sample words from each letter's list
        sampled_words = []
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if letter_words[letter]:
                sampled_words.extend(random.sample(letter_words[letter], min(1, len(letter_words[letter]))))
        
        # Fill the rest of the quota with random words from the entire list
        remaining_words = num_words - len(sampled_words)
        if remaining_words > 0:
            sampled_words.extend(random.sample(word_list, min(remaining_words, len(word_list))))
    
        return sampled_words """

    def generate_words(self, word_list, num_words):
        words = []
        letter_pairs = {}
        for letter1 in 'abcdefghijklmnopqrstuvwxyz':
            for letter2 in 'abcdefghijklmnopqrstuvwxyz':
                pair = letter1 + letter2
                letter_pairs[pair] = [word for word in word_list if word.startswith(pair) and len(word) >= 5]
        
        for pair in letter_pairs:
            if letter_pairs[pair]:
                words.extend(random.sample(letter_pairs[pair], min(9, len(letter_pairs[pair]))))
        
        # Fill the rest of the quota with random words from the entire list
        remaining_words = num_words - len(words)
        if remaining_words > 0:
            words.extend(random.sample(word_list, min(remaining_words, len(word_list))))
        
        return words[:num_words]

    def read_words_from_file(self, temp_file):          
        with open(temp_file, 'r') as file:
            return [line.strip() for line in file.readlines()]
    
    def shrink_database (self):
        word_list = self.read_words_from_file(self.input_file)
        words = self.generate_words(word_list, 3000)

        with open(self.output_file, 'w') as file:
            for word in words:
                file.write(word + '\n')

    def run(self):
        self.shrink_database()
        # self.extract_lexemes() 
        # self.extract_english_words()


if __name__ == '__main__':
    # extractor = Extractor('dict.tsv', 'dictionary.pls') #Lexemes format
    # extractor = Extractor('dict.tsv', 'just_english.txt') #English words format
    extractor = Extractor('just_english.txt', 'small_dictionary.txt') #Shrink database
    extractor.run()