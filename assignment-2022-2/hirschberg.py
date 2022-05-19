
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

    if i == 0 and j == 0:
        WW.append(W)
        ZZ.append(Z)
        return
    if i>0 and j>0:
        m = Compare(A[i-1],B[j-1])
        if F[i][j] == F[i-1][j-1]+m:
            enumerate_alignments(A[0:i-1],B[0:j-1],F,A[i-1]+W,B[j-1]+Z,Compare,g,WW,ZZ)
    if i > 0 and F[i][j] == F[i-1][j]-g:
        enumerate_alignments(A[0:i-1],B,F,A[i-1]+W,'-'+Z,Compare,g,WW,ZZ)
    if j > 0 and F[i][j] == F[i][j-1]-g:
        enumerate_alignments(A,B[0:j-1],F,'-'+W,B[j-1]+Z,Compare,g,WW,ZZ)


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
def hirschberg(A,B,Compare,g):


    # Define the outputs to be lists
    WW = []
    ZZ = []

    if len(A) == 0:
        WW = ['-'*len(B)]
        ZZ = [B]
    elif len(B) == 0:
        WW = [A]
        ZZ = ['-'*len(A)]
    elif len(A) == 1 or len(B) == 1:
        # Create the arrays for the enumeration
        WW,ZZ = [],[]

        # Create and calculate the F array
        F = Fconstructor(A,B,g)
        Fgenerator(A,B,F,Compare(1,1),-Compare(1,0),g,len(A),len(B))

        # Enumerate
        enumerate_alignments(A,B,F,"","",Compare,g,WW,ZZ)
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
            WWl, ZZl = hirschberg(A[0:i],B[0:j],Compare,g)
            WWr, ZZr = hirschberg(A[i:],B[j:],Compare,g)

            # We need to concatenate those two
            for l in range(len(WWl)):
                for k in range(len(WWr)):

                    # Create the new element
                    wwn = WWl[l]+WWr[k]
                    zzn = ZZl[l]+ZZr[k]
                    
                    # Append to the lists
                    WW.append(wwn)
                    ZZ.append(zzn)

    return (WW,ZZ)

# A sample compare function
def compare(a,b,match, differ):
    return match if a == b else differ

# A simple main function to see if we did good
def main():

    # Initialize the parameters
    m, d, g = 1,-1,-2
    A = "CTAAC"
    B = "ACTGACG"

    # Create proper compare function
    myCompare = lambda x,y: compare(x,y,m,d)
    # Run to see some results
    ww,zz = hirschberg(A,B,myCompare,-g)

    for i in range(len(ww)):
        print(ww[i]+"\n"+zz[i]+"\n")

if __name__ == "__main__":
    main()