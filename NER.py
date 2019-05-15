from sets import Set
from math import *;
from copy import *;
import sys;
# pi={}
a={}
b={}
default_mass=0.000000000001
neg_inf = -1* float('inf');

def trainModel(filePath):
    f = open(filePath);
    prevsplits=[];
    words = Set();
    for line in iter(f):
        splits = line.split();
        if len(splits) == 0:
            a[prevsplits[2]]['stop'] = a.setdefault(prevsplits[2],{}).setdefault('stop',0)+1;
        else:
            b[splits[2]][splits[0]]= b.setdefault(splits[2],{}).setdefault(splits[0],0)+1;
            words.add(splits[0])
            if len(prevsplits)==0 :
                a['start'][splits[2]] = a.setdefault('start',{}).setdefault(splits[2],0)+1;
                
            else  :
                a[prevsplits[2]][splits[2]]=a.setdefault(prevsplits[2],{}).setdefault(splits[2],0)+1;
        
        
        prevsplits = splits;
    
    print len(b.keys());
#     smooth the shit
    for key in a.keys():
        sum = 0;
        for subkey in a[key].keys():
            sum = sum + a[key][subkey]
        for subkey in a[key].keys():
            a[key][subkey] = log(float(a[key][subkey])/float(sum));
    
    for key in b.keys():
        sum = 0;
        for subkey in b[key].keys():
            sum = sum+b[key][subkey]; 
        for subkey in b[key].keys():
            b[key][subkey] = log(float(b[key][subkey])/float(sum));
        
    b['start']['<start>']=log(b.setdefault('start',{}).setdefault('<start>',0)+1);
    b['stop']['<stop>']=log(b.setdefault('stop',{}).setdefault('<start>',0)+1);
    

    
def decode(obs):
#     StateSpace = a.keys();
    print obs
    StateSpace= [];
    for key in a.keys():
        StateSpace.append(key)
    StateSpace.append('stop');
#     StateSpace = StateSpace.append('stop');
    q=[{}];
    q.append({});
    path={};
    
    for state in StateSpace:
        q[1][state] = a.get('start',{}).get(state,log(default_mass)) + b.get(state,{}).get(obs[1],log(default_mass));
        path[state]=['start',state];
    for n in xrange(2, len(obs)):
        newPath = {};
        q.append({})
        for state in StateSpace:
            max_prob = neg_inf;
            best_state='';
            for state_prev in StateSpace:
#                 print("checking from "+ state_prev + " to "+state + " for n= "+str(n)+"  "+obs[n]);
                prob = a.get(state_prev,{}).get(state, log(default_mass)) + q[n-1][state_prev] + b.get(state, {}).get(obs[n],log(default_mass));
                (max_prob  , best_state) = max((max_prob, best_state),(prob, state_prev));
            q[n][state] = max_prob;
#             print path;
#             if path.has_key(best_state):
#                 print path[best_state]
#             else :
#                 print "fuceked " + best_state;
#             print "updating " + state + "  with "+ best_state;
            tmp = deepcopy(path[best_state]);
            tmp.append(state);
            newPath[state] = tmp;
#             print("-------------------------------------------------------------")
        
        path = newPath;
#         print path;
    
    (best_prob, best_state)  = max((q[len(obs)-1][state],state) for state in StateSpace);
    print best_prob;
    return path[best_state];
#     print path[best_state];
#     print best_prob;
    
def testModel(filePath, outPath):
    f = open(filePath);
    w = open(outPath,'w')
    sentence=['<start>'];
    correct_tags=['start'];
    tokensList=[];
    count =0;
    for line in iter(f):
        tokensList.append(line.rstrip());
        splits= line.split();
        if len(splits)==0 :
            print "tagging sentence: "+str(count);
            count+=1;
            sentence.append('stop');
            correct_tags.append('<stop>');
            taggged_sentence = decode(sentence);
#             print taggged_sentence;
            for i in xrange(1, len(taggged_sentence)-1):
                w.write(tokensList[i-1]+" "+taggged_sentence[i]+'\n');
            w.write('\n');
            
            sentence =['<start>'];
            correct_tags=['start'];
            tokensList=[];
        else :
            sentence.append(splits[0]);
            correct_tags.append(splits[2]);
    f.close();
    w.close();
	
#penambahan fitur
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    
    features = {
        'bias': 1.0, 
        'word.lower()': word.lower(), 
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True
	return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]
def sent2labels(sent):
    return [label for token, postag, label in sent]
def sent2tokens(sent):
    return [token for token, postag, label in sent]
	
            
if __name__ == '__main__':
    if len(sys.argv)<3:
        print 'Usage python ner_train.py trainfile testfile testOutput'
    else:
        trainModel(sys.argv[1]);
        testModel(sys.argv[2],sys.argv[3]);