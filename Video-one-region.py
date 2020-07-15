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

csv_directory="C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Webscrapping-SESDF/PROGRAMA-backup-dados-extraidos-covid"
localidades_path="C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Webscrapping-SESDF/PROGRAMA-localidades/localidades.csv"

geojson_diretory="C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros/Espalhamento/Mapeamento-Brasilia/Geojsons"

max_value=500
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
for f in os.scandir(csv_directory):
    if f.name.endswith(".csv"):
        list_files_csv.append(str(f.name))
        #print(str(f.name))
#print(list_files_csv)
# Iterate over all csv files in the folder and process each one in turn
for input_file in list_files_csv:
    aux=input_file
    aux=aux.replace(".csv","").split("_")[1].split("-")
    datas.append(datetime.datetime(int(aux[0]), int(aux[1]), int(aux[2])))


#for data in datas:
#    print(data)



localidades=pd.read_csv(localidades_path)
#print(localidades['regiao'][4])
for i in range(len(localidades['regiao'])):
    localidades.at[i,'regiao']=strip_accents(localidades.at[i,'regiao']).lower()




cont=0
lista_dataframes =[]
for f in os.scandir(csv_directory):
    cont+=1
    if(f.name.endswith(".csv")):
        df=pd.DataFrame(pd.read_csv(f))
        for i in range(len(df['regiao'])):
            df.at[i,'regiao']=strip_accents(df.at[i,'regiao']).lower()
        df2=df.set_index('regiao', drop = False)
        lista_dataframes.append(df2)
#print(cont)




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
#quantidade de dias para olhar (len(datas))
################################################################################


# simple array 
array =[]
cont=0
#array=np.append(array,lista_dataframes[39].loc[localidades['regiao'][4],'num'])
for dataframe in lista_dataframes:
    #print(list_files_csv[cont])
    cont+=1
    #print(dataframe)
    array=np.append(array,dataframe.loc[localidades['regiao'][4],'num']) 
  
ser = pd.Series(array)
#ser.plot()
#plt.show()

#print(ser)


fig = plt.figure(1,figsize=(10, 4), dpi=180)
ax = plt.gca()
ax.set_aspect(1)
reds= plt.get_cmap('magma')
colors = reds(np.linspace(0,1,max_value))



with open("C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros/Espalhamento/Mapeamento-Brasilia/Geojsons"+"/Taguatinga.geojson") as f:
    pydata = simplejson.load(f)
#print(pydata)

#print(pydata['features'][0]['geometry']['coordinates'])


poly = {"type": "Polygon", "coordinates": pydata['features'][0]['geometry']['coordinates'][0]}
setPlotExtent_limitfile(ax, "C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros/Espalhamento/Mapeamento-Brasilia/Geojsons"+"/Limites.geojson")

index=0
props = dict(boxstyle='round', facecolor='wheat', alpha=1)
ax.text(0.05, 0.95, str("Frame: ")+str(index)+str(" Data: ")+str(datas[0].strftime("%Y-%m-%d"))+str(" Casos: ")+str(array[0]), transform=ax.transAxes, fontsize=10,verticalalignment='top', bbox=props)
patch= PolygonPatch(poly, fc=colors[0], ec='#1f1d1d', alpha=0.5, zorder=2)
ax.add_patch(patch)


date_iter=iter(datas)
value_iter=iter(array)
index_iter=iter(range(len(datas)))
#print(len(datas))
#print(len(array))

def init():
    # initialize an empty list of cirlces
    return []

def animate(i):
    global index
    valor=next(value_iter)
    data=next(date_iter)
    indice=next(index_iter)
    #patches = []
    ax.text(0.05, 0.95, str("Frame: ")+str(indice)+str(" Data: ")+str(data.strftime("%Y-%m-%d"))+str(" Casos: ")+str(valor), transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)
    patch.set_facecolor(colors[int(max_value-valor)])
    return ax

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(datas)-1, interval=200)  #, blit=True)
plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros\Espalhamento/Exemplo-Video/ffmpeg-20200528-c0f01ea-win64-static/ffmpeg-20200528-c0f01ea-win64-static/bin/ffmpeg'
Writer = animation.FFMpegWriter(fps=5, metadata=dict(artist='Me'), bitrate=1800)
anim.save('Taguatinga.mp4', writer=Writer )




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

