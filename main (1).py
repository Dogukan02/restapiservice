
from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data' : data}, 200

    def post(self):
        name = request.args['isim']
        age = request.args['yaş']
        city = request.args['şehir']

        data = pd.read_csv('users.csv')

        new_data = pd.DataFrame({
            'isim'      : [name],
            'yaş'       : [age],
            'şehir'      : [city]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('users.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 200

    def delete(self):
        name = request.args['isim']
        data = pd.read_csv('users.csv')
        data = data[data['isim'] != name]

        data.to_csv('users.csv', index=False)
        return {'message' : 'Kayıt başarıyla silindi'}, 200

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv',usecols=[2])
        data = data.to_dict('records')
        
        return {'data' : data}, 200

class Name(Resource):
    def get(self,name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['isim'] == name :
                return {'veri' : entry}, 200
        return {'Mesaj' : 'Aradığınız isimde giriş yok !'}, 404


# Add URL endpoints
api.add_resource(Users, '/kullanıcı')
api.add_resource(Cities, '/şehir')
api.add_resource(Name, '/<string:name>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    app.run()