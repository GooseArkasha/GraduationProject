from flask import Flask, jsonify, request

app = Flask(__name__)

client = app.test_client()

employees = [
    {
        'id': 0,
        'first_name': 'Adam',
        'last_name': 'Black'
    },
    {
        'id': 1,
        'first_name': 'Jim',
        'last_name': 'Frost'
    }
]

@app.route('/employees', methods=['GET'])
def get_list():
    return jsonify(employees)

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    item = next((x for x in employees if x['id'] == employee_id), None)
    if not item:
        return {'message': 'No Employees with this id'}, 400
    return item

@app.route('/employees', methods=['POST'])
def update_list():
    new_one = request.json
    employees.append(new_one)
    return jsonify(employees)


@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    item = next((x for x in employees if x['id'] == employee_id), None)
    params = request.json
    if not item:
        return {'message': 'No Employees with this id'}, 400
    item.update(params)
    return item

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    item = next((x for x in employees if x['id'] == employee_id), None)
    if not item:
        return {'message': 'No Employees with this id'}, 400
    employees.pop(item['id'])
    return '', 204


if __name__ == '__main__':
    app.run()
