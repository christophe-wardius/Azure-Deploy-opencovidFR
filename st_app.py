# modules
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm

st.set_page_config(page_title='OPEN COVID (FR)', layout='wide')

st.title('OPEN COVID (FR)')

"""
## Données nationales concernant l'épidémie de COVID19
### Sources

* Santé publique France
* Chiffres clés et cas par région
* Données GÉODES
* Agences Régionales de Santé
* Préfectures
* Ministère des Solidarités et de la Santé
* Vidéos / Vidéos en direct
* Points de situation (vidéos + PDF)
* Communiqués de presse

---
"""

# Load data
@st.cache(suppress_st_warning=True, allow_output_mutation=True, persist=True)
def load_data():
    # load data from github opencovidfr
    data = 'https://github.com/opencovid19-fr/data/raw/master/dist/chiffres-cles.csv'
    df0 = pd.read_csv(data, sep=",", low_memory=False)
    df0['date'] = df0['date'].str.replace('_','-')
    df0['date'] = pd.to_datetime(df0['date'], errors='coerce')
    
    # load data from data.gouv.fr
    df_dep0 = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675', sep=";", low_memory=False)
    df_tid0 = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/cbd6477e-bda6-485d-afdc-8e61b904d771', sep=";", low_memory=False)
    df_tid_dep0 = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/3c18e242-7d45-44f2-ac70-dee78a38ee1c', sep=";", low_memory=False)
    
    ## update gps coordinates
    # vars
    d_gps = {'France': [46.603354, 1.8883335], 'Charente': [45.6667902, 0.09730504409848517], 'Charente-Maritime': [45.73022675, -0.7212875872563794], 'Corrèze': [45.342904700000005, 1.8176424406120555], 'Creuse': [46.0593485, 2.04890101251091], 'Dordogne': [45.14291985, 0.6321258058651044], 'Gironde': [44.883745950000005, -0.6051264440438711], 'Landes': [44.00996945, -0.6433872354467377], 'Lot-et-Garonne': [44.3691703, 0.45391575832487524], 'Pyrénées-Atlantiques': [43.18718655, -0.728247400084667], 'Deux-Sèvres': [46.53914, -0.29947849341978416], 'Vienne': [46.612116549999996, 0.4654070096639711], 'Haute-Vienne': [45.91901925, 1.203176771876291], 'Île-de-France': [48.6443057, 2.7537863], 'Nouvelle-Aquitaine': [45.4039367, 0.3756199], 'Monde': [44.9863862, 4.5729027], 'Hérault': [43.591422, 3.3553309364095925], 'Haute-Savoie': [46.068820849999994, 6.344536991587102], 'Auvergne-Rhône-Alpes': [45.2968119, 4.6604809], 'Bourgogne-Franche-Comté': [47.0510946, 5.0740568], 'Aisne': [49.453285449999996, 3.606899003594057], 'Doubs': [47.06699155, 6.235622772820445], 'Nord': [50.52896715, 3.0883523694464854], 'Oise': [49.41205455, 2.406487846905477], 'Pas-de-Calais': [50.5144061, 2.258007849773996], 'Somme': [49.96897145, 2.373858954610659], 'Territoire de Belfort': [47.62923095, 6.899301156710882], 'Hauts-de-France': [50.1024606, 2.7247515], 'Grand Est': [48.4845157, 6.113035], "Côte-d'Or": [47.465503350000006, 4.74812234575117], 'Finistère': [48.24511525, -4.044090245241742], 'Loire-Atlantique': [47.34816145, -1.8727461214619257], 'Bas-Rhin': [48.5991783, 7.533818624332648], 'Alpes-Maritimes': [43.9210587, 7.1790785], 'Maine-et-Loire': [47.38863045, -0.3909097146387368], 'Mayenne': [48.1507819, -0.6491273812007092], 'Seine-Maritime': [49.66323745, 0.9401133910609153], 'Guadeloupe': [16.230510250000002, -61.68712602138846], 'Martinique': [14.6367927, -61.01582685063731], 'Guyane': [4.0039882, -52.999998], 'La Réunion': [-21.130737949999997, 55.536480112992315], 'Mayotte': [-12.8253862, 45.148626111147614], 'Centre-Val de Loire': [47.5490251, 1.7324062], 'Normandie': [49.0677708, 0.3138532], 'Pays de la Loire': [47.6594864, -0.8186143], 'Bretagne': [48.2640845, -2.9202408], 'Occitanie': [43.6487851, 2.3435684], "Provence-Alpes-Côte d'Azur": [44.0580563, 6.0638506], 'Corse': [42.188089649999995, 9.068413771427695], 'Ille-et-Vilaine': [48.17276805, -1.6498092420681134], 'Saint-Barthélemy': [17.9036287, -62.811568843006896], 'Saint-Martin': [48.5683066, 6.7539988], 'Morbihan': [47.825981150000004, -2.7633492695588253], 'Sarthe': [48.026928749999996, 0.2538217482247317], 'Ain': [49.453285449999996, 3.606899003594057], 'Ardennes': [49.69801175, 4.671600518245179], 'Aube': [48.3201921, 4.1905396615047525], 'Eure': [49.0756358, 0.9652025944774796], 'Marne': [48.961264, 4.31224359285714], 'Haute-Marne': [48.1329414, 5.252910789751933], 'Meurthe-et-Moselle': [48.95596825, 5.987038299756556], 'Meuse': [49.01296845, 5.428669076639772], 'Moselle': [49.0207259, 6.538035170357949], 'Haut-Rhin': [47.8654746, 7.231543347579764], 'Rhône': [45.8802348, 4.564533629559522], 'Vosges': [48.16378605, 6.382071173595532], 'Allier': [46.36746405, 3.163882848311948], 'Ardèche': [44.815194000000005, 4.3986524702343965], 'Cantal': [45.0497701, 2.699717567737356], 'Drôme': [44.72964575, 5.204559599996514], 'Gard': [43.95995, 4.297637002377168], 'Isère': [45.28979315, 5.634382477386232], 'Loire': [45.75385355, 4.045473682551104], 'Haute-Loire': [45.085724850000005, 3.833826117673291], 'Puy-de-Dôme': [45.7715343, 3.0839934206717934], 'Saône-et-Loire': [46.6557086, 4.55855481835173], 'Savoie': [45.494895150000005, 6.384660381375652], 'Aveyron': [44.315857449999996, 2.5065697302419823], 'Bouches-du-Rhône': [43.5424182, 5.034323560504859], "Côtes-d'Armor": [48.458422150000004, -2.7505868346107736], 'Eure-et-Loir': [48.4474102, 1.3998820185020766], 'Indre-et-Loire': [47.2232046, 0.6866702523286876], 'Haute-Saône': [47.63842335, 6.095114088932768], 'Vaucluse': [43.993864349999996, 5.1818898389002355], 'Hautes-Alpes': [44.6564666, 6.352024584507948], 'Calvados': [49.09076485, -0.24139505722798021], 'Cher': [47.024882399999996, 2.5753333606655704], 'Corse-du-Sud': [41.87340825, 9.0087052196875], 'Haute-Corse': [42.42196975, 9.100906549656115], 'Haute-Garonne': [43.305454600000004, 0.9716791701901577], 'Indre': [46.81210565, 1.5382051557056249], 'Loir-et-Cher': [47.65977515, 1.297183525390464], 'Loiret': [47.9140388, 2.3073794620675887], 'Manche': [49.091895199999996, -1.2454370607545526], 'Paris': [48.8566969, 2.3514616], 'Seine-et-Marne': [48.61902069999999, 3.0418157506708345], 'Yvelines': [48.76203735, 1.8871375621264361], 'Var': [43.4173592, 6.2664620128919], 'Essonne': [48.53034015, 2.239291805668168], 'Hauts-de-Seine': [48.840185899999994, 2.198641221906077], 'Seine-Saint-Denis': [48.9098125, 2.4528634784461856], 'Val-de-Marne': [48.774489349999996, 2.4543321444588204], "Val-d'Oise": [49.07507045, 2.209811443668384], 'Jura': [46.783362499999996, 5.783285726354901], 'Lot': [44.624991800000004, 1.6657742169753669], 'Tarn': [43.7921741, 2.133964772269535], 'Tarn-et-Garonne': [44.080656000000005, 1.2050632958700225], 'Vendée': [46.5040559, -0.7479592], 'Yonne': [47.85512575, 3.6450439257238765], 'Aude': [43.0542733, 2.512471457499548], 'Nièvre': [47.11969705, 3.5448897947227174], 'Orne': [48.57605325, 0.04466171759588161], 'Alpes-de-Haute-Provence': [44.1640832, 6.187851538609079], 'Gers': [43.695527600000005, 0.4101019175237992], 'Polynésie française': [-16.03442485, -146.0490931059517], 'Hautes-Pyrénées': [43.1437925, 0.15866611287926924], 'Pyrénées-Orientales': [42.625894, 2.5065089946931507], 'Lozère': [44.5425706, 3.521114648333333], 'Ariège': [42.9455368, 1.4065544156065486], 'Nouvelle-Calédonie': [-20.454288599999998, 164.55660583077983], 'Wallis et Futuna': [-13.289402, -176.204224]}
    DEPARTMENTS={'01':'Ain','02':'Aisne','03':'Allier','04':'Alpes-de-Haute-Provence','05':'Hautes-Alpes','06':'Alpes-Maritimes','07':'Ardèche','08':'Ardennes','09':'Ariège','10':'Aube','11':'Aude','12':'Aveyron','13':'Bouches-du-Rhône','14':'Calvados','15':'Cantal','16':'Charente','17':'Charente-Maritime','18':'Cher','19':'Corrèze','2A':'Corse-du-Sud','2B':'Haute-Corse','21':"Côte-d'Or",'22':"Côtes-d'Armor",'23':'Creuse','24':'Dordogne','25':'Doubs','26':'Drôme','27':'Eure','28':'Eure-et-Loir','29':'Finistère','30':'Gard','31':'Haute-Garonne','32':'Gers','33':'Gironde','34':'Hérault','35':'Ille-et-Vilaine','36':'Indre','37':'Indre-et-Loire','38':'Isère','39':'Jura','40':'Landes','41':'Loir-et-Cher','42':'Loire','43':'Haute-Loire','44':'Loire-Atlantique','45':'Loiret','46':'Lot','47':'Lot-et-Garonne','48':'Lozère','49':'Maine-et-Loire','50':'Manche','51':'Marne','52':'Haute-Marne','53':'Mayenne','54':'Meurthe-et-Moselle','55':'Meuse','56':'Morbihan','57':'Moselle','58':'Nièvre','59':'Nord','60':'Oise','61':'Orne','62':'Pas-de-Calais','63':'Puy-de-Dôme','64':'Pyrénées-Atlantiques','65':'Hautes-Pyrénées','66':'Pyrénées-Orientales','67':'Bas-Rhin','68':'Haut-Rhin','69':'Rhône','70':'Haute-Saône','71':'Saône-et-Loire','72':'Sarthe','73':'Savoie','74':'Haute-Savoie','75':'Paris','76':'Seine-Maritime','77':'Seine-et-Marne','78':'Yvelines','79':'Deux-Sèvres','80':'Somme','81':'Tarn','82':'Tarn-et-Garonne','83':'Var','84':'Vaucluse','85':'Vendée','86':'Vienne','87':'Haute-Vienne','88':'Vosges','89':'Yonne','90':'Territoire de Belfort','91':'Essonne','92':'Hauts-de-Seine','93':'Seine-Saint-Denis','94':'Val-de-Marne','95':"Val-d'Oise",'971':'Guadeloupe','972':'Martinique','973':'Guyane','974':'La Réunion','976':'Mayotte',}
    depts = {y:x for x,y in DEPARTMENTS.items()}
    # df0
    for area in df0['maille_nom'].unique():
        dfd = df0.copy()
        mask = (dfd['maille_nom'] == area)
        df0.loc[mask,'lat'] = d_gps[area][0]
        df0.loc[mask,'lon'] = d_gps[area][1]
    # df_dep0
    for x in depts.keys():
        dfd2 = df_dep0.copy()
        mask = (dfd2['dep'] == depts[x])
        df_dep0.loc[mask,'lat'] = d_gps[x][0]
        df_dep0.loc[mask,'lon'] = d_gps[x][1]
    # df_tid_dep0
    for x in depts.keys():
        dfd3 = df_tid_dep0.copy()
        mask = (dfd3['dep'] == depts[x])
        df_tid_dep0.loc[mask,'lat'] = d_gps[x][0]
        df_tid_dep0.loc[mask,'lon'] = d_gps[x][1]
    
    # df_depts0
    df_depts0 = df0[df0['granularite']=='departement']
    df_depts0.loc[:,'nouvelles_hospitalisations'] = df_depts0.loc[:,'nouvelles_hospitalisations'].fillna(0)
    
    return df0, df_dep0, df_tid0, df_tid_dep0, df_depts0, depts

