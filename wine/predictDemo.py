# predict based on given example
import pickle
import utility
import tkinter as tk

# read model
dataName = "I:/HCI_KTH/big data/project/codes/wine_study/wine/NBmodel_freq_expensive.pkl"
with open(dataName, 'rb') as load_data:
    model = pickle.load(load_data)

# read model
dataName = "I:/HCI_KTH/big data/project/codes/wine_study/wine/freq_dict.pkl"
with open(dataName, 'rb') as load_data:
    dictWords = pickle.load(load_data)

# # show dict
# sortedDict=sorted(dictWords.vocabulary_.items(), key=lambda item: item[1], reverse=True)
# sortedDict[2500-200:2500]

# UI
window = tk.Tk()
window.title('Wine Market Forecaster')
window.geometry('500x200')

# wine description
e = tk.Entry(window)
e.pack()

#predict result
result = tk.StringVar()
result.set("no result")


#predict button

def predictMarket():
    inputString = e.get()
    # process input
    cleanedCom = utility.cleanText([inputString])  # clean special symbols etc
    X = dictWords.transform(cleanedCom).toarray()
    #show result
    # predict
    if model.predict(X)[0] == 1:
        result.set("market probably like it")
    else:
        result.set("market may not like it!")
    tk.Label(window, text=str(result.get())).place(x = 170,y = 80)

b1 = tk.Button(
    window,
    text="Predict",
    width=15,
    height=1,
    command=predictMarket)
b1.pack()

window.mainloop()

#inputString='Deep ruby nose of raspberry and plum, slight oak silky smooth tannins with long finish hint of chocolate can likely cellar for 5+ years '
#inputString='Way too much spices and artificial earthy wood notes giving a weirdly bitter aftertaste, together with the high alcohol and low tannin profile just not balanced.'
#inputString='Slightly smooth and fruity with flavor of raspberry and plum.'
#inputString='Not smooth and not fruity without flavor of raspberry and plum.'



