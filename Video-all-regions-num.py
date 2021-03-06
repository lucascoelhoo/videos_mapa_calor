from descartes import PolygonPatch
import simplejson
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation
import datetime
import glob
import os
import pandas as pd
import simplejson
# import numpy as np 
import numpy as np 
import unicodedata
from scipy.interpolate import interp1d
import csv
from pathlib import Path

input_path = str(Path.cwd()).replace("\\","/")+"/"
#csv_directory="/home/simop/webscrapping-sesdf/Webscrapping-SESDF/PROGRAMA-backup-dados-extraidos-covid"
csv_directory="C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Webscrapping-SESDF/PROGRAMA-backup-dados-extraidos-covid"
localidades_path=input_path+"localidades/localidades.csv"

geojson_diretory=input_path+"Geojsons"

titulo="Evolução da COVID-19 no DF (Número de Casos)"

max_value=0
interpol = interp1d([0,max_value],[0,1])

#Funcao que limpa strings retirando e/ou substituindo caracteres especiais###########################
#####################################################################################################
def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)
#####################################################################################################





def configurePlot():
    # set up the mapplotlib
    fig = pyplot.figure(figsize=(10, 4), dpi=180)
    ax = fig.add_subplot(1,2,1)
    return fig, ax


def setPlotExtent(ax, data):
    # get feature extents (a property of the cloudmade geojson)
    # note this was previously bbox
    minx = data['bounds'][0][0]
    maxx = data['bounds'][1][0]
    miny = data['bounds'][0][1]
    maxy = data['bounds'][1][1]

    # set the graph axes to the feature extents
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)



def setPlotExtent_limitfile(ax, path):
    with open(path) as f:
        jsondata = simplejson.load(f)
    minx = jsondata['features'][0]['geometry']['coordinates'][0][0][0][0]
    maxx = jsondata['features'][0]['geometry']['coordinates'][0][0][2][0]
    miny = jsondata['features'][0]['geometry']['coordinates'][0][0][0][1]
    maxy = jsondata['features'][0]['geometry']['coordinates'][0][0][2][1]

    # set the graph axes to the feature extents
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

def plotFeature(coordinates, myplot):
    poly = {"type": "Polygon", "coordinates": coordinates}
    patch = PolygonPatch(poly, fc='#cc6672', ec='#1f1d1d', alpha=0.5, zorder=2)
    # plot it on the graph
    myplot.add_patch(patch)




datas=[]
list_files_csv=[]
lista_sort_aux=os.listdir(csv_directory)
for fname,index_aux_sort in zip(lista_sort_aux,range(len(lista_sort_aux))):
    if not fname.endswith(".csv"):
        lista_sort_aux.pop(index_aux_sort)
