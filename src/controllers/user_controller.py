from flask import jsonify
from flask_restx import Resource
from src.config.instance import instance
from src.models.user import User

app, api =  instance.app, instance.api

@api.route('/users',methods=['GET'], defaults={"page": 1, "per_page": 100})
@api.route('/users/<int:page>/<int:per_page>', methods=['GET'])
class UserList(Resource):
    def get(self, page, per_page):
        page = page
        per_page = per_page
        message = ""
        if per_page > 1000:
            per_page = 1000
            message = 'The maximum number of items per page is 1000'
            
        user_database = User.query.order_by(User.id).paginate(page=page, per_page = per_page)
        
        if len(user_database.items) > 0 :
            return generateResponseWithPagination(user_database, True, message)
        else:
            return generateResponseNotFound(True)      

@api.route('/user/country/<name>', defaults={"page": 1, "per_page": 100})
@api.route('/user/country/<name>/<int:page>/<int:per_page>', methods=['GET'])
class UserByCountry(Resource):
    def get(self, name, page, per_page):
        page = page
        per_page = per_page
        message = ""
        if per_page > 1000:
            per_page = 1000
            message = 'The maximum number of items per page is 1000'
            
        user_database = User.query.filter(User.country == name.upper()).paginate(page=page, per_page = per_page)

        if len(user_database.items) > 0 :
            return generateResponseWithPagination(user_database, True, message)
        else:
            return generateResponseNotFound(True)  
    
@api.route('/user/id/<int:id>')
@api.doc(params={'id': 'Id of User'})
class UserById(Resource):
    def get(self, id):
        user_database = User.query.filter(User.id == id)
        
        user_json = [user.to_json() for user in user_database]
        
        response = generateResponseWithoutPagination(user_json, True)
        
        return response
    
    
def generateResponseWithPagination(result, success, message=""):
    
    data=[]
    
    for user in result.items:
        data.append({
            'id': user.id,
            'name': user.name,
            'country': user.country
        })

        pagination = {
            'page': result.page,
            'total_pages': result.pages,
            'total_count': result.total,
            'prev_page': result.prev_num,
            'next_page': result.next_num,
            'has_next': result.has_next,
            'has_prev': result.has_prev,
            'total_items': len(data)
        }
        
    return jsonify({
            'results':data,
            'success': success,
            'pagination': pagination,
            'message': message
        })
    

def generateResponseWithoutPagination(result, success):
    return jsonify({
            'results':result,
            'success': success,
        })
    
def generateResponseNotFound(success):
    return jsonify({
            'results':[],
            'success': success,
            'message': 'Name not found'
        })
    
    