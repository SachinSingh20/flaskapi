import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_address = _json['address']
		_hobby = _json['hobby']
		if _name and _email and _phone and _address and request.method == 'POST':
			sqlQuery = "INSERT INTO rest_emp(name, email, phone, address) VALUES(%s, %s, %s, %s, %s)"
			bindData = (_name, _email, _phone, _address)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('Employee added successfully!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@app.route('/user')
def user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id, name, address, hobby FROM userinfo")
		userRows = cursor.fetchall()
		respone = jsonify(userRows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(
			"SELECT id, name, address, hobby FROM userinfo WHERE id =%s", id)
		userRow = cursor.fetchone()
		respone = jsonify(userRow)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update', method=['PUT'])
def update_user():
	try:
		_json =  request.json
		_id = _json['id']
		_name = _json['name']
		_address = _json['address']
		_hobby = _json['hobby']
		if _id and _name and _address and _hobby and request.method == 'PUT':
			sqlQuery = "UPDATE userinfo SET id=%s, name=%s, address=%s, hobby=%s WHERE id=%s"
			bindData = (_id, _name,_address, _hobby)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('user data updates successfully')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	finally:
			cursor.close() 
		    conn.close()
	
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM userinfo WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('user data deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
		
if __name__ == "__main__":
    app.run()