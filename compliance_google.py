import pandas as pd
import numpy as np
import math

import json
from pandas.io.json import json_normalize

from inspect import getmembers, isfunction

import common_utils as utils
import cosmosdb_utils as cosmosdb

'''
Metodo de verificacion de cumplimiento con google
'''
def due_diligence(req_data):
    # Cosmos: get setup search metadata for google
    first_last_name = req_data['apellidoPaterno']
    second_last_name = req_data['apellidoMaterno']
    full_names = req_data['nombres']
    identity = req_data['id']

    comosdb_context = cosmosdb.CosmosDBContext(
        cosmosdb.Setting.COSMOS_END_POINT,
        cosmosdb.Setting.COSMOS_KEY)

    setup = comosdb_context.get_cosmosdb_container(
        cosmosdb.Setting.COSMOS_DATABASE,
        cosmosdb.Setting.COSMOS_CONTAINER_SETUP,
        cosmosdb.Setting.COSMOS_CONTAINER_SETUP_PARTITION_KEY)
   
    query = "SELECT * FROM c WHERE c.id='google-query'"
    items = list(setup.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    request_charge = setup.client_connection.last_response_headers['x-ms-request-charge']
    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
    #Compliance Google API: prepare query for google (wish, veto y otros)
    
    query_list = items[0].get(utils.KeyTerm.Q_BASE)
    persona= full_names + " " + first_last_name
    full_name_fist_last_name= full_names + " " + first_last_name
    full_last_names = first_last_name + " " + second_last_name
    full_names_cuotes = "(" + req_data['nombres'] + ")"
    q_google = persona
    json_data = {
        "id" : identity,
        "apellido_paterno" : first_last_name,
        "apellido_materno" : second_last_name,
        "nombres" : full_names,
        "total_vetos" : 0,
        "total_wish" : 0,
        "total_otros" : 0
    }
    total_vetos = 0
    total_wish = 0
    total_otros = 0
    list_details = list()
    list_details_stored = list()
    for query_item in query_list:
        category    = query_item.get(utils.KeyTerm.Q_BASE_CTG)
        level    = query_item.get(utils.KeyTerm.Q_BASE_LVL)
        termino = query_item.get(utils.KeyTerm.Q_BASE_TRM)
        if level == "url_empresas":
            q_google = '"' + persona + '"' + ' ' + termino
        elif level in (['linkedin','url_lkd']):
            q_google = '("' + full_name_fist_last_name + '" | ("' + full_last_names + '" + ' + full_names_cuotes + ')) ' + termino
        else:
            q_google = '"' + persona + '"' + ' ' + termino
        res = utils.google_search(
            q_google,
            utils.Setting.API_KEY,
            utils.Setting.CSE_ID,
            utils.Setting.NUM_RESULTS_DEFAULT
            )
        total_results = int(res.get('searchInformation').get('totalResults'))
        if category == utils.KeyTerm.Q_BASE_CTG_WISH and total_results>0:
            total_wish = total_wish + 1
        if category == utils.KeyTerm.Q_BASE_CTG_VETO and total_results>0:
            total_vetos = total_vetos + 1
        if category == utils.KeyTerm.Q_BASE_CTG_OTROS and total_results>0:
            total_otros = total_otros + 1
        json_detail = {
            "category": category,
            "level": level,
            "query": q_google,
            "total_resuls": total_results
        }
        json_detail_stored = json_detail.copy()
        if total_results>0:
            json_detail_stored["results"] = res.get('items')
        list_details.append( json_detail )
        list_details_stored.append(json_detail_stored)

    #Compliance Google API-->>Cosmos:query information stored 
    json_data["total_wish"] = total_wish
    json_data["total_vetos"] = total_vetos
    json_data["total_otros"] = total_otros
    if total_vetos>0:
        json_data["status"] = 'OBSERVADO'
    else:
        json_data["status"] = 'APROBADO'

    json_data_stored = json_data.copy()
    json_data_stored["details"] = list_details_stored

    evaluation = comosdb_context.get_cosmosdb_container(
        cosmosdb.Setting.COSMOS_DATABASE,
        cosmosdb.Setting.COSMOS_CONTAINER_TRACK,
        cosmosdb.Setting.COSMOS_CONTAINER_TRACK_PARTITION_KEY)
    query = "SELECT * FROM c WHERE c.id='"+ identity +"'"
    items = list(evaluation.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    if len(items)==0:
        response = evaluation.create_item(body=json_data_stored)
        print('Upserted Item\'s Id is {0}'.format(response['id']))
    json_data["details"] = list_details
    json_msg = json.dumps(json_data)
    #Notificar si tiene noticias negativas
    return json_msg