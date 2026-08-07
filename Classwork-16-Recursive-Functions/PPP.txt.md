# INPUT parameters: structure, parent_key (default ''), separator (default '.')

# PROCESS
elements <- empty list

IF structure is a list THEN
    items <- enumerate structure
ELSE
    items <- get key-value pairs from structure
END IF

FOR EACH key, value IN items DO
    
    IF parent_key is not empty THEN
        new_key <- parent_key + separator + key
    ELSE
        new_key <- convert key to string
    END IF
    
    IF value is a dictionary OR value is a list THEN
        # Recursive call
        nested_elements <- Flatten_JSON(value, new_key, separator)
        add all items from nested_elements to elements
    ELSE
        add (new_key, value) to elements
    END IF

END FOR

# OUTPUT
RETURN dictionary created from elements
