from keras.layers.recurrent import GRU,LSTM
from keras.layers.embeddings import Embedding
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential,model_from_json
from keras.layers.core import Dense,RepeatVector
import MeCab

MODEL_STRUCT_FILE = 'piglatin_struct.json'
MODEL_WEIGHTS_FILE = 'piglatin_weights.h5'

class keras_seq2seq():
    def __init__(self,filename):
        self.MAX_VOCABULARY=60000
        self.EMBEDDING_DIM = 300
        self.HIDDEN_DIM = 300
        self.MAX_INOUT_LEN = 100
        self.data_read(filename)
    def data_read(self,filename):
        questions = []
        answers = []
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                sentences = line.split("\t")
                question = ["<start>"] + self.parse_sentence(sentences[0]) + ["<eos>"]
                answer = self.parse_sentence(sentences[1]) + ["<eos>"]
                questions.append(question)
                answers.append(answer)
        word2id = {"■": 0}
        id2word = {0: "■"}
        word2id['<start>'] = 1
        id2word[1] = '<start>'
        word2id['<eos>'] = 2
        id2word[2] = '<eos>'
        word2id['<pad>'] = 3
        id2word[3] = '<pad>'
        id = 4

        sentences = questions + answers
        for sentence in sentences:
            for word in sentence:
                if word not in word2id:
                    word2id[word] = id
                    id2word[id] = word
                    id += 1

        self.questions=questions
        self.answers=answers
        self.word2id=word2id
        self.id2word=id2word
    def parse_sentence(self,sentence):
        parsed = []
        m = MeCab.Tagger(' -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
        for chunk in m.parse(sentence).splitlines()[:-1]:
            parsed.append(chunk.split('\t')[0])
        return parsed
    def build_model(self):
        #seq2seqのモデル作成
        model = Sequential()
        model.add(Embedding(vocab+1,self.EMBEDDING_DIM,input_length=self.MAX_INOUT_LEN))
        model.add(LSTM(self.HIDDEN_DIM,return_sequences=False))
        model.add(RepeatVector(self.MAX_INOUT_LEN))
        model.add(LSTM(self.HIDDEN_DIM, return_sequences=True))
        model.add(TimeDistributed(Dense(output_dim=vocab,activation='softmax')))

        model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

        return model
    def run(self):
        pass

if __name__=='__main__':
    my=keras_seq2seq()
