from num2words import num2words
def corrected_num2words(num):
    word = num2words(num, lang="az").upper()
    if "NÖQTƏ" in word:
        parts = word.split(" NÖQTƏ ")
        r_num = str(num).split(".")[1]
        c_num = r_num + "0" if len(r_num) == 1 else r_num[:2]
        return parts[0] + " MANAT " + num2words(int(c_num), lang="az").upper() + " QƏPIK"
    return word + " MANAT"
