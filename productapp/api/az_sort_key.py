def az_sort_key(word):
    # Define Azerbaijani alphabet order
    az_alphabet = "a,b,c,ç,d,e,ə,f,g,ğ,h,x,ı,i,j,k,q,l,m,n,o,ö,p,r,s,ş,t,u,ü,v,y,z"
    az_order = {letter: idx for idx, letter in enumerate(az_alphabet.split(','))}
    
    # Return a tuple with the index of each character in the word for comparison
    return [az_order.get(c, len(az_alphabet)) for c in word.lower()]  # For case-insensitivity