df, df_dep, df_tid, df_tid_dep, df_depts, depts = load_data()

### STREAMLIT ###
#################

# sidebar

area = st.sidebar.selectbox('Choisissez la zone à étudier',sorted([x for x in depts.keys()], key=lambda x: x))

if st.sidebar.checkbox('Indicateurs'):
    """
    ## Données nationales (Indicateurs)
    """
    
    df_france = df[df['maille_nom'] == 'France']
    
    #Indicators (National)
    
    fig0_1 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_france.tail(1)['nouvelles_hospitalisations'].values[0]),
        title = {'text': "Nouvelles hospitalisations ("+str(df_france.tail(1)['date'].values[0])[:10]+")"},
        delta = {'reference': int(df_france.tail(2)['nouvelles_hospitalisations'].values[0])},
        ))
    
    fig0_2 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_france.tail(1)['nouvelles_reanimations'].values[0]),
        title = {'text': "Nouvelles réanimations ("+str(df_france.tail(1)['date'].values[0])[:10]+")"},
        delta = {'reference': int(df_france.tail(2)['nouvelles_reanimations'].values[0])},
        ))
    
    fig0_3 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_dep.groupby('jour')['P'].sum().reset_index().tail(1)['P'].values[0]),
        title = {'text': "Nouveaux cas positifs ("+str(df_dep.groupby('jour')['P'].sum().reset_index().tail(1)['jour'].values[0])+")"},
        delta = {'reference': int(df_dep.groupby('jour')['P'].sum().reset_index().tail(2)['P'].values[0])},
        ))
    
    # dataframe sur le taux d'incidence
    df_tid['tx_id'] = df_tid['P']*100000/df_tid['pop']
    
    fig0_4 = go.Figure(go.Indicator(
        value = df_tid.tail(1)['tx_id'].values[0],
        mode = "gauge+number+delta",
        title = {'text': "Taux d'incidence"},
        delta = {'reference': df_tid.tail(2)['tx_id'].values[0]},
        gauge = {'axis': {'range': [None, 160]},
                 'steps' : [
                     {'range': [0, 10], 'color': "lightgray"},
                     {'range': [10, 50], 'color': "gray"},
                     {'range': [50, 100], 'color': "orange"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 50}}))
    
    st.plotly_chart(fig0_1)
    st.plotly_chart(fig0_2)
    st.plotly_chart(fig0_3)
    st.plotly_chart(fig0_4)
    
    """
    ## Données sur la 'zone' sélectionnée
    """
    
    # st_display
    'Vous avez choisi: ', area
    
    df_area = df[df['maille_nom'] == area]
    df_tid_dep['tx_id'] = df_tid_dep['P']*100000/df_tid_dep['pop']
    
    # indicateurs (zone sélectionnée)
    ind1_1 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = int(df_tid_dep[df_tid_dep['dep'] == depts[area]].tail(1)['tx_id'].values[0]),
        title = {'text': "Taux d'incidence ("+area+")"},
        delta = {'reference': int(df_tid_dep[df_tid_dep['dep'] == depts[area]].tail(2)['tx_id'].values[0])},
        gauge = {'axis': {'range': [None, 160]},
                 'steps' : [
                     {'range': [0, 10], 'color': "lightgray"},
                     {'range': [10, 50], 'color': "gray"},
                     {'range': [50, 100], 'color': "orange"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 50}}))
    
    ind1_2 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_area.tail(1)['deces'].values[0]),
        title = {'text': "Nombre de décès (cumulé)"},
        delta = {'reference': int(df_area.tail(2)['deces'].values[0])},
        ))
    
    ind1_3 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_area.tail(1)['nouvelles_hospitalisations'].values[0]),
        title = {'text': "Nouvelles hospitalisations"},
        delta = {'reference': int(df_area.tail(2)['nouvelles_hospitalisations'].values[0])},
        ))
    
    ind1_4 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_area.tail(1)['nouvelles_reanimations'].values[0]),
        title = {'text': "Nouvelles réanimations"},
        delta = {'reference': int(df_area.tail(2)['nouvelles_reanimations'].values[0])},
        ))
    
    df_dep_area = df_dep[df_dep['dep'] == depts[area]]
    df_tested = df_dep_area.groupby(['jour','cl_age90'])['T'].sum().reset_index()
    
    ind1_5 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_tested.tail(1)['T'].values[0]),
        title = {'text': "Nombre de personnes testées ("+str(df_tested.tail(1)['jour'].values[0])+")"},
        delta = {'reference': int(df_tested.tail(2)['T'].values[0])},
        ))
    
    df_pos = df_dep_area.groupby(['jour','cl_age90'])['P'].sum().reset_index()
    
    ind1_6 = go.Figure(go.Indicator(
        mode = "number+delta",
        value = int(df_pos.tail(1)['P'].values[0]),
        title = {'text': "Nombre de cas positifs ("+str(df_pos.tail(1)['jour'].values[0])+")"},
        delta = {'reference': int(df_pos.tail(2)['P'].values[0])},
        ))
    
    st.plotly_chart(ind1_1)
    st.plotly_chart(ind1_2)
    st.plotly_chart(ind1_3)
    st.plotly_chart(ind1_4)
    st.plotly_chart(ind1_5)
    st.plotly_chart(ind1_6)

