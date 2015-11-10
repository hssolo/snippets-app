import logging
import argparse
import sys
import psycopg2


logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname= 'snippets'")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    #NOTE: Allows Python to run sql commands in Postgres session.
    cursor = connection.cursor()
    #NOTE: %s is substituted by the tuple in the cursor.execute method.
    try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError:
        print('exception error')
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name. If there is no such snippet nothing Returns the snippet"""
    logging.info("Retrieving snippet {!r})".format(name)) 
    cursor = connection.cursor()
    #QUESTION: Dont understand how it knows where to substitute the %s.
    command = "select keyword, message from snippets where keyword= (%s)"
    #ANSWER:  psycopg2 does translation of this
    #NOTE: When you execute a SQL statement, the parameters must always be packaged up into a tuple. This requires a comma: (word,) not just (word).
    cursor.execute(command, (name,)) 
    result = cursor.fetchone() 
    connection.commit()
    if not result:
        print("that snippet does not exist")
    else: 
        logging.debug("Snippet pulled successfuly: {!r}".format(result[1]))
        return result[1]
    
def main():
    #NOTE: Alone this only provides the description without any other help.
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    print('printing argparse object:')
    print(parser)
    print("\n")
    
    # #NOTE: Allows for positional arguments. Alone it creates an {empty set} of available commands.
    logging.info("Constructing subparser")
    subparsers = parser.add_subparsers(dest="command", help="Available commands") 
    print('printing subparse object:')
    print(subparsers)
    print("\n")
    
    #NOTE: Provides values to {empty set} in subparsers.
    logging.debug("Constructing put_subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    print(put_parser)
    print("\n")
    
    #NOTE: Provides values to {empty set} in subparsers object.
    logging.debug("Constructing get_subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    print(get_parser)
    print("\n")
    
    #NOTE: Adds positional arguments to --help
    put_parser.add_argument("name", help="The name of the snippet") 
    put_parser.add_argument("snippet", help="The snippet text") 
    get_parser.add_argument("name", help="The name of the snippet") #Positional Argument
    
    #NOTE: This becomes Namespace
    arguments = parser.parse_args(sys.argv[1:]) 
    print('First Value: The "arguments" variable equals "Namespace" of the command line arguments')
    print(arguments)
    print (type(arguments))
    print("\n")
    
    #NOTE: Converts the command line arguments of variable-"arguments" into a dictionary
    arguments = vars(arguments)
    print('Second Value: The arguments variable is converted to a string based key:value dictionary')
    print(arguments)
    print(type(arguments))
    print(len(arguments))
    print("\n")
    
    #NOTE:"command" string in parentheses relates to dest=("command") of subparser on line 40.
    kommand = arguments.pop("command") 
    print('the value of kommand is:')
    print(kommand)
    print("\n")
    
    if kommand == "put":
        another_name, another_snippet = put(**arguments)
        print(another_snippet)
        print(another_name)
        print("Stored {!r} as {!r}".format(another_snippet, another_name))
    elif kommand == "get":
        message = get(**arguments)
        print(message)
        print("Retrieved snippet: {!r}".format(message))
   

    
if __name__ == "__main__":
    main()




  #!r = used for print and logging info such as used with .format, %s is used with variables 
 
  