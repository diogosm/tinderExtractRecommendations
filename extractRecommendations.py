import argparse
import json
import os 
import requests

HEADER = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Auth-Token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'platform': 'web'
}
URL = "https://api.gotinder.com/v2/recs/core"

if __name__ == "__main__":
    get_profiles = requests.get(URL, headers=HEADER)

    if get_profiles.status_code == 200:
        print 'Dados coletados com sucesso\n'

        try:
            json_response = json.loads(get_profiles.text)
            #print json.dumps(json_response['data']['results'], indent=2, sort_keys=True)
            cont = 0

            for user in json_response['data']['results']:
                print 'Usuario = ', user['user']['name'], '\n'
                print '\tFoto_name = ', user['user']['_id'], '\n'

                user_id = user['user']['_id']
                if not os.path.exists(user_id):
                    os.mkdir(user_id, 0755)
                os.chdir(user_id)
                cont_fotos = 1
                for fotos in user['user']['photos']:
                    print 'Salvando foto ', cont_fotos
                    cont_fotos+=1
                    foto_id = fotos['id']

                    ans = requests.get(fotos['url'], stream = True)
                    
                    import shutil
                    ans.raw.decode_content = True
                    shutil.copyfileobj(ans.raw, open(foto_id + '.jpeg', 'wb'))

                os.chdir('../')
                cont += 1

            print 'Contador de user coletados = ', cont, '\n'
                
        except Exception as e:
            print e
            exit('Falhou')
