
class analysedText(object):

    def __init__(self, text):
        # TODO: Assign the formatted text to a new attribute called "fmtText"
        fmtText = text.lower().replace(('.', '!', '?', ','), '')

    def freqAll(self, fmtText):
        # TODO: Split the text into a list of words
        fmtText.split()
        # TODO: Create a dictionary with the unique words in the text as keys
        for key in set(fmtText):
            dict = {key: fmtText.count(key)}
        # and the number of times they occur in the text as values
        return dict  # return the created dictionary

    def freqOf(self,fmtText,word):
        return fmtText.count(word)


newtext = "Lorem ipsum dolor! diam amet, consetetur Lorem magn" \
"a. sed diam nonumy eirmod tempor. diam et labore? et diam magna. et diam amet."


newtext.lower()
edited = newtext.lower().replace('.','').replace('!','').replace('?', '').replace(',', '')
print(edited.split(''))