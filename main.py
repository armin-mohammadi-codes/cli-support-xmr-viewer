# pyinstaller --onefile main.py
# pip freeze > packages.txt

import os
import json
import time
import cursor
import requests

class app:
    def __init__(self):
        self.__data_base__ = {
            'wallet': '',
            'github': 'https://github.com/armin-mohammadi-codes'
        }
        self.__api_url__ = "https://supportxmr.com/api/"
        self.__startup__()

    def __startup__(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as infile:
                self.__data_base__ = json.load(infile)
        else:
            setup_wallet = True
            while setup_wallet:
                os.system("color a")
                os.system("title github : https://github.com/armin-mohammadi-codes")
                os.system("cls")
                wallet = input("Enter your XMR wallet address : ")
                if wallet is not None:
                    self.__data_base__["wallet"] = wallet
                    if self.xmr_account() is not None and self.xmr_user()["msg"]["payout_threshold"] != 0:
                        self.__merge_database__()
                        setup_wallet = False
                    else:
                        os.remove("data.json")
                        print("Your wallet is not exist, please enter the valid XMR wallet !")
                        time.sleep(1)
                else:
                    os.remove("data.json")
                    print("Please enter the valid XMR wallet !")
                    time.sleep(1)

    def __merge_database__(self):
        with open("data.json", "w") as outfile:
            json.dump(self.__data_base__, outfile)

    def xmr_account(self):
        url = self.__api_url__ + "miner/" + self.__data_base__["wallet"] + "/stats"
        result = requests.get(url)
        if result.status_code == 200:
            self.__data_base__["account"] = result.json()
            self.__merge_database__()
            return self.__data_base__["account"]
        else:
            return None

    def xmr_user(self):
        url = self.__api_url__ + "user/" + self.__data_base__["wallet"]
        result = requests.get(url)
        if result.status_code == 200:
            self.__data_base__["user"] = result.json()
            self.__merge_database__()
            return self.__data_base__["user"]
        else:
            return None

    def xmr_worker(self):
        url = self.__api_url__ + "miner/" + self.__data_base__["wallet"] + "/identifiers"
        result = requests.get(url)
        if result.status_code == 200:
            self.__data_base__["worker"] = result.json()
            self.__merge_database__()
            return self.__data_base__["worker"]
        else:
            return None

    def xmr_wallet(self):
        return self.__data_base__["wallet"]



if __name__ == "__main__":
    my_app = app()
    while True:
        cursor.hide()
        os.system("title Support XMR Viewer")
        os.system("color A")
        os.system("cls")
        data  = my_app.xmr_account()
        print()
        print("Wallet address : " + my_app.xmr_wallet())
        print()
        print("Minimum for instant pay : " + str((my_app.xmr_user()["msg"]["payout_threshold"])/1000000000000) + " XMR ")
        print()
        print("XMR Pending : " + str(round(data["amtDue"]/1000000000000, 8)))
        print("XMR Paid : " + str(round(data["amtPaid"]/1000000000000, 8)))
        print()
        print(f"Valid Shares : {str(data["validShares"])}")
        print(f"Invalid Shares : {str(data["invalidShares"])}")
        print()
        print("Worker : {")
        m_id = 0
        for worker in my_app.xmr_worker():
            print("\t" + f"ID : {m_id} - NAME : {worker}")
            m_id += 1
        print("}")
        print()
        print(f"Total hashrate : {",".join([str(data["totalHashes"])[i:i+3] for i in range(0, len(str(data["totalHashes"])), 3)])}")
        time.sleep(60)