lista_sort_aux.sort(key=lambda lista_sort_aux:int(lista_sort_aux.replace(".csv","")))
for f in lista_sort_aux:
    if f.endswith(".csv"):
        with open(csv_directory+"/"+(f),"r", encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row,index in zip(csv_reader,range(2)):
                if(index==1): #aqui garantimos pegar a primeira data do arquivo
                    #print(row[1])
                    list_files_csv.append(row[1])
                    break
#print(list_files_csv)        
# Iterate over all csv files in the folder and process each one in turn
for input_data in list_files_csv:
    aux=input_data
    datas.append(datetime.datetime(int(aux.split("-")[0]), int(aux.split("-")[1]), int(aux.split("-")[2])))
datas=sorted(datas)
#for data in datas:
#    print(data)
#quit()


localidades=pd.read_csv(localidades_path)
#print(localidades['regiao'][4])
for i in range(len(localidades['regiao'])):
    localidades.at[i,'regiao']=strip_accents(localidades.at[i,'regiao']).lower()



cont_frames=0
lista_dataframes =[]
#print(*sorted(os.listdir(csv_directory),key=len), sep = "\n")
for f in lista_sort_aux:
    if(f.endswith(".csv")):
        cont_frames+=1
        df=pd.DataFrame(pd.read_csv(csv_directory+"/"+(f)))
        for i in range(len(df['regiao'])):
            df.at[i,'regiao']=strip_accents(df.at[i,'regiao']).lower()
        df2=df.set_index('regiao', drop = False)
        lista_dataframes.append(df2)
#print(cont_frames)





#print(lista_dataframes[29]['regiao'])
#print(lista_dataframes[39].loc['Taguatinga',:])

#print(lista_dataframes[39].loc[localidades['regiao'][4],:])

#Descomente abaixo para ver como tudo esta estruturado corretamente, cheque os arquivos no diretorio
#print(list_files_csv[39])
#print(datas[39])
#print(lista_dataframes[39].loc[localidades['regiao'][4],'num'])

################################################################################
#Ate aqui ja temos: lista de datas (datas), lista de localidades (localidades)
#e lista de dataframes com os dados de cada relatorio (lista_dataframes) e
#quantidade de dias para olhar (len(datas)), e por fim, tambem temos o valor
#que servira de referencia        
################################################################################


# simple array 
#array =[]
#for dataframe in lista_dataframes:
#    array=np.append(array,dataframe.loc[localidades['regiao'][4],'num'])  
#ser = pd.Series(array)
#ser.plot()
#plt.show()
#print(ser)

fig = plt.figure(1,figsize=(10, 4), dpi=180)
ax = plt.gca()
ax.set_aspect(1)
#reds= plt.get_cmap('Reds')
reds= plt.get_cmap('magma').reversed()
colors = reds(np.linspace(0,1,10000)) #valor apenas para inicializar a variavel, depois eh alterado para max_value

with open("Geojsons/Brasilia.geojson") as f:
    pydata_brasilia = simplejson.load(f)
poly_brasilia = {"type": "Polygon", "coordinates": pydata_brasilia['features'][0]['geometry']['coordinates'][0]}
ax.add_patch(PolygonPatch(poly_brasilia,fc="lightblue", ec='#1f1d1d', alpha=0.5, zorder=2))


setPlotExtent_limitfile(ax, "Geojsons/Limites.geojson")
ax.invert_yaxis()
ax.axis('off')



################

patch_regions_array=dict()

for localidade,num in zip(localidades['regiao'],range(len(localidades['regiao']))):
    for file in os.scandir("Geojsons"):
        if(file.name.endswith(".geojson") and (  int(file.name[0:2]) if str(file.name[0:2]).isnumeric() else 999    )==num):
            with open(file) as f:
                pydata = simplejson.load(f)
            poly = {"type": "Polygon", "coordinates": pydata['features'][0]['geometry']['coordinates'][0]}
            #patch_regions_array[localidade]= PolygonPatch(poly, fc=colors[0], ec='#1f1d1d', alpha=0.5, zorder=2) #use this line for reds
            patch_regions_array[localidade]= PolygonPatch(poly, fc=colors[1], ec='#1f1d1d', alpha=0.5, zorder=2) #use this line for magma
            ax.add_patch(patch_regions_array[localidade])
            
max_value=0
for indice_aux in range(len(datas)):
    for localidade,num in zip(localidades['regiao'],range(len(localidades['regiao']))): 
        if (localidade in patch_regions_array and localidade in lista_dataframes[indice_aux]['regiao']):
            valor=int(lista_dataframes[indice_aux].at[localidade,'num'])
            if(valor>max_value):
                max_value=valor
print(max_value)     

#for dataframe in lista_dataframes:
#    array=np.append(array,dataframe.loc[localidades['regiao'][4],'num']) 



colors = reds(np.linspace(0,1,max_value+1)) #valor apenas para inicializar a variavel, depois eh alterado para max_value

index=-1
props = dict(boxstyle='round', facecolor='wheat', alpha=1)
ax.text(0, 1.02, titulo+str("    ")+str(" Data: ")+str(datas[0].strftime("%d/%m/%Y")), transform=ax.transAxes, fontsize=10,verticalalignment='top', bbox=props)

# Add a colorbar
color_map_aux = plt.cm.get_cmap('magma')
color_map_aux=color_map_aux.reversed()
sm = plt.cm.ScalarMappable(cmap=color_map_aux, norm=plt.Normalize(vmin=0, vmax=max_value))
sm.set_array([])
fig.colorbar(sm,ax=ax)

date_iter=iter(datas)
index_iter=iter(range(len(datas)))

#print(lista_dataframes[0].loc[strip_accents('Aguas Claras').lower(),:])
#print(localidades['regiao'][1]==lista_dataframes[0]['regiao'][1])
#print(localidades['regiao'][1])
#print(lista_dataframes[0]['regiao'][1])
#print(lista_dataframes[0].at[localidades['regiao'][1],'num'])
#print(lista_dataframes[0].iloc[[1],[4]])
greatest=0

def init():
    # initialize an empty list of cirlces
    return []

def animate(i):
    global date_iter
    global index_iter
    global greatest
    data=next(date_iter)
    indice=next(index_iter)
    ax.text(0, 1.02, titulo+str("    ")+str(" Data: ")+str(data.strftime("%d/%m/%Y")), transform=ax.transAxes, fontsize=10,verticalalignment='top', bbox=props)
    print(str(indice)+" "+str(data.strftime("%Y-%m-%d")))
    for localidade,num in zip(localidades['regiao'],range(len(localidades['regiao']))): 
        if (localidade in patch_regions_array and localidade in lista_dataframes[indice]['regiao']):
            #print(num)
            valor=int(lista_dataframes[indice].at[localidade,'num'])
            if(localidade=='ceilandia'):
                print(valor)
            #print(valor)
            #patch_regions_array[localidade].set_facecolor(colors[int(valor)]) #use this line for reds
            patch_regions_array[localidade].set_facecolor(colors[int(valor)]) #use this line for magma
            if(valor>greatest):
                greatest=valor
    print("")
    ax.text(0.01, 0.05, str("Contato: lucas.almeida@redes.unb.br\nENE/UNB - DF"), transform=ax.transAxes, fontsize=4,verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.03))
    
    return ax

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(datas), interval=200)  #, blit=True)
#plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros\Espalhamento/Exemplo-Video/ffmpeg-20200528-c0f01ea-win64-static/ffmpeg-20200528-c0f01ea-win64-static/bin/ffmpeg'
Writer = animation.FFMpegWriter(fps=5, metadata=dict(name='Espalhamento da doença COVID-19 no Distrito Federal (Número de Casos)',artist='Lucas Coelho de Almeida',year='2020'
                                                     ,description='Feito usando processamento avançados dos informes divulgados pela SES-DF. Email: luccoelhoo@gmail.com',
                                                     url='luccoelhoo@gmail.com'), bitrate=1800)
