# Import the sys functionality to read the arguments
import sys


# Function that constructs the F matrix from two arrays A and B
# It is generated at the correct size, but with None values that have to be filled
def Fconstructor(A,B,g):

    # Create the matrix
    F = [None]*(len(A)+1)
    for i in range(len(A)+1):
        F[i] = [None]*(len(B)+1)
    
    # Set the initial values
    for i in range(len(F)):
        F[i][0] = -g*i
    for j in range(len(F[0])):
        F[0][j] = -g*j

    # Finally return the function
    return F

# Function that finds the value of matrix F at the position specified
# The F matrix is passed through recursion, and the value is generated if
# not already present
def Fgenerator(A,B,F,m,d,g,i,j):
    # Note that A and B must both contain at least one element

    # Check that you are within bounds
    if i >= len(F) or j >= len(F[0]):
        print("( "+str(i)+", "+str(j)+") is out of bounds for F")
        return None

    # Check if the value is already present
    if F[i][j] != None:
        return F[i][j]

    # If it is not present, generate it
    if i+j == 0:
        F[i][j] = 0
    elif j == 0:
        F[i][j] = -g*i
    elif i == 0:
        F[i][j] = -g*j
    else:
        F[i][j] = max(
            Fgenerator(A,B,F,m,d,g,i-1,j)-g,
            Fgenerator(A,B,F,m,d,g,i,j-1)-g,
            Fgenerator(A,B,F,m,d,g,i-1,j-1)+m if A[i-1] == B[j-1]
            else Fgenerator(A,B,F,m,d,g,i-1,j-1)-d
        )


    # You found and have written the value, so just return it
    return F[i][j]






# Functions that are given to us as is
def enumerate_alignments(A,B,F,W,Z,Compare,g, WW,ZZ):

    i = len(A)
    j = len(B)

    # Check for lists
    dash = '-'
    if type(A) != str:
        dash = ['-']

    if i == 0 and j == 0:
        WW.append(W)
        ZZ.append(Z)
        return
    if i>0 and j>0:
        m = Compare(A[i-1],B[j-1])
        if F[i][j] == F[i-1][j-1]+m:
            a = A[i-1] if type(A) == str else [A[i-1]]
            b = B[j-1] if type(B) == str else [B[j-1]]
            enumerate_alignments(A[0:i-1],B[0:j-1],F,a+W,b+Z,Compare,g,WW,ZZ)
            if type(A) != str:
                return # This puts a priority on not having gaps when reading files
    if i > 0 and F[i][j] == F[i-1][j]-g:
        a = A[i-1] if type(A) == str else [A[i-1]]
        enumerate_alignments(A[0:i-1],B,F,a+W,dash+Z,Compare,g,WW,ZZ)
    if j > 0 and F[i][j] == F[i][j-1]-g:
        b = B[j-1] if type(B) == str else [B[j-1]]
        enumerate_alignments(A,B[0:j-1],F,dash+W,b+Z,Compare,g,WW,ZZ)


# Compute allignment score
def compute_alignment_score(A,B,Compare, g):

    L = [0]*(len(B)+1)
    for j in range(len(B)+1):
        L[j] = j*g
    K = [0]*(len(B)+1)    
    for i in range(1,len(A)+1):
        L,K = K,L
        L[0] = i*g
        for j in range(1,len(B)+1):
            md = Compare(A[i-1],B[j-1])
            L[j] = max(L[j-1]+g,K[j]+g,K[j-1]+md)
    return L


