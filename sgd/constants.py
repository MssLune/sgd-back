# True options list
TRUE_OPTIONS = ['True', 'true', 't', 'T', '1', 1, True]

DELETED_USER = 2  # user pk for replace relations with

# Role: used for permissions based on group model
# Update this class anytime there are updates in Group table

class ROLE:
    ADMIN = 1
    TECHNICIAN = 2
    CLIENT = 3
