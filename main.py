from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
import os
import imageio
from glob import glob

def show_prompt()->int:
    """
    mostra um prompt para receber a um valor que será a regra utilizada

    Returns:
        int: retorna um valor entra 0 e 255
    """
    print('REGRAS ESTÃO ENTRE 0 e 255')
    regra = int(input("Entre com o valor da regra"))
    return regra

def decimal_to_binary(rule:int)->list:
    """
    Converter numeros decimal em binários

    Args:
        rule (int): valor entre 0 e 255

    Returns:
        list: o valor em binário
    """
    binary_number = []
    for _ in range(9):
        binary_number.append(int(rule%2))
        rule = int(rule)/2
    return binary_number

def cellular_automaton(rules:list, one_seed:bool,base_path:str):
    """
    Evolução no tempo e aplicação das regras 

    Args:
        rules (list): valor da regra a ser aplicada na base 2
        one_seed (bool): Ter uma ou varias sementes
        base_path (str): Caminho da pasta onde serão salvas as imagens
    """
    grid = [[0]*500]*500
    preview = [0]*500
    forward = [0]*500
    qtd_seed = 100
    for tempo in range(500):
        if tempo == 0:
            if one_seed:
                preview[int(len(forward)/2)] = 1
            else:
                index_seed = random.sample(list(range(len(preview))),qtd_seed)
                for seed in index_seed:                
                    preview[seed] = 1
        else:   
            preview[0] = forward[0]
            preview[-1] = forward[-1]         
            for pixel in range(0,500):  
                if pixel+1 >= len(preview):
                    pos = 0
                else:
                    pos = pixel + 1
                                                      
                if preview[pixel-1] == 0 and preview[pixel] == 0 and preview[pos] == 0:
                    forward[pixel] = (rules[0])#000
                elif preview[pixel-1] == 0 and preview[pixel] == 0 and preview[pos] == 1:
                    forward[pixel] = (rules[1])#001
                elif preview[pixel-1] == 0 and preview[pixel] == 1 and preview[pos] == 0:
                    forward[pixel] = (rules[2])#010
                elif preview[pixel-1] == 0 and preview[pixel] == 1 and preview[pos] == 1:
                    forward[pixel] = (rules[3])#011
                elif preview[pixel-1] == 1 and preview[pixel] == 0 and preview[pos] == 0:
                    forward[pixel] = (rules[4])#100
                elif preview[pixel-1] == 1 and preview[pixel] == 0 and preview[pos] == 1:
                    forward[pixel] = (rules[5])#101
                elif preview[pixel-1] == 1 and preview[pixel] == 1 and preview[pos] == 0:
                    forward[pixel] = (rules[6])#110
                elif preview[pixel-1] == 1 and preview[pixel] == 1 and preview[pos] == 1:
                    forward[pixel] = (rules[7])#111
            preview = deepcopy(forward)
        grid[tempo] = deepcopy(preview)
        figure = plt.figure()
        axes = figure.add_subplot()
        fig1 = plt.gcf()  
        axes.matshow(grid, cmap= ListedColormap(['w','b']))
        plt.yticks([])
        plt.xticks([])
        plt.draw()
        fig1.savefig(os.path.join(base_path,str(tempo)+".png"),dp1= 300)
        plt.close() 


def rename_image(base_path:str):
    """
    renomeia os arquivos com a extensão .png

    Args:
        base_path (str): nome da pasta onde estão as imagens
    """
    imagens = glob(os.path.join(base_path,"*.png"))
    for item in imagens:
        new_name = item.split('\\')[-1]    
        if len(new_name) == 5:
            new_name = '00' + new_name
            os.rename(item,os.path.join(base_path,new_name))
        elif len(new_name) == 6:
            new_name = '0' + new_name
            os.rename(item,os.path.join(base_path,new_name))


def create_gif(base_path:str,rule:int):
    """
    cria um gif com as imagens de uma pasta

    Args:
        base_path (str): nome da pasta onde estão as imagns
        rule (int): a regra utilizada
    """
    imagens = glob(os.path.join(base_path,"*.png"))
    file_name = 'celulas_automatos'
    ext_file = '.gif'    
    gif = []
    for item in imagens:
        gif.append(imageio.imread(item))
    imageio.mimsave(file_name+"_"+str(rule)+ext_file,gif,duration=.1)


def remove_png(base_path:str):
    """
    remove os arquivos da pasta com a extensão .png

    Args:
        base_path (str): nome da pasta
    """
    imagens = glob(os.path.join(base_path,"*.png"))
    for item in imagens: os.remove(item)    


rules = show_prompt()
binary_rules = decimal_to_binary(rules)
cellular_automaton(binary_rules, True,r'graficos')
rename_image(r'graficos')
create_gif(r'graficos',rules)
remove_png(r'graficos')
