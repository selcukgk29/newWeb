from flask import session,redirect

def sessionControl():
    try:
        session['username']
    except:
        return redirect('/')