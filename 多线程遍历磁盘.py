import string,os,threading,shutil,time
from threading import Thread

dest_file_path_1=[]
diver_list=[]
for p in string.ascii_uppercase:    #生成A-Z的字母
    diver=p + ":\\"                 #形成磁盘'A:\\' - 'Z:\\'
    if os.path.isdir(diver):        #判断磁盘是否存在
        diver_list.append(diver)    #如果磁盘存在就添加到diver_list列表中
print(diver_list)                   #打印列表
sem=threading.Semaphore(len(diver_list))#限制当前最大连接量，如果连接人数过大就等待
def thread_fun(n):
    '''函数功能：找出相对应后缀的文件'''
    global dest_file_path_1         #设置全局变量
    sem.acquire()
   # for m in diver_list:
       # for root, dirs,files in os.walk(m):
    for root, dirs, files in os.walk(n):
        for f in files:
            if f[-4:].lower()=='.jpg':
                dest_file_path=os.path.join(root,f)
                dest_file_path_1.append(dest_file_path)
    sem.release()

def copy_file():
    '''函数功能：对文件进行复制'''
    if dest_file_path_1!=None:
        s=0
        for i in dest_file_path_1:
            ms=i.split("\\")
            mn=r"C:\Users\Administrator\Desktop\copy\\"+ms[-1]
            shutil.copyfile(i,mn)
            s += 1
        print('copy完成')

#threading.Thread(target=thread_fun).start()
#通过两个线程同时遍历两个磁盘找出图片文件路径添加到dest_file_path_1列表中
for i in diver_list:
    threading.Thread(target=thread_fun,args=(i,)).start()
time.sleep(5)#休眠时间用来复制图片
threading.Thread(target=copy_file).start()#复制图片线程