#Hirschberg
def hirschberg(A,B,Compare,g,verbose=False):


    # Define the outputs to be lists
    WW = []
    ZZ = []

    # Check for lists
    empty = ""
    if type(A) != str:
        empty = []

    if len(A) == 0:
        WW = ['-'*len(B)] if type(A) == str else [['-']*len(B)]
        ZZ = [B]
    elif len(B) == 0:
        WW = [A]
        ZZ = ['-'*len(A)] if type(A) == str else [['-']*len(A)]
    elif len(A) == 1 or len(B) == 1:
        # Create the arrays for the enumeration
        WW,ZZ = [],[]

        # Create and calculate the F array
        F = Fconstructor(A,B,g)
        Fgenerator(A,B,F,Compare(1,1),-Compare(1,0),g,len(A),len(B))

        # Enumerate
        enumerate_alignments(A,B,F,empty,empty,Compare,g,WW,ZZ)
        #print(WW,ZZ)
    else:
        Ar = A[::-1]
        Br = B[::-1]
        i = len(A) // 2
        Sl = compute_alignment_score(A[0:i],B,Compare,-g)
        Sr = compute_alignment_score(A[i:][::-1],Br,Compare,-g)
        Srr = Sr[::-1]
        S = [Sl[i]+Srr[i] for i in range(len(Sl))]
        Smax = max(S)
        J = [jj for jj in range(len(S)) if Smax==S[jj]]
        for j in J:

            # Print the i, j tupple if you are on verbose mode
            if verbose:
                print(str(i)+',',j)

            # Do the recursion to obtain the results
            WWl, ZZl = hirschberg(A[0:i],B[0:j],Compare,g,verbose)
            WWr, ZZr = hirschberg(A[i:],B[j:],Compare,g,verbose)

            # We need to concatenate those two
            for l in range(len(WWl)):
                for k in range(len(WWr)):

                    # Create the new element
                    wwn = WWl[l]+WWr[k]
                    zzn = ZZl[l]+ZZr[k]
                    
                    # Append to the lists
                    WW.append(wwn)
                    ZZ.append(zzn)

    # Remove doubles before returning
    combined = zip(WW,ZZ)
    c_unique = []
    for c in combined:
        if c not in c_unique:
            c_unique.append(c)

    # Extract the elements from that
    WW,ZZ = [],[]
    for w,z in c_unique:
        WW.append(w)
        ZZ.append(z)      
    
    return (WW,ZZ)

# A sample compare function
def compare(a,b,match, differ):
    return match if a == b else differ


def file_string(filename, lines):
    # This will read a file and return it as a string
    # If lines is checked, it will return a list of strings that
    # correspond to the file lines

    # Define variable for output
    output = None

    # Open the file and read it
    file = open(filename,'r')
    if lines:
        output = [x for x in file.readlines()]
    else:
        output = file.read()
    
    # Close the file and return the result
    file.close()
    return output

# A simple main function to see if we did good
def main():

    # Setup variables for the program parameters
    nums = [0]*3
    num_at = 0
    strings = [""]*2
    first_num = False
    read_file = False
    read_lines = False
    verbose = False


    # Read the arguments
    for arg in sys.argv:
        if not first_num:
            verbose = verbose or (arg == '-t')
            read_file = read_file or (arg == '-f')
            read_lines = read_lines or (arg == '-l')
        
        if num_at < 3:
            try:
                number = int(arg)
                first_num = True
                nums[num_at] = number
                num_at += 1
            except:
                pass
        else:
            if num_at < 5:
                strings[num_at-3] = arg
                num_at += 1
        
    # Now, we have parsed the arguments
    # Time for some preprocessing
    g, m, d = (x for x in nums)

    # Check if you need to read files
    if read_file:
        strings = [file_string(x,read_lines) for x in strings]
        if read_lines and False:
            diff = abs(len(strings[0]) - len(strings[1]))
            if len(strings[0]) > len(strings[1]):
                strings[1].extend(['\n']*diff)
            elif diff != 0:
                strings[0].extend(['ff']*diff)

    print(type(strings[0]))

    # Create proper compare function
    myCompare = lambda x,y: compare(x,y,m,d)
    
    # Run to see some results
    ww,zz = hirschberg(strings[0],strings[1],myCompare,-g,verbose)

    if not read_lines:
        for i in range(len(ww)):
            print(ww[i]+"\n"+zz[i]+"\n")
    else:
        for i in range(len(ww)):
            for wl, zl in zip(ww[i],zz[i]):
                if wl == zl:
                    if wl[-1] == '\n':
                        wl = wl[:-1]
                        zl = zl[:-1]
                    print("=", wl,'\n=',zl)
                else:
                    if wl[-1] == '\n':
                        wl = wl[:-1]
                    if zl[-1] == '\n':
                        zl = zl[:-1]
                    print("<", wl,'\n>',zl)

if __name__ == "__main__":
    main()