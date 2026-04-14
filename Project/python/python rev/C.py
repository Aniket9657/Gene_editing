word = input("enter the word : ")
len(word)
print(len(word)//2)


def palin_check(word):
    for w in range(len(word)//2):
        print("to check iteration")
        if word[w] != word[len(word)-1-w]:
            return False
    return True
        
word ="AWW"
print(palin_check(word))
 