import streamlit as st
import os
import pathlib
from os import listdir
from os.path import isfile, join,basename
import classifyer as c
import utils_treat_data as ut
import os
import numpy as np
import matplotlib.pyplot as plt
st.write("""
# Demo
""")
parent_path = pathlib.Path(__file__).parent.parent.resolve()
data_path = os.path.join(parent_path, "audios")
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
option = st.sidebar.selectbox('Pick a dataset', onlyfiles)
file_location=os.path.join(data_path, option)
# use `file_location` as a parameter to the main script

audio_name = os.path.basename(file_location)

model_name = 'model1500 epochs - 90 batch_size - 0.002 learning_rate - 0.9 beta_1 - 0.999 beta_2 - 0.01 decay(train3).h5'
pasta = 'audios/'
pasta_salvar_audios = 'cutted_audio/'
src = pasta + audio_name + '.mp3'
dest = pasta + audio_name + '.wav'

## parameters 
threshold = 0.7
max_consec = 50

###########
try:
    ut.adjust_audio_mp3(src,dest)
except:
    print('not an mp3 file')

audio = c.get_audio(audio_name, audio_folder = pasta, add_wav = False)

c.multiple_split(audio =audio,
                  qtde_split = 6,
                  filename_save=audio_name,
                  save_folder = pasta_salvar_audios)

lista_audios = c.get_audio_split(audio_name = audio_name, folder = pasta_salvar_audios )


st.caption(audio_name)

model = c.get_model(model_name)
for i in lista_audios:
    st.markdown("- **" + i + "**")
    predictions = c.get_prediction(model = model,filename = i, print=False)
    ll= predictions[0,:,0]
    #ax1, ax2 = fig.subplots(2, 1, sharey=True,sharex=True)
    fig = plt.figure(figsize=[6.4, 1.5]) 
    ax1 = fig.subplots(1)
    ax1.plot(ll)
    ax1.set_ylim([0, 1.05])
    ax1.set_ylabel('probability')
    #plt.ylabel('Probability')
    st.pyplot(fig)
    nn = c.number_of_consecutives(predictions = predictions, threshold = threshold)
    N_consecutivess = '-'.join(str(x) for x in nn)
    st.markdown("Especificação de quantidade de pontos consecutivos acima do limiar de " + str(threshold) + " : " + N_consecutivess)

lista_audios = c.get_audio_split(audio_name = audio_name, folder = pasta_salvar_audios )
consecutives  = c.get_all_predictions_consecutives(model = model, list_of_audios = lista_audios,threshold = threshold, print = False)
consecutivess = ''.join(str(x) for x in consecutives)
res = c.second_classifier(consecutives, limit = max_consec)
if res == 1:
    classificacao = "<span style='color:red'> contém ruido industrial </span>"
else:
    classificacao = "<span style='color:green'> não contém ruido industrial </span>"



st.markdown("### Considerando um limiar de " + 
            str(threshold * 100) + 
            """% e o maior número de steps consecutivos acima do limiar de """ +
            str(max_consec) +
            " steps o audio selecionado " + 
            classificacao, 
            unsafe_allow_html=True)