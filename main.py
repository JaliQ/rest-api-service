from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

def error_400():
    return {
  "code": 400,
  "message": "Validation Failed"
}

def compare_dates(date1, date2):
    dt1=datetime.strptime(date1, "%Y-%m-%dT%H:%M:%S%fZ")
    dt2=datetime.strptime(date2, "%Y-%m-%dT%H:%M:%S")
    if dt1>dt2:
        return True
    return False

def get_date(date):
    return datetime.fromisoformat(date.replace("Z", '+00:00'))

def update_parents_date(parent,date):
    db.session.execute(f'UPDATE item SET date="{date}" WHERE id="{parent.id}"')
    if parent.parentId != None:
        elder = Item.query.get(parent.parentId)
        update_parents_date(elder, date)

def find_all_children(id):    
    output = []
    size = 0
    children = list(db.session.execute(f'SELECT * FROM item WHERE parentId="{id}"'))
    if children == []:
        return output
    for item in children:
        item_obj = {"id": item[0],"url":item[1], "parentId" : item[2],"size" : item[3], "type" : item[4],
        "date" : datetime.isoformat(get_date(item[5])).replace("+00:00","Z"), "children": None}
        if item_obj["type"] == "FOLDER":
            item_obj["children"],item_obj["size"]= find_all_children(item_obj["id"])
        size+=item_obj["size"]
        output.append(item_obj)
    return output, size    

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.String(255), primary_key = True)
    url = db.Column(db.String(255) , nullable = True)
    parentId = db.Column(db.String(255), nullable = True) 
    size = db.Column(db.Integer , nullable = True)
    type = db.Column(db.String(255) , nullable = False)
    date = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return f"{self.id}  - {self.url} - {self.type}"

@app.route("/imports", methods = ["POST"])  #IMPORTING DATA AND UPDATING IT
def import_data():
    used = set() #Array for id's used in request
    for item in request.json["items"]:
        data = Item(id = item.get("id"),
            url = item.get("url"),
            parentId = item.get("parentId"),
            size =item.get("size"),
            type = item.get("type"),
            date = get_date(request.json["updateDate"]))
        if data.id in used:
            return error_400()
        used.add(data.id)
        if data.id == None:
            return error_400()
        if data.url != None and data.type == "FOLDER" :
            return error_400()
        if data.size != None and data.type == "FOLDER" :
            return error_400()
        if (data.size==None or data.size <=0) and data.type == "FILE":
            return error_400()
        if data.parentId != None:
            parent = Item.query.get(data.parentId)
            if parent.type == "FILE":
                return error_400()
            update_parents_date(parent,data.date)
        data_last =list( db.session.execute(f'SELECT * FROM item WHERE id="{data.id}"'))
        columns = ['id','url','parentId', 'size','type',"date"]
        if data_last == []:
            db.session.add(data)
            db.session.commit() 
        elif data_last != [()]:
            data_last = [x for x in data_last[0]]
            c = 0
            for k in columns:
                if data_last[c]!= vars(data)[k]:
                    if vars(data)[k] == None:
                        value = "NULL"
                    else:
                        value = f'"{vars(data)[k]}"'
                    db.session.execute(f'UPDATE item SET {k}={value}  WHERE id="{data.id}"')
                    db.session.commit()
                c+=1
    return {"Succesfully" : "Added"}

@app.route('/updates', methods = ["GET"]) 
def check_updated():
    date_end = request.args.get("date")
    date_end = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%SZ')
    date_start = date_end - timedelta(hours=24)
    date_end =  datetime.strftime(date_end, '%Y-%m-%d %H:%M:%SZ').replace("Z", "+00:00")
    date_start =  datetime.strftime(date_start, '%Y-%m-%d %H:%M:%SZ').replace("Z", "+00:00")
    files = db.session.execute(f'SELECT * FROM item WHERE date >= "{date_start}" AND date <= "{date_end}" AND type="FILE"')
    return {"items" : str(files)}

@app.route('/nodes/<id>')  #Getting Data and ALL CHILDREN ELEMENTS
def get_data(id):
    data = Item.query.get_or_404(id)
    output = []
    if data.type == "FILE":
        size = data.size
        output = None
    else:
        output,size = find_all_children(data.id)
    return {"id" : data.id, "url" : data.url,"parentId" : data.parentId, "size" : size ,
     "type" : data.type,
      "date" : datetime.isoformat(data.date)+"Z",
       "children" : sorted(output,key =  lambda x : x["id"])}  

@app.route("/delete/<id>",methods = ["DELETE"])      #Deleting data AND ALL CHILDRENS
def delete_data(id):
    ids,size = find_all_children(id)
    ids = [x.get("id") for x in ids]
    ids.append(id)
    for ident in ids:
        item = Item.query.get(ident)
        if item is None:
            return {
                    "code": 404,
                    "message": "Item not found"
                    }
        db.session.delete(item)
        db.session.commit()
    return {"Deleted" : ids}

if __name__ == "__main__":
    app.run(debug=True, port = 8080, host="localhost")