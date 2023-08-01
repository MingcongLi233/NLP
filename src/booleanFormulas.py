
import spacy

abbr2cddt_desc = {
    'LL': ['Left-Hand Drive', 'Drive Left-Hand', 'Left Hand Drive', 'Drive Left Hand'],
    'RL': ['Right-Hand Drive', 'Drive Right-Hand', 'Right Hand Drive', 'Drive Right Hand'],
    'P33BA': ['M Sport Package Pro', 'Package M Pro', 'Sport Package M Pro',
                'Professional M Sport Package', 'Professional Package M', 'Professional Sport Package M'],
    'P337A': ['M Sport Package', 'Package M', 'Sport Package M', 'Package Sport M'],
    'P7LGA': ['Comfort Package EU', 'EU Comfort Package', 'EU Package'],
    'S407A': ['Sky Lounge Panorama Glass Roof', 'Panorama Sky Lounge Glass Roof', 
                'Sky Lounge Panorama Roof', 'Sky Lounge Roof', 'Panorama Roof Sky Lounge', 'Roof Sky Lounge'],
    'S402A': ['Panorama Glass Roof', 'Panorama Roof', 'Roof Panorama'],
    'S403A': ['Sunroof']
} # list the possible descriptions of each abbreviation
desc2abbr = {} # reverse the abbr2cddt_desc
for abbr, desc_list in abbr2cddt_desc.items():
    for desc in desc_list:
        desc2abbr[desc] = abbr


def format_list(lst):
    '''
    Format the list to a string
    '''
    list_formatted = [(), (), ()]
    for cddt in lst:
        abbr = desc2abbr[cddt]
        if abbr in ['LL', 'RL']:
            list_formatted[0] += (cddt,)
        elif abbr in ['P337A', 'P33BA', 'P7LGA']:
            list_formatted[1] += (cddt,)
        else:
            list_formatted[2] += (cddt,)

    return list_formatted


def find_willing_and_unwilling(sentence_lower, all_cddts):
    '''
    Find the willing and unwilling list
    '''
    hate_kwds = ['without', 'does not', 'do not', ' not ', 'not have', 'not has', 
                 'have no', 'has no', 'not include', 'not includes', 'not including', 'not equipped with',
                 'having no', 'not having', ' excludes ', ' excluding ', ' excluded ', ' exclude ']
    hate_kwds_formatted = ['-'.join(kwd.split(' ')) for kwd in hate_kwds]
    for kwd in hate_kwds:
        if kwd in sentence_lower:
            sentence_lower = sentence_lower.replace(kwd, '-'.join(kwd.split(' ')))
    want_kwds = [' with ', 'includes', 'include', 'including', 'has', 'have', 'having', 'contain', 'equipped with']
    all_kwds = hate_kwds_formatted + want_kwds
    willing = []
    unwilling = []
    flag = 0
    for cddt in all_cddts:
        idx = sentence_lower.find(cddt.lower())
        prefix = sentence_lower[:idx]
        if any(word in prefix for word in all_kwds):
            # first find the nearest keyword
            nearest_kwd = ''
            nearest_idx = -1
            for word in all_kwds:
                if word in prefix:
                    if prefix.find(word) > nearest_idx:
                        nearest_kwd = word
                        nearest_idx = prefix.find(word)
            if nearest_kwd in hate_kwds_formatted:
                unwilling.append(cddt)
            else:
                willing.append(cddt)
        else:
            willing.append(cddt) # defalut is willing!! TODO

    # format
    willing_formatted = format_list(willing)
    unwilling_formatted = format_list(unwilling)
    
    return willing_formatted, unwilling_formatted


def generate_boolean_formula(doc):
    formula = ""
    sentences = [sent.text for sent in doc.sents]

    for sentence in sentences:
        sentence_lower = sentence.lower()
        all_cddts = [] # all the possible configurations
        ##### 1. find all the configurations mentioned in the sentence
        for abbr, desc_list in abbr2cddt_desc.items():
            for desc in desc_list:
                desc_lower = desc.lower()
                if desc_lower in sentence_lower:
                    sentence_lower = sentence_lower.replace(desc_lower, '')
                    all_cddts.append(desc)
        ##### 2. find the willing and unwilling list
        wants, wants_not = find_willing_and_unwilling(sentence.lower(), all_cddts)
        # print(f"wants: {wants}")
        # print(f"wants_not: {wants_not}")
        ##### 3. generate the boolean formula
        if wants == [(), (), ()] and wants_not == [(), (), ()]:
            # print("No configuration mentioned in the sentence")
            continue
        else:
            for w, wn in zip(wants, wants_not):
                if w == () and wn == ():
                    continue
                elif w == ():
                    if len(wn) == 1:
                        formula += '-' + desc2abbr[wn[0]]
                    else: # to be checked
                        formula += '-+(' + '/'.join([desc2abbr[cddt] for cddt in wn]) + ')' 
                elif wn == ():
                    if len(w) == 1:
                        formula += '+' + desc2abbr[w[0]]
                    else:
                        formula += '+(' + '/'.join([desc2abbr[cddt] for cddt in w]) + ')'
                else:
                    if len(w) == 1:
                        formula += '+' + desc2abbr[w[0]]
                    else:
                        formula += '+(' + '/'.join([desc2abbr[cddt] for cddt in w]) + ')'
                    if len(wn) == 1:
                        formula += '-' + desc2abbr[wn[0]]
                    else: # to be checked
                        formula += '-+(' + '/'.join([desc2abbr[cddt] for cddt in wn]) + ')'

    return formula
