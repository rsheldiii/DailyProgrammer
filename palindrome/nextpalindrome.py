#given a number, we find the next base 10 digit palindrome after that number.


#known knowns:
#every digit change there is ALWAYS a palindrome before it. Always. which means we don't have to worry about changing digits once we add 1 (since we're getting the next palindrome)
import time

def nextPalindrome(n):
    n += 1
    #will never have to deal with middle number, because it doesnt have to match anything
    for i in range(0,len(str(n))//2):
        while str(n)[i] != str(n)[-(i+1)]:
            n += 10**i
    return(str(n))

def timer(function, n):#I know there's a better way to do this with the @ symbol but I never bothered how
    before = time.time()
    returnstr = function(n)
    after = time.time()

    print (str(n) + " is " + returnstr + " and took " + str(after-before) + " seconds")





timer(nextPalindrome,808)
timer(nextPalindrome,999)
timer(nextPalindrome,2133)
timer(nextPalindrome,3**39)
timer(nextPalindrome,7**100)


input("end")
