
# importing the required packages
import itertools
import csv
import os
import subprocess
from os import listdir
from os.path import isfile, join
import time

# Config settings:

#usually best set this on CLI directly before running this
###############################
###SET TO MAINNET BETA#####
# os.system("solana config set --url https://api.mainnet-beta.solana.com")
###SET TO DEVNET#####
# os.system("solana config set --url https://api.devnet.solana.com")

###############################
###test mint to be distributed
mintAddress = "7NTQ2ipuB2vVrFH2iLW37Bq4sp9iEwzjyWKh9WYxCN6A"


##########################
#name of the file from which wallets and amount needs to be read
fileName = "4-airdrop.csv"

# the file is expected to be in a folder named receivingWallets
with open('receivingWallets/' + fileName, 'r', encoding='UTF8') as f:

    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row[0])
        print(row[1])

        numOfTokens = float(row[1]);
        if (numOfTokens > 300):
            print("Not processing as num of tokens is greater than 300");
            wf = open("receivingWallets/"+ fileName + "-txn-log.txt", "a")
            wf.write("Not processing as num of tokens is greater than 300 \n")
            wf.close()
            continue

        line_count += 1
        #this assumes the default account has enough SOL and tokens to do the airdrop
        print(f'spl-token transfer --allow-unfunded-recipient --fund-recipient {mintAddress} {row[1]} {row[0]}')
        transferSOLRInstr = subprocess.run(["spl-token", "transfer", "--allow-unfunded-recipient", "--fund-recipient" , mintAddress, row[1], row[0]], stdout=subprocess.PIPE, stderr =subprocess.PIPE, text=True)
        # print("ROW no " + line_count + "\n")
        wf = open("receivingWallets/"+ fileName + "-txn-log.txt", "a")
        wf.write(transferSOLRInstr.stdout + transferSOLRInstr.stderr)
        wf.write('End ' + time.strftime('%l:%M %S %p %Z on %b %d, %Y') + "\n")

        print(transferSOLRInstr.stdout + transferSOLRInstr.stderr)        
        wf.close()
f.close();


#Move the file after successsful transfer to another folder to avoid accidentally sending again
os.rename("receivingWallets/" + fileName, "finished/" + fileName)