if st.sidebar.checkbox('Tendances'):
    """
    ## Tendances
    """
    """
    ### France
    #### Évolution des cas testés et positifs (P)
    """
    f0 = px.bar(df_dep.groupby('jour')['P'].sum().reset_index(), x='jour', y='P')
    st.plotly_chart(f0)
    
    """
    ### France
    #### Évolution des personnes testées (T)
    """
    f0_1 = px.bar(df_dep.groupby('jour')['T'].sum().reset_index(), x='jour', y='T')
    st.plotly_chart(f0_1)
    
    """
    ### Par zone :
    #### Les 10 derniers jours (Nouvelles hospitalisations, Nouvelles réanimations) 
    """
    area
    
    # création du df_area
    df_area = df[df['maille_nom'] == area]
    
    # fig 1 : hosp/reas last10 days
    # plotly chart 1
    df_last10 = df_area.tail(10)
    df1 = df_last10.melt(id_vars='date', value_vars=['nouvelles_hospitalisations', 'nouvelles_reanimations'])
    fig1 = px.line(df1, x='date' , y='value' , color='variable')
    st.plotly_chart(fig1)
    
    """
    #### Décès, Hospitalisés 
    ##### par zone:
    """
    area
    
    # fig2 : ['deces','hospitalises']
    # plotly chart 2
    df2 = df_area.melt(id_vars='date', value_vars=['deces','hospitalises'])
    fig2 = px.line(df2, x='date' , y='value' , color='variable')
    st.plotly_chart(fig2)
    
    """
    #### Réanimations
    ##### par zone:
    """
    area
    
    # fig3 : ['reanimation']
    # plotly chart 3
    df3 = df_area
    fig3 = px.line(df3, x='date', y='reanimation')
    st.plotly_chart(fig3)
    
    """
    ### Données sur le Système d’Informations de DEPistage (SI-DEP)
    
    Le Système d’Informations de DEPistage (SI-DEP)
    Le nouveau système d’information de dépistage (SI-DEP), en déploiement depuis le 13 mai 2020, est une plateforme sécurisée où sont systématiquement enregistrés les résultats des laboratoires des tests réalisés par l’ensemble des laboratoires de ville et établissements hospitaliers concernant le SARS-COV2.
    
    La création de ce système d'information est autorisée pour une durée de 6 mois à compter de la fin de l'état d'urgence sanitaire par application du décret n° 2020-551 du 12 mai 2020 relatif aux systèmes d’information mentionnés à l’article 11 de la loi n° 2020-546 du 11 mai 2020 prorogeant l’état d’urgence sanitaire et complétant ses dispositions.
    
    #### Description des données
    Le présent jeu de données renseigne à l'échelle départementale et régionale :
    
    * le nombre de personnes testées (`T`) et le nombre de personnes déclarées positives (`P`) par classe d'âge (`cl_age90`) ;
    * le nombre de personnes positives sur 7 jours glissants (`pop`).
    
    ##### Taux d'incidence
    Le taux d'incidence correspond au nombre de cas positifs au Covid-19 pour 100 000 habitants. La formule utilisée pour calculer ce fameux taux est la suivante : nombre de personnes positives multiplié par 100 000, le tout divisé par le nombre d'habitants de la zone étudiée.
    Lorsque le taux d'incidence dépasse 10 cas positifs pour 100 000 habitants sur sept jours, le département atteint un premier «seuil de vigilance». Au-delà de 50 cas positifs en une semaine, on atteint le «seuil d'alerte».
    
    """
    
    df_dep_area = df_dep[df_dep['dep'] == depts[area]]
    st.write(df_dep_area.head())
    
    """
    #### Évolution du nombre de personnes testées
    """
    st.write(area)
    
    df_tested = df_dep_area.groupby(['jour','cl_age90'])['T'].sum().reset_index()
    'Nombre de personnes testées le ', str(df_tested.tail(1)['jour'].values[0]), ' : ', df_tested.tail(1)['T'].values[0]
    
    # plotly fig 5
    fig5 = px.bar(data_frame=df_tested, x='jour', y='T', color='cl_age90')
    st.plotly_chart(fig5)
         
    """
    #### Évolution du nombre de cas positifs
    """
    st.write(area)
    
    df_pos = df_dep_area.groupby(['jour','cl_age90'])['P'].sum().reset_index()
    'Nombre de cas positifs le ', str(df_pos.tail(1)['jour'].values[0]), ' : ', df_pos.tail(1)['P'].values[0]
    
    # plotly fig 6
    fig6 = px.bar(data_frame=df_pos, x='jour', y='P', color='cl_age90')
    st.plotly_chart(fig6)

