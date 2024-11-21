"""
Given a text file with raw descriptions of actions, tag each description with
parts-of-speech tags, then write them in the training format to a new file.
"""

import spacy

nlp = spacy.load('en_core_web_sm')

def process_text(sentence: str) -> tuple[list[str], list[str]]:
    """
    Return lists of words and their parts of speech (POS) tags
    for a given sentence.

    :param sentence:    string to be tagged
    :return word_list:  list of tokens found in the sentence
    :return pos_list:   list of part-of-speech tags by token
    """
    sentence = sentence.replace('-', '')
    doc = nlp(sentence)
    word_list = []
    pos_list = []
    for token in doc:
        word = token.text
        if not word.isalpha():
            continue
        if (token.pos_ in ("NOUN", "VERB")) and (word != 'left'):
            word_list.append(token.lemma_)
        else:
            word_list.append(word)
        pos_list.append(token.pos_)
    return (word_list, pos_list)


def read_text_from_file(input_file: str) -> list[str]:
    """
    Read the text from a file of action descriptions for parsing.

    :param input_file:  string path to the input file
    :return result:     list of strings read from the input file
    """
    with open(input_file, 'r', encoding="utf-8") as infile:
        raw_lines = infile.readlines()
        result = [line.strip() for line in raw_lines]

    return result


def prepare_combined_line(sentence: str, start_time: float=0.0, end_time: float=0.0) -> str:
    """
    Given each sentence, parse it and attach tags to each token.
    Then include the description start and end time to be edited if needed.
    By default, these are 0.0 if we are describing the full sequence.

    :param sentence:    string containing an input sentence
    :param start_time:  float representing start time of the description
    :param end_time:    float representing end time of the description
    :return combined_line:  string containing sentence#tagged_sentence#start_time#end_time
    """
    (words, tags) = process_text(sentence)
    tagged_sentence = ' '.join([f"{n[0]}/{n[1]}" for n in zip(words, tags)])
    combined_line = f"{sentence}#{tagged_sentence}#{start_time}#{end_time}\n"

    return combined_line


def write_output_file(output_list: list[str], output_file: str):
    """
    Write a specified output list to a specified file.

    :param output_list:     list of strings to write
    :param output_file:     string path to output file location
    """
    with open(output_file, 'w', encoding="utf-8") as outfile:
        outfile.writelines(output_list)


def main():
    """
    Actually run the conversion here.
    """
    output = []
    strings = []
    INPUT_FILE = "testfile.txt"
    OUTPUT_FILE = "taggedfile.txt"

    strings = read_text_from_file(input_file=INPUT_FILE)

    for input_line in strings:
        output_line = prepare_combined_line(input_line)
        output.append(output_line)

    write_output_file(output_list=output, output_file=OUTPUT_FILE)

if __name__ == "__main__":
    main()
