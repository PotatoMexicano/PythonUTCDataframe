from multiprocessing import Pool as ThreadPool, cpu_count
import multiprocessing
import os
import datetime
import time
import pandas as pd

def drop_Files(dirFiles):
    for root,dirs,files in os.walk(dirFiles):
        for file in files:
            if file.endswith(".txt"):
                cod_file = int(str(file).removesuffix(".txt"))
                if cod_file%10 != 0:
                    os.remove(os.path.join(root,file))
def listFiles(pathFiles):
    f = open(pathFiles, "a")
    f.write(str(datetime.datetime.utcnow())+"\nPool:"+str(multiprocessing.current_process().name))
    file = str(pathFiles).split("\\")[7]
    data = []
    data.append([str(multiprocessing.current_process().name)[9:], file])
    return data
def createFiles(path, number):
    filesCreated = []
    for n in range(number):
        open(path+str(n+1)+".txt", "w")
        file = str(path)+str(n+1)+".txt"
        filesCreated.append(file)
    return filesCreated
def main():
    start = time.time()
    filesCreated = createFiles("C:\\Users\\gabri\\Documents\\Programação\\Python\\Testes\\", 10000)
    pool = ThreadPool(cpu_count())
    df = pd.DataFrame(columns=["worker"])
    rest = pool.map(listFiles, (filesCreated))
    drop_Files("C:\\Users\\gabri\\Documents\\Programação\\Python\\Testes\\")
    index = 0
    for n in rest:
        index+=1
        n = n[0]
        df.loc[index] = [n[0]]
    df = df.drop_duplicates()
    df.to_excel("log.xlsx", sheet_name="files_created", index=False)
    pool.close()
    pool.join()
    end =  time.time()
    print(end-start)
if __name__ == "__main__":
    main()