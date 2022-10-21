from email_validator import validate_email, EmailNotValidError
def usernameValid(username):
    if len(username)<3:
        return False    
    return True

def emailValid(email):
    try:
        email = validate_email(email).email     
    except EmailNotValidError as e:   
        print(e)    
        return e


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%', ".",",","+","-","*","/","!", "?", "_", "=", ")", "(", "&"]
    val = True

    if len(passwd) < 6:
        val = False

    if len(passwd) > 20:
        val = False

    if not any(char.isdigit() for char in passwd):
        val = False

    if not any(char.isupper() for char in passwd):
        val = False

    if not any(char.islower() for char in passwd):
        val = False

    if not any(char in SpecialSym for char in passwd):
        val = False
    if val:
        return val
