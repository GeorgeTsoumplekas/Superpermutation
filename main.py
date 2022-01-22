'''
Ονομα: Γιωργος Τσουμπλέκας
ΑΕΜ: 9359
Email: gktsoump@ece.auth.gr

Στο παρόν πρόγραμμα, δεδομένου ενός θετικού ακεραίου n, επιθυμούμε να βρούμε το string με το ελάχιστο μήκος το οποίο περιέχει όλες τις n-μεταθέσεις (superpermutation).
Η συγκεκριμένη υλοποίηση βασίζεται σε έναν αναδρομικό αλγόριθμο ο οποίος δείχνει πώς από το (n-1)-superpermutation μπορούμε να δημιουργήσουμε το n-superpermutation.

Για ευκολία χειρισμού των χαρακτήρων χρησιμοποιήθηκαν κεφαλαία λατινικά γράμματα αντί για ψηφία. Έτσι, θεωρητικά μπορουμε να εξετάσουμε μέχρι και την περίπτωση n = 26. Βέβαια, ήδη για n>10 το πρόγραμμα εμφανίζει αρκετα μεγάλο
χρόνο εκτέλεσης οπότε η μελέτη μεγαλύτερων n παρουσιάζει μόνο θεωρητικό και όχι πρακτικό ενδιαφέρον.
Τα γράμματα θα μπορούσαν να μετατραπούν από κωδικα ASCII σε ακεραίους (A -> 1, B -> 2, κοκ) αλλά προτιμήθηκε να μην γίνει για να μην έχουμε την επιπλέον επιβάρυνση στον χρόνο εκτέλεσης του προγράμματος.

Μέχρι και για n = 8  οι χρόνοι εκτέλεσης είναι πολύ μικροί. Έπειτα:
n = 9: t = 6,15s
n = 10: t = 4166,75 s = 1h 9,5mins (approximately)
Για n = 11 και μεγαλύτερα ο χρόνος εκτέλσης γίνεται σημαντικά μεγαλύτερος
'''

import itertools
import time
import math


# Στην συνάρτηση αυτή υλοποιείται ο αλγόριθμος με τον οποίο παράγουμε αναδρομικά το n-superpermutation από το (n-1)-superpermutation
def superpermutation(n):
    final_result = ""
    if n == 1:
        final_result = "A"
        return final_result
    else:
        prev = superpermutation(n - 1)
        p_list = find_permutations(prev, (
                n - 1))  # 1. Store in a list the permutations in the original superpermutation, in the order in which they appear.
        for it in p_list:
            final_result = final_result + it + str(
                chr(n + 64)) + it  # 2. Duplicate each of them, placing the new symbol n between the two copies.
            x = int(len(final_result)) - 2 * int(
                len(it)) - 1  # x := index at the beginning of the new elements added on the string
            initial = final_result[x]
            # 3. Squeeze the result back together again, making use of all available overlaps.
            if x != 0:  # If there elements before the newly added ones in the string:
                i = x - 1
                while final_result[i] != initial and final_result[i] != str(chr(n + 64)):  # Delete all letters before the first letter of the newly added string until we find one which is the same as this.
                    final_result = final_result[:i] + final_result[i + 1:]
                    i = i - 1
                if final_result[i] == initial:  # Then, delete this too, so we don't have the same letters back to back.
                    final_result = final_result[:i] + final_result[i + 1:]
        return final_result

# Ελέγχει αν το n-superpermutation περιέχει όλα τα n-permutations
def check_superpermutation(super_perm, size):
    perms_list = find_permutations(super_perm, size) # Ο αναδρομικός τρόπος δημιουργίας του superpermutation και η λειτουργία της find_permutations εξασφαλίζει οτι όλα τα permutations που περιέχει η perms_list είναι διαφορετικα το ένα από το άλλο.
    if len(perms_list) == math.factorial(size): # n-μεταθέσεις n-αντικειμένων = n!
        return True
    else:
        return False


#Βρίσκει όλα τα n-permutations που περιέχονται σε ένα n-superpermutation
def find_permutations(super_perm, n):
    list1 = []
    a = ''
    b = 0
    for x in range(0, int(len(super_perm)) - n + 1):
        for y in range(x, x + n):
            a = a + super_perm[y] # a =: string μήκους n που περιέχει ένα συγκεκριμένo n-permutation
            b = b + ord(super_perm[y]) - 64 # b := το άθροισμα των ψηφίων του permutation
        if b == n * (n + 1) / 2: # Αν το a είναι ένα έγκυρο permutation τότε θα περιέχει όλα τα ψηφία από 1 μέχρι n ακριβως μια φορά. Έτσι, το άθροισμα των ψηφίων του θα ισούται με n*(n+1)/2 βάσει της γνωστής ταυτότητας.
            list1.append(a)
        a = ''
        b = 0
    return list1

# Main script
n = -1
while n <= 0:
    n = int(input("Type a positive integer: "))
start = time.time()
superperm = superpermutation(n)
check = check_superpermutation(superperm, n)
end = time.time()
print("The superpermutation is: " + superperm)
print("Length of the superpermutation:", len(superperm))
print("Execution time:", end - start, "s")
if check is True:
    print("All permutations found in the superpermutation")
else:
    print("Error! Not all permutations found in the superpermutation.")
