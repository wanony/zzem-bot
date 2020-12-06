import mysql.connector as mysql
from mysql.connector import errorcode
import json

with open('directories.json') as direc:
    direc_dict = json.load(direc)
with open(direc_dict["apis"], 'r') as apis:
    apis_dict = json.load(apis)

command_prefix = apis_dict["command_prefix"]

user = apis_dict["database_user"]
password = apis_dict["database_password"]
database = apis_dict["database_name"]
host = apis_dict["database_host"]
port = apis_dict["database_port"]

cnx = None
try:
    cnx = mysql.connect(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port
    )
except mysql.Error as err:
    print("Database connection could not be established!")
    print(err)
    exit(1)


def AddCommand(name, link, added_by):
    cursor = cnx.cursor()
    sql = "INSERT INTO CustomCommands (CommandName, Command, AddedBy) VALUES (%s, %s, %s)"
    val = (name, link, added_by)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()


def GetCommands():
    cursor = cnx.cursor()
    sql = "SELECT CommandName, Command FROM CustomCommands"
    cursor.execute(sql)
    return dict(cursor.fetchall())


def RemoveCommand(name):
    cursor = cnx.cursor()
    sql = "DELETE FROM CustomCommands WHERE CommandName = %s"
    value = (name,)
    cursor.execute(sql, value)
    cnx.commit()
    row_count = cursor.rowcount
    cursor.close()
    return row_count > 0


with open(direc_dict["gfys"], 'r') as gfys:
    gfys_dict = json.load(gfys)
with open(direc_dict["levels"], 'r') as usrs:
    users = json.load(usrs)
with open(direc_dict["recents"], 'r') as rece:
    recent_dict = json.load(rece)
with open(direc_dict["contri"], 'r') as cont:
    contri_dict = json.load(cont)
with open(direc_dict["reddit"], 'r') as redd:
    reddit_dict = json.load(redd)
