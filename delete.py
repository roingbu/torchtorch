# -*- coding: utf-8 -*-
"""
Created on 2022年1月6日23:26:00

@author: MambaCloud
"""

import os
import shutil


def file_copy(path,targe_path,num):  #将path目录下所有jpg文件复制到targe_path
    '''
    root 所指的是当前正在遍历的这个文件夹的本身的地址
    dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
    files 同样是 list , 内容是该文件夹中所有的文件名(不包括子目录)
    '''
    n=0
    if not os.path.exists(targe_path):  # 如果目的路径不存在该文件就创建空文件,并保持目录层级结构
        os.makedirs(targe_path)
    for root,dirs,files in os.walk(path):  # 列出源目录文件和文件夹
        for name in files:
            if name.endswith('.jpg'):#若文件名结尾是以jpg结尾，则复制到新文件夹
                list=(os.path.join(root,name)) #list是jpg文件的全路径
                # shutil.copy(list, targe_path) #将jpg文件复制到新文件夹
                os.remove(list)
                n+=1
                if n==num:
                    break
                
        

path="/home/bu/mmgeneration-master/work_dirs/try copy"
# targe_path="/home/bu/anfangDataset/trans/train/"
num = 353395
file_copy(path, targe_path,num)