## Prédictions ##

if st.sidebar.checkbox('Prédictions (30 jours)'):
    """
    ## Prédictions sur 30 jours
    """
    """
    ### France : Cas positifs à 30 jours
    """
    
    p = df_dep.groupby('jour')['P'].sum().reset_index()
    p['jour'] = pd.to_datetime(p['jour'])
    p = p.set_index('jour')
    p = p.dropna() # cleaning
    
    p_log = np.log(p) # Transformée logarithmique
    p_log = p_log.dropna() # cleaning
    
    # création du modèle SARIMAX
    model = sm.tsa.SARIMAX(p_log.squeeze(),order=(4,0,2),seasonal_order=(4,0,2,7),
                           enforce_stationarity=False, enforce_invertibility=False,
                           trend='n') 
    
    sarima = model.fit() # entraînement du modèle

    pred = np.exp(sarima.predict(433, 463)) # Prédiction et passage à l'exponentielle
    p_pred = pd.concat([p, pred]) # Concaténation des prédictions
    p_pred = p_pred.rename(columns={"P": "Cas Positifs", 0: "Prédictions"})
    
    fig_p = px.line(p_pred)
    st.plotly_chart(fig_p)
    
    """
    ### Département sélectionné : Cas positifs à 30 jours
    """
    st.write(area)

    p2 = df_dep[df_dep['dep'] == depts[area]].groupby('jour')['P'].sum().reset_index()
    p2['P'] = p2['P']*100
    p2['jour'] = pd.to_datetime(p2['jour'])
    p2 = p2.set_index('jour')
    p2['P'] = p2['P'].replace(0,1)
    p2 = p2.dropna()

    p2_log = np.log(p2) # Transformée logarithmique
    p2_log = p2_log.dropna() # cleaning to avoid NaN / infs error
    
    # création du modèle SARIMAX
    model2 = sm.tsa.SARIMAX(p2_log.squeeze(),order=(1,0,2),seasonal_order=(1,0,1,7))
    
    sarima2 = model2.fit()
    
    pred2 = np.exp(sarima2.predict(433, 463)) # Prédiction et passage à l'exponentielle
    p2_pred = pd.concat([p2, pred2]) # Concaténation des prédictions
    p2_pred = p2_pred.rename(columns={"P": "Cas Positifs", 0: "Prédictions"})
    
    fig_p2 = px.line(p2_pred)
    st.plotly_chart(fig_p2)
    
