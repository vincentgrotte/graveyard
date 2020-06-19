ctrlc = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way - in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only. Decrypt!"

# input = "It was the best of times, it was the worst of times, it was the age of wisdom, " +\
# "it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, " +\
# "it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the " +\
# "winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven,"+\
# " we were all going direct the other way - in short, the period was so far like the present period," +\
# " that some of its noisiest authorities insisted on its being received, for good or for evil," +\
# " in the superlative degree of comparison only. Decrypt!"

# words = input.split(" ")

# first_letters = [word[0].lower() for word in words]

# output = "".join(first_letters)

# print(output)
# iwtbotiwtwotiwtaowiwtaofiwteobiwteoiiwtsoliwtsodiwtsohiwtwodwhebuwhnbuwwagdthwwagdtow
# -istpwsfltpptsoinaioibrfgofeitsdocod

text1 = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way"
text2 = " in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only. Decrypt!"

# def decrypto(string):
#     output = ""

#     for letter in string:
#         if letter == " ":
#             output += "a"
#             # output += "b"
#         elif letter.isalnum():
#             # output += "a"
#             output += "b"
#         elif letter == ",":
#             output += " "

#     return output

# print(decrypto(text1))
# print(decrypto(text2))

# text3 = "eirtbeirkateitateitaateierescbeabeirerkcebeakcebeescatakcabakeibakeeiebebeeiebcbcieicesbcaicccirbaaiatecaeikcciraebeacca"

# print(text3[::-1])

lc2bin = {ch: '{:05b}'.format(i) 
          for i, ch in enumerate(string.ascii_lowercase + ' .')}
bin2lc = {val: key for key, val in lc2bin.items()}

def decrypt(bacontext):
    binary = []
    bin5 = []
    out = []
    for ch in bacontext:
        if ch.isalpha():
            binary.append('1' if ch.isupper() else '0')
            if len(binary) == 5:
                bin5 = ''.join(binary)
                out.append(bin2lc[bin5])
                binary = []
    return ''.join(out)


print(decrypt(ctrlc))



































































