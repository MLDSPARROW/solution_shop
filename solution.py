import mysql.connector
from datetime import datetime


def start_analyzing():
    """
    the main function of the project and analyzes based on the fetched data from database
    """

    current_date, current_month = get_current_date()
    
    cnx = get_connection()
    
    budgets = get_budgets(cnx, current_month)

    for item in budgets:
        shop_id = item[0]
        shop_name = item[1]
        spent_amount = item[2]
        budget_amount = item[3]
        month = item[4]
        notified_threshold = item[5]
        spent_to_budget = round((spent_amount / budget_amount) * 100, 2)

        if spent_to_budget >= 50 and spent_to_budget < 100:
            if not notified_threshold:
                insert_notified_and_show_message(cnx, shop_id, current_date, shop_name , spent_to_budget, month, '50%')
        elif spent_to_budget >= 100:
            if notified_threshold != '100%':
                insert_notified_and_show_message(cnx, shop_id, current_date, shop_name , spent_to_budget, month, '100%')
            
    
    #close the connection to database
    cnx.close()

def get_current_date():
    """
    return current month and dcurrent date
    """

    current_month = datetime.today().strftime('%Y-%m') + '-1'
    current_date = datetime.today().strftime('%Y-%m-%d')
    
    return current_date, current_month

def get_connection():
    """
    have one connection which is re usable for all tasks:
    returns a connection
    """

    cnx = mysql.connector.connect(user = 'username', password = 'password', host = 'hostaddress', database = 'databasename')

    return cnx

def get_budgets(cnx, current_month):
    """
    get all information of shops and budgets by joining two tables of T_SHOPS and T_BUDGETS 
    which they are online and are for current month

    returns the list of budgets as a generator
    """

    resuls_cursor = cnx.cursor(buffered=True)

    # the query gets all data which are in current month and also they are online: A_ONLINE = 1
    query = "SELECT S.A_ID,A_NAME,A_AMOUNT_SPENT,A_BUDGET_AMOUNT,B.A_MONTH,N.A_THRESHOLD  FROM T_SHOPS S INNER JOIN T_BUDGETS B ON S.A_ID = B.A_SHOP_ID LEFT JOIN T_NOTIFIED N ON S.A_ID = N.A_SHOP_ID AND B.A_MONTH = N.A_MONTH WHERE B.A_MONTH = '{}' and A_ONLINE = 1;".format(current_month)
    resuls_cursor.execute(query)

    # Using the generator not to push so much pressure on the CPU
    budgets = (item for item in resuls_cursor)

    return budgets

def insert_notified_and_show_message(cnx, shop_id, current_date, shop_name , spent_to_budget, month, threshold):
    """
    based on the threshold, the notified row is inserted into the T_NOTIFIED
    the structure of the table is defined in a way that two similar thresholds in the same month and shop_id cannot be inserted
    if the threshold arrives to 100%, also updates online status inside if the T_SHOPS
    """
    cursor = cnx.cursor()
    if threshold == '50%':
        query = "INSERT INTO T_NOTIFIED (A_SHOP_ID, A_MONTH, A_THRESHOLD) VALUES ({}, '{}', '{}');".format(shop_id, month, threshold)
        try:
            cursor.execute(query)
            cnx.commit()
            show_message(current_date, shop_name , spent_to_budget)
        except:
            print("Unexpected Error was Happened")
        
    elif threshold == '100%':
        query = "INSERT INTO T_NOTIFIED (A_SHOP_ID, A_MONTH, A_THRESHOLD) VALUES ({}, '{}', '{}');".format(shop_id, month, threshold)
        try:
            cursor.execute(query)
            cnx.commit()
            show_message(current_date, shop_name , spent_to_budget, off_line = True)
            query = "Update T_SHOPS SET A_ONLINE = 0 WHERE A_ID = {};".format(shop_id)
            cursor.execute(query)
            cnx.commit()
        except:
            print("Unexpected Error was Happened")

def show_message(current_date, shop_name , spent_to_budget, off_line = False):
    """
    shows the message by printingon terminal based on the given parametrs 
    """
    off_line_message = ''
    if off_line:
        off_line_message = '\n    and Your advertisement will be removed from site for this month'
    message = """
    Date: {}
    Dear {}
    You have spent {} % of monthly budget{}
    """.format(current_date, shop_name, spent_to_budget, off_line_message)
    print(message)


if __name__ == "__main__":
    start_analyzing()
