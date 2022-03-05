from flask import session


def capcalculate():
    yourcrypto = session['yourcrypto']
    futurecrypto = session['futurecrypto']

    upside = futurecrypto/yourcrypto

    message = f'the upside will be a {upside}x'
    return message 
