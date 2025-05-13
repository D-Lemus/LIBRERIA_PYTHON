from typing import TypeVar, Callable
from collections import namedtuple
from functools import partial

T = TypeVar("T")

Customer = namedtuple("Customer", ["name", "rfc", "address"])


# HASH CODE FUNCTION FOR CUSTOMER OBJECTS
def hash_code(e: Customer, m: int) -> int:
    """
    Calculates a hash value for a Customer object.
    
    Args:
        e: Customer object to hash
        m: Size of the hash table
        
    Returns:
        An integer hash value in the range [0, m-1]
    """
    # Use the RFC as the primary key for hashing
    # Convert to a hash value using the built-in hash function
    # Take modulo m to ensure the hash is within the range [0, m-1]
    return abs(hash(e.rfc)) % m


class HashTable:
    def __init__(self, A: list[T], hash_code: Callable) -> None:
        self.table = {}
        self.hash_code = hash_code
        for e in A:
            self.insert(e)

    def __repr__(self) -> str:
        return str(self.table)

    def search(self, e: T) -> bool:
        """
        Searches for an element in the hash table.
        
        Args:
            e: Element to search for
            
        Returns:
            True if the element is in the hash table, False otherwise
        """
        # Compute the hash value for the element
        h = self.hash_code(e)
        
        # Check if the hash exists in the table
        if h not in self.table:
            return False
        
        # Check if the element is in the list at the hash position
        return e in self.table[h]

    def insert(self, e: T) -> bool:
        """
        Inserts an element into the hash table.
        
        Args:
            e: Element to insert
            
        Returns:
            True if the element was inserted, False if it was already in the table
        """
        # If the element is already in the table, don't insert it again
        if self.search(e):
            return False
        
        # Compute the hash value
        h = self.hash_code(e)
        
        # If this is the first element with this hash, create a new list
        if h not in self.table:
            self.table[h] = []
            
        # Add the element to the list at the hash position
        self.table[h].append(e)
        
        return True

    def delete(self, e: T) -> bool:
        """
        Deletes an element from the hash table.
        
        Args:
            e: Element to delete
            
        Returns:
            True if the element was deleted, False if it wasn't in the table
        """
        # Compute the hash value
        h = self.hash_code(e)
        
        # Check if the hash exists and the element is in the list
        if h in self.table and e in self.table[h]:
            # Remove the element from the list
            self.table[h].remove(e)
            
            # If the list is now empty, remove the hash entry
            if not self.table[h]:
                del self.table[h]
                
            return True
        
        # Element was not in the table
        return False


if __name__ == "__main__":
    with open("Clientes.txt", "r") as f:
        customers = [
            Customer(*[e.strip() for e in l.split("\t")]) for l in f.readlines()
        ]

    hc = partial(hash_code, m=len(customers))
    ht = HashTable(customers, hc)
    print(ht)
    # {22: [Customer(name='...'...)...]...}
    print(ht.search(customers[0]))
    # True
    print(ht.insert(customers[0]))
    # False
    print(ht.delete(customers[0]))
    # True
    print(ht.delete(customers[0]))
    # False
    print(ht.insert(customers[0]))
    # True