anim.save('regioes-df-casos.mp4', writer=Writer )
print(greatest)



'''
fig = plt.figure(1,figsize=(10, 4), dpi=180)
ax = plt.gca()
ax.set_aspect(1)
magma= plt.get_cmap('Magma')
colors = iter(magma(np.linspace(0,1,65)))


fig = plt.figure(1,figsize=(10, 4), dpi=180)
#plt.axis([0,nx,0,ny])
ax = plt.gca()
ax.set_aspect(1)

reds= plt.get_cmap('Reds')
colors = iter(reds(np.linspace(0,1,65)))
with open(r"file2.geojson") as f:
    pydata = simplejson.load(f)
#print(pydata)
poly = {"type": "Polygon", "coordinates": pydata['coordinates']}
setPlotExtent(ax, pydata)
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=1)
#textstr = '\n'.join(( r'$\mu=%.2f$' % (mu, ),r'$\mathrm{median}=%.2f$' % (median, ), r'$\sigma=%.2f$' % (sigma, )))
textstr=""
count=0
ax.text(0.05, 0.95, str(count), transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)
patch= PolygonPatch(poly, fc=next(colors), ec='#1f1d1d', alpha=0.5, zorder=2)
#patches.append(patch)
ax.add_patch(patch)

def init():
    # initialize an empty list of cirlces
    return []

def animate(i):
    global count
    count+=1
    #patches = []
    ax.text(0.05, 0.95, str(count), transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)
    patch.set_facecolor(next(colors))
    return ax

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=60, interval=1)  #, blit=True)

#anim.save('im_geojson', metadata={'artist':'Lucas'})
plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros\Espalhamento/Exemplo-Video/ffmpeg-20200528-c0f01ea-win64-static/ffmpeg-20200528-c0f01ea-win64-static/bin/ffmpeg'
Writer = animation.FFMpegWriter(fps=30, metadata=dict(artist='Me'), bitrate=1800)
anim.save('im_geojson-tentativa.mp4', writer=Writer )

#with open("myvideo.html", "w") as f:
#    print(anim.to_html5_video(), file=f)
'''

