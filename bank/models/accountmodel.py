accounts = {}

class AccountModels():

    def __init__(self, iban, bankcode, customerid=0, accountid=0,):
        '''
        Account create
        Arguments: 
            iban {[string]}
            bankcode {[int]}
            customerid {[int]}
        '''
        self.accountid = self.create_accountid()
        self.iban = iban
        self.bankcode = bankcode
        self.customerid = self.create_customerid()

    def serialize(self):
        ''' returns string string representations of the dictionary object '''
        return {
            'accountid': self.accountid,
            'iban': self.iban,
            'bankcode': self.bankcode,
            'customerid': self.customerid
        }
    
    ''' Check for duplicates'''
    @staticmethod
    def input_exists(accounts, iban):
        for x in accounts:
            if accounts[x].iban == iban:
                return x
        return False
    
    ''' autogenerate accountid for new account'''
    def create_accountid(self, accountid=0):
        if accountid == 0:
            accountid = len(accounts)+1

        if accountid in accounts:
            accountid = accountid+1
            return self.create_accountid(accountid)
        return accountid
    
    ''' autogenerate customerid for new account'''
    def create_customerid(self, customerid=0):
        if customerid == 0:
            customerid = len(accounts)+1

        if customerid in accounts:
            customerid = customerid+1
            return self.create_customerid(customerid)
        return customerid

    ''' Function to return a dictionary object'''
    def account_dict(self):
        return dict(accountid=self.accountid)
    
    def detail_list(self):
        ''' get all attributes of an object'''
        return dict(accountid=self.accountid, iban=self.iban, bankcode=self.bankcode, customerid=self.customerid)
    
    def get_accounts(self):
        return dict(accountid=self.accountid, iban=self.iban, bankcode=self.bankcode)
    
    ''' Insert the object into the list of accounts'''
    def save_accounts(self):
        accounts[self.accountid] = self
    
    def update_account(self, iban, bankcode):
        ''' Updates iban and bank code of an account'''
        self.iban = iban
        self.bankcode = bankcode
    
    def delete_account(self):
        ''' remove account from the list of accounts'''
        del accounts[self.accountid]

    def delete_accounts(self):
        ''' deletes all the accounts from the list'''
        accounts.clear()

    
    ''' function to be used to check for duplicates in the list '''
    def check_accounts(self, iban=None):
        if iban == None:
            iban = self.iban
        for x in accounts:
            if accounts[x].iban == iban:
                return x
        return False