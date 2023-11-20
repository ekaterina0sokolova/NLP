import matplotlib.pyplot as plt

ranks = []
freq = []
# список для потсоянной Зипфа
c = []
k = []
lemm = []

with open("result_lemms.txt", "r+", encoding="utf-8") as lemm_file:
    for line in lemm_file:
        line = line.split()
        ranks.append(int(line[0]))
        lemm.append(line[1])
        freq.append(int(line[2]))
        k.append(int(line[2])//30755)
        c.append(int(line[0])*int(line[2])/30755)

print("Постоянная Зипфа")
for i in range(len(c)):
    print(str(lemm[i])+": "+str(c[i]))

plt.title('Закон Зипфа') # заголовок
plt.xlabel("Ранг") # ось абсцисс
plt.ylabel("Частота") # ось ординат
plt.plot(ranks, k)

plt.show()