## cartes intéractives ##
    
if st.sidebar.checkbox('Cartes intéractives'):
    """
    ## Cartes interactives
    """
    
    """
    #### France : Taux d'incidence
    """
    # calcul de taux d'incidence par département
    df_tid_dep['tx_id'] = df_tid_dep['P']*100000/df_tid_dep['pop']
    # dernière semaine glissante
    last_week = df_tid_dep['semaine_glissante'].values[-1]
    
    
    fig1_2= px.scatter_mapbox(df_tid_dep[df_tid_dep['semaine_glissante'] == last_week], lat="lat", lon="lon", 
    						size="tx_id", hover_name="tx_id", color="tx_id",
    						zoom=4, center={'lat':48.862725,'lon':2.287592}, 
    						height=800,
    						mapbox_style="open-street-map")
    
    st.plotly_chart(fig1_2)

    """
    ### Période à étudier :
    """
    
    col1, col2 = st.beta_columns(2)
    date1 = col1.date_input('Date de début', value=pd.to_datetime(df_dep.groupby('jour')['P'].sum().reset_index().tail(1)['jour'].values[0]))
    date2 = col2.date_input('Date de fin', value=pd.to_datetime(df_dep.groupby('jour')['P'].sum().reset_index().tail(1)['jour'].values[0]))
    
    """
    #### France : Évolution des 'Nouvelles hospitalisations'
    ##### (animation)
    """
    
    df_anim = df_depts
    df_anim['dt_str'] = df_anim['date'].apply(lambda x: x.strftime("%d-%b-%Y"))
    df_anim = df_anim[(df_anim['date'] >= pd.to_datetime(date1)) & (df_anim['date'] <= pd.to_datetime(date2))]
    
    try:
    	fig1_0= px.scatter_mapbox(df_anim, lat="lat", lon="lon", 
    						size="nouvelles_hospitalisations", hover_name="maille_nom",
    						animation_frame="dt_str", 
    						zoom=4, center={'lat':48.862725,'lon':2.287592}, 
    						height=800,
    						mapbox_style="open-street-map")
    
    	st.plotly_chart(fig1_0)
    except KeyError:
    	st.write('Dates incorrectes')
        
    """
    #### France : Évolution des cas positifs
    ##### (animation)
    """
    
    df_anim2 = df_dep.groupby(['jour','dep','lat','lon'])['P'].sum().reset_index()
    df_anim2 = df_anim2[(pd.to_datetime(df_anim2['jour']) >= pd.to_datetime(date1)) & (pd.to_datetime(df_anim2['jour']) <= pd.to_datetime(date2))]
    
    try:
    	fig1_1= px.scatter_mapbox(df_anim2, lat="lat", lon="lon", 
    						size="P", hover_name="dep",
    						animation_frame="jour",
    						zoom=4, center={'lat':48.862725,'lon':2.287592}, 
    						height=800,
    						mapbox_style="open-street-map")
    
    	st.plotly_chart(fig1_1)
    except KeyError:
    	st.write('Dates incorrectes')