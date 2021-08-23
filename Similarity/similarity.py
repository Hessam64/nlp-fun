from nltk.corpus import wordnet as wn


def get_synsets(word, pos = None):
    if pos is not None:
        if pos == 'a' or pos == 's' or pos == 'A':
            if (pos == 'A'):
                return wn.synsets(word,'a')
            result = []
            synsets = wn.synsets(word,'a')
            for synset in synsets:
                if synset.pos() == pos:
                    result.append(synset)
            return result
        return wn.synsets(word,pos)
    return wn.synsets(word)

def select_sim_func(syn1, syn2, type , ic = None):
    if type == 'path':
        return syn1.path_similarity(syn2)
    if type == 'lcs':
        return syn1.lch_similarity(syn2)
    if type == 'wup':
        return syn1.wup_similarity(syn2)
    if type == 'res':
        return syn1.res_similarity(syn2, ic)

def find_similarity(synset1, synset2, type, option = None, ic = None, skip = False):
    
    
    if option !='first':
        
        max_similarity = float('-inf')
        min_similarity = float('inf')
        sum = 0
        count = 0
        
        for syn1 in synset1:
            for syn2 in synset2:
                if (not skip or syn1.pos() == syn2.pos()  or (syn1.pos() in ['a', 's'] and syn2.pos() in ['a', 's'] )): # For part 2 if it is part2 (skip = True) and syn1.pos() == syn2.pos()
                    if (type not in['lcs', 'res'] or (syn1.pos() == syn2.pos() and type in ['lcs','res'])):
                        count +=1
                        similarity = select_sim_func(syn1,syn2, type, ic)
                        sum += similarity
                        if similarity > max_similarity:
                            max_similarity = similarity
                        if similarity < min_similarity:
                            min_similarity = similarity


        if option is None:
            return max_similarity if max_similarity != float('-inf') else None
        if option == 'avg':
            return sum/ (count)
        if option == 'min':
            return min_similarity if min_similarity != float('inf') else None

    return (select_sim_func(synset1[0], synset2[0], type, ic))

def word_path_similarity(w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)


    return find_similarity(synset1, synset2, 'path' , option = option )

def word_lcs_similarity(w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)

    return find_similarity(synset1, synset2, 'lcs', option = option )

def word_wup_similarity(w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)

    return find_similarity(synset1, synset2, 'wup',  option = option )

def word_res_similarity(ic, w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)
    try:
        return find_similarity(synset1, synset2, 'res', option = option , ic = ic )
    except:
        return None


#*************************** Part 2 *********************************


def get_synset_DRF(synset):
    lemmas = synset.lemmas()
    DRF_list = []

    for lemma in lemmas:
        DRF_list += lemma.derivationally_related_forms()
    return DRF_list


def create_synset_lemmas(lemmas):

    synsets = []

    for lemma in lemmas:
        synsets.append(lemma.synset())
    
    return synsets

def create_DRF_synsets(synset):

    lemmas = get_synset_DRF(synset)
    return create_synset_lemmas(lemmas)

def find_similarity_with_DFR(synsets1, synsets2, type, option = None, ic = None):
    
    
    if option !='first':
        
        max_similarity = float('-inf')
        min_similarity = float('inf')
        sum = 0
        count = 0
        
        for syn1 in synsets1:
            for syn2 in synsets2:
                if (syn1.pos() == syn2.pos() or (syn1.pos() in ['a', 's'] and syn2.pos() in ['a', 's'] )):
                    if (syn1.pos () == 'n'):
                        count +=1
                        similarity = select_sim_func(syn1,syn2, type, ic)
                    else :     
                        lemmas_synsets1 = create_DRF_synsets(syn1)
                        lemmas_synsets2 = create_DRF_synsets(syn2)
                        try:
                            similarity = find_similarity(lemmas_synsets1, lemmas_synsets2, type, option = None, ic = None, skip=True)
                        except:
                            similarity = None
                    if (similarity is not None):
                        sum += similarity
                        count +=1
                        if similarity > max_similarity:
                            max_similarity = similarity
                        if similarity < min_similarity:
                            min_similarity = similarity

        if option is None:
            return max_similarity if max_similarity != float('-inf') else None
        if option == 'avg':
            return sum/ (count)
        if option == 'min':
            return min_similarity if min_similarity != float('inf') else None

    
    if (synsets1[0].pos() != synsets2[0].pos() and not (synsets1[0].pos() in ['a', 's'] and synsets2[0].pos() in ['a', 's'])):
        return None
    if (synsets1[0].pos() == 'n'):
        return (select_sim_func(synsets1[0], synsets2[0], type, ic))
    
    lemmas_synsets1 = create_DRF_synsets(synsets1[0])
    lemmas_synsets2 = create_DRF_synsets(synsets2[0])
    try:
        return find_similarity(lemmas_synsets1, lemmas_synsets2, type, option = None, ic = None, skip=True)
    except:
        return None

def extra_word_path_similarity(w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)

    return find_similarity_with_DFR(synset1, synset2, 'path' , option = option )

def extra_word_lcs_similarity(w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)

    return find_similarity_with_DFR(synset1, synset2, 'lcs', option = option )

def extra_word_wup_similarity(w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)

    return find_similarity_with_DFR(synset1, synset2, 'wup',  option = option )

def extra_word_res_similarity(ic, w1, w2, pos1 = None, pos2 = None, option = None):
    
    synset1 = get_synsets(w1, pos1)
    synset2 = get_synsets(w2,pos2)
    try:
        return find_similarity_with_DFR(synset1, synset2, 'res', option = option , ic = ic )
    except:
        return None