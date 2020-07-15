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
localidades_path="localidades/localidades2.csv"

geojson_diretory="C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros/Espalhamento/Mapeamento-Brasilia/Geojsons"

max_value=50
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
reds= plt.get_cmap('magma')
colors = reds(np.linspace(0,1,max_value+1))

with open("Geojsons/Brasilia.geojson") as f:
    pydata_brasilia = simplejson.load(f)
poly_brasilia = {"type": "Polygon", "coordinates": pydata_brasilia['features'][0]['geometry']['coordinates'][0]}
ax.add_patch(PolygonPatch(poly_brasilia,fc="lightblue", ec='#1f1d1d', alpha=0.5, zorder=2))


setPlotExtent_limitfile(ax, "Geojsons/Limites.geojson")
ax.invert_yaxis()



################

patch_regions_array=dict()

for localidade,num in zip(localidades['regiao'],range(len(localidades['regiao']))):
    for file in os.scandir("Geojsons"):
        if(file.name.endswith(".geojson") and (  int(file.name[0:2]) if str(file.name[0:2]).isnumeric() else 999    )==num):
            with open(file) as f:
                pydata = simplejson.load(f)
            poly = {"type": "Polygon", "coordinates": pydata['features'][0]['geometry']['coordinates'][0]}
            #patch_regions_array[localidade]= PolygonPatch(poly, fc=colors[0], ec='#1f1d1d', alpha=0.5, zorder=2) #use this line for reds
            patch_regions_array[localidade]= PolygonPatch(poly, fc=colors[max_value], ec='#1f1d1d', alpha=0.5, zorder=2) #use this line for magma
            ax.add_patch(patch_regions_array[localidade])
            
            

#for dataframe in lista_dataframes:
#    array=np.append(array,dataframe.loc[localidades['regiao'][4],'num']) 




index=-1
props = dict(boxstyle='round', facecolor='wheat', alpha=1)
ax.text(0.02, 0.97, str("Frame: ")+str(index)+str(" Data: ")+str(datas[0].strftime("%Y-%m-%d")), transform=ax.transAxes, fontsize=10,verticalalignment='top', bbox=props)


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
    ax.text(0.02, 0.97, str("Frame: ")+str(indice)+str(" Data: ")+str(data.strftime("%Y-%m-%d")), transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)
    print(str(indice)+" "+str(data.strftime("%Y-%m-%d")))
    for localidade,num in zip(localidades['regiao'],range(len(localidades['regiao']))): 
        if (localidade in patch_regions_array and localidade in lista_dataframes[indice]['regiao']):
            #print(num)
            valor=float(lista_dataframes[indice].at[localidade,'obitos'])
            #print(valor)
            #patch_regions_array[localidade].set_facecolor(colors[int(valor)]) #use this line for reds
            patch_regions_array[localidade].set_facecolor(colors[int((max_value-1)-int(valor))]) #use this line for magma
            if(valor>greatest):
                greatest=valor
    ax.text(0.52, 0.72, str("Desenv.: ")+str("Lucas Coelho de Almeida\nEmail: luccoelhoo@gmail.com"), transform=ax.transAxes, fontsize=6.5,verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.03))


    return ax

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(datas), interval=200)  #, blit=True)
plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/lucas/Desktop/UNB/Mestrado/Projetos/App-Covid-19/Outros\Espalhamento/Exemplo-Video/ffmpeg-20200528-c0f01ea-win64-static/ffmpeg-20200528-c0f01ea-win64-static/bin/ffmpeg'
Writer = animation.FFMpegWriter(fps=4, metadata=dict(name='Espalhamento da doença COVID-19 no Distrito Federal',artist='Lucas Coelho de Almeida',year='2020',description='Feito usando processamento avançados dos informes divulgados pela SES-DF. Email: luccoelhoo@gmail.com',url='luccoelhoo@gmail.com'), bitrate=1800)
anim.save('All-Regions-obitos.mp4', writer=Writer )
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

