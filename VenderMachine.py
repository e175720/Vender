import csv

class Vendermachine:

    money = 0
    menu_dic={}

    def Setup(self):
        #CSVファイルの読み込み(在庫情報,売り上げ,商品説明,etc...)

        with open('./Item.csv') as f:
            reader = csv.reader(f)
            ind = 1
            dic = True
            for row in reader:
                if dic == True:
                    self.menu_dic[0] = int(row[0])
                    dic = False
                    continue
                self.menu_dic[ind] = row
                self.menu_dic[ind][1] = int(self.menu_dic[ind][1])
                self.menu_dic[ind][3] = int(self.menu_dic[ind][3])
                self.menu_dic[ind][4] = int(self.menu_dic[ind][4])
                ind += 1

    def ViewMenu(self):
        print("###################")
        for i in range(1,len(self.menu_dic)):
            print("{0}.{1}:{2}円 在庫：{3}".format(i,self.menu_dic[i][0], self.menu_dic[i][1],self.menu_dic[i][3]))
        print("###################")


    def diff(self, price, inputmoney):
        return inputmoney - price


    def Enter(self,menu_number):
        #お金を投入した後の処理

        Inputmoney = int(input())
        select_dic = self.menu_dic[int(menu_number)]
        oturi = self.diff(select_dic[1], Inputmoney)

        while oturi < 0:
            #お釣りが足りないとき
            print("{0}円足りない".format(oturi * -1)) #絶対値
            Inputmoney += int(input("お金を追加してください："))
            oturi = self.diff(select_dic[1], Inputmoney) #おつりの更新

        print("投入した金額は" + str(Inputmoney) + "です。")
        print("{0} を購入しました。".format(select_dic[0]))

        #在庫と売り上げ個数の管理
        select_dic[3] -= 1
        select_dic[4] += 1

        if oturi == 0:
            self.money += int(Inputmoney)
        elif oturi > 0:
            print("お釣りがでます:{0}円".format(oturi))
            self.money += select_dic[1]

    def AdminMode(self):
        #管理者情報を表示

        total = 0

        print("------------------------------")
        for num in range(1,len(self.menu_dic)):
            total += self.menu_dic[num][4]*self.menu_dic[num][1]
            print("{0}の売り上げ金額:{1}".format(self.menu_dic[num][0] ,self.menu_dic[num][4]*self.menu_dic[num][1]))
        print("今日の売り上げ:{0}".format(total))
        print("------------------------------")


def save(menu_dic):
    with open("./Item.csv","w") as w:
        writer = csv.writer(w)
        writer.writerow(str(menu_dic[0]))
        for number in range(1,len(menu_dic)):
            writer.writerow(menu_dic[number])


def main():

    vm = Vendermachine()
    vm.Setup()

    while True:
        vm.ViewMenu()
        menu_number = input("何を買いますか？番号で入力してください:")

        if menu_number == "admin":
            #管理者情報を表示
            vm.AdminMode()
            continue

        #メニュー外を選択した時の処理
        try:
            menu_name = vm.menu_dic[int(menu_number)][0]
            menu_setumei = vm.menu_dic[int(menu_number)][2]
        except:
            print("正しい番号を入力してください")
            continue

        if vm.menu_dic[int(menu_number)][3] <= 0:
            print("在庫がありません")
            continue

        print("{0}を選択しました。".format(menu_name))
        print(menu_setumei)

        judge = input("この商品を買いますか?[y/n]:")

        if judge == "n":
            print("選択画面に戻ります。")
            continue
        elif judge != "y":
            print("正しく入力してください。選択画面に戻ります。")
            continue

        print("お金を入れてください。")

        vm.Enter(menu_number)
        save(vm.menu_dic)


if __name__ == '__main__':
    main()
