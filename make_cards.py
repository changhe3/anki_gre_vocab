import argparse
from PyDictionary import PyDictionary
import csv

class Anki(object):

    def __init__(self,  vocab_file, output_file, error_file):
        self.vocab_file = vocab_file
        self.output_file = output_file
        self.error_file = error_file

    def read_vocab_file(self):
        vocab_list = [word.rstrip() for word in  open(self.vocab_file).readlines()]
        return vocab_list

    def define_vocab(self,vocab_list,verbose):
        dictionary = PyDictionary()
        defs_list = list()
        error_list= list()
        for word in vocab_list:
            if dictionary.meaning(word) != "":
                if verbose:
                    print([word, dictionary.meaning(word)])
                defs_list.append(dictionary.meaning(word))
            else:
                if verbose:
                    print("%s has been added to the error list"%word)
                error_list.append(word)
        return  defs_list, error_list

    def make_deck(self,vocab_list,defs_list,verbose):
        with open(self.output_file,"w") as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            for word, definition in zip(vocab_list,defs_list):
                writer.writerow([word, definition])
        if verbose:
            print("anki deck has been created.")
        return self.output_file

    def write_errors(self,error_list,verbose):
        with open(self.error_file,"w") as csvfile:
            writer = csvwriter(csvfile, delimiter = '\t')
            for err in error_list:
                writer.writerow(err)
        if verbose:
            print("error log has beenw written.")
        return self.error_file

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This script makes anki flash cards from a text file of vocab words.')
    parser.add_argument('vocab_file', metavar='vocab_file', action="store",
                        help='txt file full of vocab words')
    parser.add_argument('-o', '--output_file', metavar='output_file',
                        default='anki_gre_vocab.txt', action="store",
                        help='output anki deck txt file')
    parser.add_argument('-e', '--error_file',metavar='error_file',
                        default='error_words.txt',action="store",
                        help='error file for the words that there were no definitions')
    parser.add_argument('-m','--edit_mode', dest='edit_mode',default=False,
                        action="store_true", help='manually edit mode allows for the editing of an existing deck file to manually edit definitions')
    parser.add_argument('-v','--verbose', dest='verbose',default=False,
                        action="store_true", help='verbose mode')

    args = parser.parse_args()

    if ~args.edit_mode:
        anki = Anki(args.vocab_file, args.output_file,args.error_file)
        vocab_list = anki.read_vocab_file()
        defs_list, error_list = anki.define_vocab(vocab_list, args.verbose)
        anki_deck = anki.make_deck(vocab_list,defs_list,args.verbose)
        error_log = anki.write_errors(error_list,args.verbose)
    else:
        print('edit mode in progress')
