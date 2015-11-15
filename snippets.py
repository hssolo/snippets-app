import logging
import argparse
import sys
import psycopg2

# set log file and log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

# initial connection to PostgresSQL db
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname= 'snippets'")
logging.debug("Database connection established.")


def put(name, snippet, hide=False):
    #Question: because the value of arguments is a dictionary without order and used in, put(**arguments),
    #how is name, snippet and hide able to take the appropriate values from put(**arguments)?
    #import pdb; pdb.set_trace()
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}, {!r}".format(name, snippet, hide))
    with connection, connection.cursor() as cursor:
        try:
            command = "insert into snippets values (%s, %s, %s)"
            cursor.execute(command, (name, snippet, hide))
        except psycopg2.IntegrityError:
            connection.rollback()
            command = "update snippets set message=%s, hidden=%s where keyword=%s"
            cursor.execute(command, (snippet, hide, name))
        connection.commit()
        logging.debug("Snippet stored successfully.")
        return name, snippet
    
def get(name):
    """
        Retrieve the snippet with a given name. If there is no such snippet 
        nothing Returns the snippet
    """
    logging.info("Retrieving snippet {!r})".format(name)) 
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        result = cursor.fetchone()
        connection.commit()
    if not result:
        print("that snippet does not exist")
        print(" -h or --help for additional commands")
    else: 
        logging.debug("Snippet pulled successfuly: {!r}".format(result))
        return result
        
def catalog():
    """List all the Keyword names in the snippets db"""
    logging.info("Retrieving keywords")
    cursor = connection.cursor()
    command = "select keyword from snippets where hidden=False order by keyword"
    cursor.execute(command)
    result = cursor.fetchall() 
    connection.commit()
    return result
    
def search(string):
    """Search for a string through all the snippets in the snippets db"""    
    logging.info("Searching for strings")
    cursor = connection.cursor()
    cursor.execute("select * from snippets where message like {!r} and hidden=False".format(string))
    result = cursor.fetchall()
    connection.commit()
    logging.debug("String found successfuly: {!r}".format(result))
    return result
    
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="can_be_anything", help="Available commands")
    
    # Subparser for put command
    logging.debug("Constructing put subparsers")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")#'name' is variable for  what is being expected  as a command line argument.  
    put_parser.add_argument("snippet", help="The snippet text") 
    put_parser.add_argument("--hide", action="store_true")
    
    # Subparser for get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    # Subparser for catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Query for keywords")
    
    # Subparser for search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Run a search")
    search_parser.add_argument("string", help="search string in snippet")

    # Convert parsed arguments from Namespace to dictionary
    arguments = parser.parse_args(sys.argv[1:])
    arguments = vars(arguments)
    kommand = arguments.pop("can_be_anything")

    
    if kommand == "put":
        another_name, another_snippet = put(**arguments) 
        #Question: Why can't I use "hide" here? I get an unpack error.
        print(another_name, another_snippet)
        print("Stored {!r} as {!r}".format(another_snippet, another_name))
    elif kommand == "get":
        message = get(**arguments)
        print("Retrieved snippet: {!r}".format(message))
    elif kommand == "catalog":
        keywords = catalog()
        print("Retrieved list of names: {!r}".format(keywords)) 
    elif kommand == "search":
        find = search(**arguments)
        print("Search found the following: {!r}".format(find))

    
if __name__ == "__main__":
    main()




#Question: Again, When do I use {!r} vs %s?
#Question: How would I have used --show or --unhide?


 
  