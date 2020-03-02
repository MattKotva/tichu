class IllegalPlayError(Exception):
    '''Raised when Player tries to play an illegal play'''
    pass


class IllegalTichuCallError(Exception):
    '''Raised when Player tries to call Tichu ater playing a card'''
    pass