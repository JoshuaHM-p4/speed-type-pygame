def gross_wpm(entries = 0, time = 0):
    """ Gross, or Raw WPM (Words Per Minute) is a calculation of
    exactly how fast you type with no error penalties."""
    wpm = int((entries/5)/(int(time)/60))
    return wpm

def net_wpm(entries = 0, time = 0, errors = 0):
    """ Net WPM calculation  """
    wpm = int(((entries/5)-errors)/(int(time)/60))
    return wpm

def acc(entries, correct_entries):
    """ Typing Accuracy """
    acc = (correct_entries/entries)*100
    return acc

def acc2(entries, time, errors):
    """ An alternative to the first typing accuracy function  """
    acc2 = (net_wpm(entries, time, errors)*100)/gross_wpm(entries, time)
    return acc2
    