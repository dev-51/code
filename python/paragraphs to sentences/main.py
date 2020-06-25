import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

def breakSignal(data, str):
    sentences = data
    new_sentences = []

    for s in sentences:        
        if s.find('"') == -1 and s.find(str) != -1:            
            ss = s.split(str)
            
            for r in ss:
                if s.find(r+str) != -1:
                    new_sentences.append(r.strip() + str)
                else:
                    new_sentences.append(r.strip())
        else:
            new_sentences.append(s)

    return new_sentences

def breakQuotes(data, str):
    new_sentences = []
    for s in sentences:
        s = s.strip()

        index_start = s.find('"')
        if index_start != -1 and index_start < len(s) - 1:
            index_end = s.find('"', index_start + 1)

            if index_end != -1:
                s_left = s[:index_start].strip()
                s_middle = s[index_start:index_end+1].strip()
                s_right = s[index_end+1:].strip()
                                                                
                if len(s_left): new_sentences.append(s_left)
                new_sentences.append(s_middle)
                if len(s_right): new_sentences.append(s_right)
        else:
            new_sentences.append(s)
    
    return new_sentences

def breakUp(data, str):
    sentences = data.split(str)
    new_sentences = []

    for s in sentences:
        s = s.strip()
        if len(s) == 0: #last delimiter makes s contain empty value
            pass
        else:    
            new_sentences.append(s + str)
    return new_sentences

if __name__ == "__main__":
    data = ''
    #with open('paragraph.txt', 'r') as f:
    #    data = f.read()
    #    print(data)
    #    print('==================================================')        
    data = sys.stdin.read()

    sentences = breakUp(data, '.')
    #pp.pprint(sentences)
    #sentences = breakQuotes(sentences, '"')
    #pp.pprint(sentences)
    sentences = breakSignal(sentences, '?')
    #pp.pprint(sentences)
    sentences = breakSignal(sentences, '!')
    #pp.pprint(sentences)
    output = ''
    for s in sentences:    
        output += s+'\n'
    
    #print(output)
    sys.stdout.write(output)
    