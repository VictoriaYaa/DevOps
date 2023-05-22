#!/usr/bin/python3
"""Usage:
    check_mysql_query_vic.py --host <host> --user <user> --db_password <db_password> --query <query> --message <query_message> --warning <warning> --critical <critical> 

Options:
    --host          Name or IP address of the server host
    --user          Name of the user to connect with
    --db_password   The user's password. Will be requested later if it's not set
    --query         MySQL query to execute
    --message , -m  Message
    --warning       Threshold as integer. eg. 1
    --critical      Threshold as integer. eg. 2


    DEPENDENCIES:
       # pip install docopt

Example:
    python3 check_mysql_query_vic.py --host localhost --user root --db_password <db_password> --query "SELECT user FROM mysql.user" --message "Test" --warning 1 --critical 2

# Adapted and configured for mysql
check_mysql_query_python.py
Author: Victoria Yaakov
"""

__author__ = 'Victoria Yaakov'
__date__ = '2022-10-25'
__version__ = '0.0.1'

# Import modules
import logging
import sys
from time import time
# Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler = logging.FileHandler('/Users/victoria.yaakov/Documents/Victoria/Scripts/check_mysql_query_vic.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Try to import two modules
try:
    from docopt import docopt 
    import mysql.connector
except ImportError as missing:
    print('''Error: Could not import "{0}" module, please choose the relevant command to install "{1}":
           # pip install docopt
           # pip install mysql-connector-python'''.format(missing.name,missing.name))
    logger.error(
        '''Error: Could not import "{0}" module, please choose the relevant command to install "{1}":
           # pip install docopt
           # pip install mysql-connector-python'''.format(missing.name,missing.name)
    )
    sys.exit(2)


if __name__ == '__main__':
    args = docopt(__doc__, version=None)
    warning = int(args["<warning>"])
    host = args["<host>"]
    mynewresult = []
    
    # Trying to connect to the Database
    try:
        mydb = mysql.connector.connect(
        host= args["<host>"],
        user= args["<user>"],
        password= args["<db_password>"],
        database="mysql",
        connection_timeout=1000
        )
    except:
        print("Error: Can't connect to '{0}' server with {1}".format("mysql",host))
        logger.error("Error: Can't connect to '{0}' server with {1}".format("mysql",host))
        sys.exit(1)
    
    # Try to parse the results
    mycursor = mydb.cursor(args["<query>"])
    try:
        query_start = time()
        mycursor.execute(args["<query>"])
        query_stop = time()
        query_time = query_stop - query_start
        query_time = str(float(f'{query_time:.4f}'))
        myresult = mycursor.fetchall()
        for item in myresult:
            mynewresult.append(item)
        # row number is less then critical and bigger than warning
        if (len(myresult) < int(args["<critical>"]) and myresult != [] and len(myresult) >= int(args["<warning>"])):
            # row number is less than critical and not empty
            if len(mynewresult) < int(args["<critical>"]) and mynewresult != ['0'] and mynewresult != ['None'] and mynewresult != [('None',)] and mynewresult != [(0,)]:
                print('''Warning: Found {0} workflow id:'''.format(len(mynewresult)))
                for x in mynewresult:
                    print(x)
                print(''' | mysql_query_time={0}s'''.format(query_time))
                logger.error('''Warning: Found {0} workflow. id:{1}'''.format(len(mynewresult) ,mynewresult))
                sys.exit(1)
            # row number is bigger than critical and not empty
            elif (len(mynewresult) >= int(args["<critical>"]) and mynewresult != ['0'] and mynewresult != ['None'] and mynewresult != [('None',)] and mynewresult != [(0,)]):
                print('''Critical: Found {0} workflows ids:'''.format(len(mynewresult)))
                for x in mynewresult:
                    print(x)
                print(''' | mysql_query_time={0}s'''.format(query_time))
                logger.error('''Critical: There are {0} workflows. ids:{1}'''.format(len(mynewresult),mynewresult))
                sys.exit(2)
            else:
                print("OK: Found failing workflows: 'None' | mysql_query_time={0}s".format(query_time))
                sys.exit(0)
        # row number is bigger than critical or equal to critical and not empty
        elif (len(myresult) >= int(args["<critical>"]) and mynewresult != ['0'] and mynewresult != ['None'] and mynewresult != [('None',)] and mynewresult != [(0,)]):
            print('''Critical: Found {0} workflows ids:'''.format(len(mynewresult)))
            for x in mynewresult:
                print(x)
            print(''' | mysql_query_time={0}s'''.format(query_time))
            logger.error('''Critical: There are {0} workflows. ids:{1}'''.format(len(mynewresult),mynewresult))
            sys.exit(2)
        else:
            print("OK: Found failing workflows: 'None' | mysql_query_time={0}s".format(query_time))
        mycursor.close()
    except mysql.connector.Error as err:
        print(
        '''Error: {0}'''.format(err)
        )
        logger.error('''Error: {0}'''.format(err))
        sys.exit(1)