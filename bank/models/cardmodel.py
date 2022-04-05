import json
from .accountmodel import accounts

cards = {}
cardTypes = ['virtual', 'physical']

class CardsModel():

    def __init__(self, cardalias, cardtype,  accountid, cardid=0):
        '''
        Account create
        Arguments: 
            cardalias {[string]}
            accountid {[int]} - accountid related to the card
            cardtype {[string]}
        '''
        self.cardid = self.create_cardid()
        self.cardalias = cardalias
        self.cardtype = cardtype
        self.accountid = [accountid for x in accounts if accounts[x] == accountid]

    def serialize(self):
        ''' returns string string representations of the dictionary object '''
        return {
            'cardid': self.cardid,
            'cardalias': self.cardalias,
            'cardtype': self.cardtype,
            'customerid': self.cardid
        }
    
    ''' Check for duplicates'''
    @staticmethod
    def input_exists(cards, cardalias):
        for x in cards:
            if cards[x].cardalias == cardalias:
                return x
        return False
    
    ''' autogenerate accountid for new account'''
    def create_cardid(self, cardid=0):
        if cardid == 0:
            cardid = len(accounts)+1

        if cardid in accounts:
            cardid = cardid+1
            return self.create_cardid(cardid)
        return cardid
    

    ''' Function to return a dictionary object'''
    def card_dict(self):
        return dict(cardid=self.cardid)
    
    def detail_list(self):
        ''' get all attributes of an object'''
        return dict(cardid=self.cardid, cardalias=self.cardalias, cardtype=self.cardtype, accountid=self.accountid)
    
    
    ''' Insert the object into the list of accounts'''
    def save_cards(self):
        cards[self.cardid] = self
    
    def update_card(self, cardalias):
        ''' Updates iban and bank code of an account'''
        self.cardalias = cardalias
    
   

    
    ''' function to be used to check for duplicates in the list '''
    def check_cards(self, cardalias=None):
        if cardalias == None:
            cardalias = self.cardalias
        for x in cards:
            if cards[x].cardalias == cardalias:
                return x
        return False