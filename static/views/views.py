import hashlib
import sys
from flask import url_for, abort

# Recursive quick sort function
def sort_tuple(items, column_num):
    def parition(array, low, high):
        i = (low - 1)
        pivot = array[high][column_num]
        for j in range(low, high):
            if array[j][column_num] <= pivot:
                i = i+1
                array[i], array[j] = array[j], array[i]
        array[i+1], array[high] = array[high], array[i+1]
        return (i+1)


    def quicksort(array, low, high):
        if len(array) == 1:
            return array
        if low < high:
            pi = parition(array, low, high)

            quicksort(array, low, pi-1)
            quicksort(array, pi+1, high)

    array_items = list(items)
    quicksort(array_items, 0, len(array_items)-1)
    return tuple(array_items)

#Recursive binary search
def binary_search(array, low, high, search_item, column_num):
    try:
        # Check base case
        if high >= low:
            mid = (high + low) // 2
            # if item is in mid location
            if str(array[mid][column_num]) == search_item:
                return mid
            elif str(array[mid][column_num]) > search_item:
                return binary_search(array, low, mid - 1, search_item, column_num)
            else:
                return binary_search(array, mid+1, high, search_item, column_num)     
    except Exception as e:
        print(e)
    return -1


def select_record(mysql, query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def execute_command(mysql, query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()

def get_unfinished_cases(cases):
        unfinished = 0
        for case in cases:
            if case[2] is not "Resolved":
                unfinished += 1
        return unfinished

def search_array(self, array, search_item, column):
    return

# Class to generate a SHA3 hash of an input value
class SHA3Hash(object):
    def get_hash(self, value):
        value = str(value)
        hash = hashlib.new("sha3_512", value.encode())
        return hash.hexdigest()


# Functions for login webpage
class Login(object):
    # Validate any login attemtp by getting all user accounts that match the idenfification code entered
    def validate_login(self, identification, password, mysql):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password, type FROM admin_accounts WHERE username = %s", [identification])                      
        data = cursor.fetchall()  
        cursor.execute("SELECT username, password, court_id, type FROM courts WHERE username = %s", [identification])
        data = data + cursor.fetchall()
        cursor.execute("SELECT bar_council_num, password, type FROM barristers WHERE bar_council_num = %s", [identification]) 
        data = data + cursor.fetchall()
        cursor.execute("SELECT solicitor_reference_id, password, type FROM solicitors WHERE solicitor_reference_id = %s", [identification])
        data = data + cursor.fetchall()
        cursor.close()     
        sha = SHA3Hash()
        if len(data) >= 1: 
            if str(data[0][0]) == identification and data[0][1] == sha.get_hash(password):            
                if data[0][-1] == "ADM":
                    return url_for('admin')
                elif data[0][-1] == "BAR":
                    return url_for('barrister', id=data[0][0])
                elif data[0][-1] == "SOL":
                    return url_for('solicitor', id=data[0][0])
                elif data[0][-1] == "CRT":
                    return url_for('court', id=data[0][2])
        return url_for('index')             
           

    def register_barrister(self, form, cursor, mysql):    
        password = SHA3Hash().get_hash(form['password-main'])
        cursor.execute("INSERT INTO barristers (bar_council_num, password, chainbers_address_id, type) VALUES ({0}, '{1}', {2}, '{3}')".format(form['identification'], password, 0, "BAR"))
        mysql.connection.commit()
        return 
    

    def register_solicitor(self, form, cursor, mysql):
        password = SHA3Hash().get_hash(form['password-main'])
        cursor.execute("INSERT INTO solicitors (solicitor_reference_id, password, address_of_practise_id, type) VALUES ({0}, '{1}', {2}, '{3}')".format(form['identification'], password, 0, "SOL"))
        mysql.connection.commit()
        return
    

    def register_court(self, form, cursor, mysql):
        password = SHA3Hash().get_hash(form['password-main'])
        cursor.execute("INSERT INTO courts (username, password, address_id, type) VALUES ({0}, '{1}', {2}, '{3}')".format(form['identification'], password, 0, "CRT"))
        mysql.connection.commit()
        return


    # Handles POST requests and execute relevent functions based on the form request
    def handle_form_requests(self, mysql, form):
        def get_data():         
            if user_type == "Court":
                cursor.execute("SELECT username FROM courts WHERE username = %s", [id])
                return cursor.fetchall()
            elif user_type == "Barrister":
                cursor.execute("SELECT bar_council_num FROM barristers WHERE bar_council_num = %s", [id]) 
                return cursor.fetchall()
            elif user_type == "Solicitor":
                cursor.execute("SELECT solicitor_reference_id FROM solicitors WHERE solicitor_reference_id = %s", [id])
                return cursor.fetchall() 
            else:
                abort(500)

        if form['submit'] == 'login':               
            return self.validate_login(form['identification'], form['password']  , mysql)
        elif form['submit'] == 'register':                    
            user_type = form['combobox']       
            cursor = mysql.connection.cursor()   
            data = get_data()   
            if len(data) == 0:
                if user_type == "Barrister":
                    self.register_barrister(form, cursor, mysql)
                elif user_type == "Solicitor":
                    self.register_solicitor(form, cursor, mysql)
                elif user_type == "Court":
                    self.register_court(form, cursor, mysql)  
            else:                    
                return '//'      
            cursor.close()        
        return ''


# Functions for admin's webpage
class Admin(object):
    # List of all court options for a drop down box on the admin dashbaord
    court_options = ('County','Civil','Family','Circuit','High','Registry','Appeal','Tribunal')

    # Search all addresses linearly to find a full address present in teh tuple
    def search_addresses(self, addresses, full_address):
        for address in addresses:
            address_full = "{0}, {1}, {2}, {3}, {4}, {5}".format(
                address[1],
                address[2],
                address[3],
                address[4],
                address[5],
                address[6]
            )
            if full_address in address_full:
                return address     
        return ()

    # Search all clients linearly to find a client using a client's full name
    def search_clients(self, clients, full_client_name):
        for client in clients:
            client_full = ""      
            if client[3] == None:               
                client_full = "{0} {1} {2}".format(client[1], client[2], client[4])
            else:
                client_full = "{0} {1} {2} {3}".format(client[1], client[2], client[3], client[4])
            if full_client_name == client_full:
                return client        
        return ()
   
    # Handles post requests from the browser
    def handle_form_post_requests(self, mysql, form):
        def check_for_hash(fieldname):
            if form[fieldname] in data:
                return form[fieldname]
            return SHA3Hash().get_hash(form[fieldname])
              
        # Save or update a barrister to the database using the data from the form
        if form['submit'] == 'barrister-save':                  
            data = select_record(mysql, "SELECT * FROM barristers WHERE bar_council_num = {0}".format(form['bar-council']))
            if len(data) > 0:
                execute_command(mysql, "UPDATE barristers SET title='{0}', firstname='{1}', middle_name='{2}', surname='{3}',".format(form['barrister-title'], form['barrister-firstname'], form['barrister-middlename'], form['barrister-surname']) +
                "password='{0}', phone_number='{1}'".format(check_for_hash('barrister-password'), form['barrister-phonenumber']) +
                "WHERE bar_council_num = {0}".format(form['bar-council']))             
            else:
                execute_command(mysql, "INSERT INTO barristers VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', 0, 'BAR')".format(
                    form['bar-council'], 
                    form['barrister-title'], 
                    form['barrister-firstname'], 
                    form['barrister-middlename'], 
                    form['barrister-surname'], 
                    SHA3Hash().get_hash(form['barrister-password']), 
                    form['barrister-phonenumber']
                ))  
        # Saves or updates a solicitor to the database usingt eh form data             
        elif form['submit'] == 'solicitor-save':
            data = select_record(mysql, "SELECT * FROM solicitors WHERE solicitor_reference_id = {0}".format(form['reference-id']))
            if len(data) > 0:
                print("update")
                execute_command(mysql, "UPDATE solicitors SET title='{0}', firstname='{1}', middlename='{2}', surname='{3}', password='{4}' WHERE solicitor_reference_id = {5}".format(
                    form['solicitor-title'],
                    form['solicitor-firstname'],
                    form['solicitor-middlename'],
                    form['solicitor-surname'],
                    check_for_hash('solicitor-password'),
                    form['reference-id']
                ))
            else:            
                execute_command(mysql, "INSERT INTO solicitors VALUES {0}, '{1}', '{2}', '{3}', '{4}', '{5}', 0, 'SOL'".format(
                    form['reference-id'],
                    form['solicitor-title'],
                    form['solicitor-firstname'],
                    form['solicitor-middlename'],
                    form['solicitor-surname'],
                    SHA3Hash().get_hash(form['solicitor-password'])                   
                ))   
        # Saves or updates a court to the dataabase using the data from the form 
        elif form['submit'] == 'court-save':
            data = select_record(mysql, "SELECT * FROM courts WHERE court_id = {0}".format(form['court-id']))
            if len(data) > 0:
                execute_command(mysql, "UPDATE courts SET court_name='{0}', username='{1}', password='{2}', court_type='{3}'".format(
                    form['court-name'], 
                    form['court-username'], 
                    check_for_hash('court-password'), 
                    form['court-type']
                ))
            else:
                execute_command(mysql, "INSERT INTO courts VALUES ('{0}', '{1}', '{2}', '{3}', 0, 'CRT')".format(
                    form['court-name'],
                    form['court-username'],
                    SHA3Hash().get_hash(form['court-password']),
                    form['court-type']
                ))
        # Saves or updates an address to the database using the form data
        elif form['submit'] == 'address-save':   
            if form['address-id'] != "":
                execute_command(mysql, "UPDATE addresses SET house_number={0}, street_name='{1}', town_name='{2}', city_name='{3}', country='{4}', postcode='{5}' WHERE address_id={6}".format(
                    form['house-number'],
                    form['street-name'],
                    form['town-name'],
                    form['city'],
                    form['country'],
                    form['postcode'],
                    form['address-id']
                ))
            else:
                execute_command(mysql, "INSERT INTO addresses VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                    form['house-number'],
                    form['street-name'],
                    form['town-name'],
                    form['city'],
                    form['country'],
                    form['postcode']
                ))
        # Saves or updates a case to the database using the form data
        elif form['submit'] == 'case-save':
            data = select_record(mysql, "SELECT * FROM cases WHERE case_id={0}".format(form['claim-id']))
            if len(data) > 0:
                execute_command(mysql, "UPDATE cases SET case_id={0}, case_title='{1}', case_status={2}, start_date={3}, end_date='{4}', description_of_case='{5}', result_of_case='{6}', case_type='{7}' WHERE case_id={8}".format(
                    form['claim-id'],
                    form['case-title'],
                    form['case-status'],
                    form['case-start-date'],
                    form['case-end-date'],
                    form['case-description'],
                    form['case-result'],
                    form['case-type'],    
                    form['claim-id']           
                ))
            else:
                print("Not implemented yet!")  

# Functions for Barrister's webpage
class Barrister(object):    
    def get_cases(self, mysql):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cases")
        cases = cursor.fetchall()
        cursor.close()
        return cases
    
    def get_barrister_cases(self, mysql, barrister_id):      
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cases WHERE case_id = (SELECT case_id FROM cases_has_barristers WHERE bar_council_num=%s)", [barrister_id])
        barristers_cases = cursor.fetchall() 
        cursor.close()      
        return tuple(barristers_cases)
    
# Functions for cases webpage
class Court(object):
    court_options = ('County','Civil','Family','Circuit','High','Registry','Appeal','Tribunal')
    def get_court_cases(self, mysql, court_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cases WHERE court_id = %s", [court_id])
        court_cases = cursor.fetchall()       
        return tuple(court_cases)
      
    def get_all_cases(self, mysql):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cases")
        cases = cursor.fetchall()
        cursor.close()
        return cases

    def save_Case(self, mysql, form, court_id):
        data = select_record(mysql, "SELECT * FROM cases WHERE case_id={0}".format(form["claim-id"]))
        if (len(data) > 0):
            execute_command(mysql, "UPDATE cases SET case_id={0}, case_title='{1}', case_status={2}, start_date={3}, end_date='{4}', description_of_case='{5}', result_of_case='{6}', case_type='{7}', client_id={8}, solicitor_reference_id={9}) WHERE case_id={10}".format(
                form['claim-id'],
                form['title'],
                form['status'],
                form['start-date'],
                form['end-date'],
                form['description'],
                form['result'],
                form['type'],
                form['client'],
                form['solicitor'],
                form['claim-id']
            ))
        else:         
            execute_command(mysql, "INSERT INTO cases VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9}, {10})".format(
                form['claim-id'],
                form['title'],
                form['status'],
                form['start-date'],
                form['end-date'],
                form['description'],
                form['result'],
                form['type'],
                form['client'],
                form['solicitor'],
                court_id
            ))
        return
    


class Solicitor(object):
    def get_solicitor_cases(self, mysql, id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cases WHERE solicitor_reference_id=%s", [id])
        cases = cursor.fetchall()
        return tuple(cases)
   