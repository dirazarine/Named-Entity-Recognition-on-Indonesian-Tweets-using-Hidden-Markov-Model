# Named-Entity-Recognition-on-Indonesian-Tweets-using-Hidden-Markov-Model

how to run NER.py at cmd
py -2 NER.py train test testoutput

use conlleval
> copy the HMM results in 'testoutput' to output.txt which is in the conlleval-master.rar file
> run conlleval.py using this code:
  >> py -3 conlleval.py < output.txt
