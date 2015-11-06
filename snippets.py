import logging
import argparse
import sys

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """Store a snippet with an associated name and returns the name and the snippet"""
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name. If there is no such snippet nothing Returns the snippet"""
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    get_parser = subparsers.add_parser("get", help="retrieve a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    get_parser.add_argument("name", help="The name of the snippet")
    arguments = parser.parse_args(sys.argv[1:])
    arguments = vars(arguments) ## Converts the command line arguments in variable arguments into a dictionary.
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
        
            

    
if __name__ == "__main__":
    main()
