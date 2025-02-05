from num2words import num2words
def corrected_num2words(num):
    word = num2words(num, lang="az").upper()
    result = []
    if "NÖQTƏ" in word:
        result = word.split(" NÖQTƏ ")
        r_num = str(num).split(".")[1]
        c_num = r_num + "0" if len(r_num) == 1 else r_num[:2]
        correct_word = result[0] + " MANAT " + num2words(int(c_num), lang="az").upper() + " QƏPIK"
    else:
        correct_word = word + " MANAT"
        
    return correct_word

"""
1. ƏLLİ İKİ
2. ƏLLİ İKİ NÖQTƏ SIFIR
3. ƏLLİ İKİ NÖQTƏ SIFIR BEŞ
4. ƏLLİ İKİ NÖQTƏ SIFIR ƏLLİ BEŞ
5. ƏLLİ İKİ NÖQTƏ BEŞ
6. ƏLLİ İKİ NÖQTƏ ƏLLİ BEŞ
7. ƏLLİ İKİ NÖQTƏ BEŞ YÜZ ƏLLİ BEŞ



"""
        

        


