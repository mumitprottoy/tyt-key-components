from django.contrib.auth.models import User
import requests, json
from utils.operations import dict_to_object as ditto
from tytfs.models import StudentClub
from tytfs.models import StudentClubEmailLead as SCEL

def resolve_url(name):
    return f'https://theyellowtherapist.com/data/{name}'
    

def import_clubs():
    clubs = requests.get(resolve_url('clubs')).json()['data']
    for c in clubs:
        club = ditto(c)
        if not StudentClub.objects.filter(name=club.name).exists():
            new_club = StudentClub(
                name=club.name, logo_url=club.logo_link)
            new_club.save()



def import_email_leads():
    leads = requests.get(resolve_url('tytfs')).json()['data']
    for l in leads:
        lead = ditto(l)
        club = StudentClub.objects.get(name=lead.club)
        if not SCEL.objects.filter(club=club, email=lead.email).exists():
            SCEL(club=club, email=lead.email).save()
        
        
        
        
    
def get_users():
    import re, requests, json
    from random import randint
    users = requests.get('https://theyellowtherapist.com/data/clients').json()['data']
    l2 = [user for user in users if user['l2']]
    non_l2 = [user for user in users if not user['l2']]
    REGEX = {
        'username': r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$',
        'name_sub': r'[^a-zA-Z\s]',
        'name': r'^[a-zA-Z.\s]',
    }

    def split_names(name: str):
        return [' '.join(name.split()[:-1]), name.split()[-1]]
    nicknames = {}
    usernames = []
    user_data = []
    errors = []
    for u in l2:
        user = ditto(u)
        try:
            _, __ = split_names(user.full_name)
            def filter_name(first_name: str, last_name: str) -> list[str]:
                names: list[str] = [first_name, last_name]
                for n in range(len(names)):
                    if len(names[n]) > 0:
                        # names[n] = re.sub(REGEX['space_sub'], ' ', names[n])
                        chars = list(names[n])
                        if chars[0].isalpha():
                            chars[0] = chars[0].upper()

                        for i in range(1, len(chars)):
                            if chars[i-1] == '.' or chars[i-1] == ' ':
                                if chars[i].isalpha():
                                    chars[i] = chars[i].upper()

                        names[n] = ''.join(chars)
                        names[n] = re.sub(REGEX['name_sub'], '', names[n])

                return names
            first_name, last_name = filter_name(_, __)
            user.nickname = user.nickname.lower().strip()
            def get_unique_username(_username):
                if _username in usernames:
                    _username = user.nickname.lower() + str(randint(1,99))
                    return get_unique_username(_username)
                else: return _username
            username = get_unique_username(user.nickname)
            usernames.append(username)
            birthyear = int(user.birthdate.split()[-1])
            signup_info = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': user.email,
                'password': user.password
            }
            contact_info = {
                'phone_number': user.phone_number
            }
            personal_info = {
                'gender': user.gender,
                'birth_year': birthyear
            }

            user_data.append(ditto({
                'signup': signup_info,
                'contact_info': contact_info,
                'personal_info': personal_info
            }))
        except Exception as exec:
            d = user.__dict__.copy()
            d['exception'] = str(exec)
            errors.append(d)



    return user_data



def import_users():
    users = get_users()
    total_users = len(users)
    total_user_saved = 0
    total_contactinfo_saved = 0
    total_personalinfo_saved = 0
    total_additonalinfoflag_saved = 0
    total_emailverificationflag_saved = 0
    for _ in users:
        try:
            if User.objects.filter(username=_.signup['username']).exists():
                continue
            if User.objects.filter(email=_.signup['email']).exists():
                continue
            user = User(**_.signup).save(); total_user_saved += 1
        except Exception as exec: print(exec); continue
        # try:
        #     user.contactinfo.phone_number = _.contact_info['phone_number']
        #     user.contactinfo.save()
        #     total_contactinfo_saved += 1
        # except Exception as exec:print(exec); continue
        # try:
        #     user.personalinfo.gender = _.personal_info['gender']
        #     user.personalinfo.birth_year = _.personal_info['birth_year']
        #     user.personalinfo.save()
        #     total_personalinfo_saved += 1
        # except Exception as exec:print(exec); continue
        # try:
        #     user.emailverificationflag.verified=True
        #     user.emailverificationflag.save()
        #     total_emailverificationflag_saved += 1
        # except Exception as exec:print(exec); continue
        # try:
        #     user.additionalinfoflag.added = True
        #     user.additionalinfoflag.Save()
        #     total_additonalinfoflag_saved += 1
        # except Exception as exec:print(exec); continue
    
    print('Total Importable Users:', total_users)
    print('Total saved users:', total_user_saved)
    # print('Total saved ContactInfo:', total_contactinfo_saved)
    # print('Total saved PersonalInfo:', total_personalinfo_saved)
    # print('Total saved AdditionalInfoFlag:', total_additonalinfoflag_saved)
    # print('Total saved EmailVerificationFlag:', total_emailverificationflag_saved)
        

def remove():
    users = get_users()
    found = deleted = 0

    for _ in users:
        try:
            if User.objects.filter(username=_.signup['username']).exists():
                found += 1
                User.objects.get(username=_.signup['username']).delete()
                deleted += 1
        except: continue
    
    print('Found', found)
    print('Deleted', deleted)

    
def ok():
    users = get_users()
    email_count = 0
    for _ in users:
        if not User.objects.filter(username=_.signup['username'], email=_.signup['email']).exists():
            # print(json.dumps(_.__dict__, indent=4))
            if User.objects.filter(email=_.signup['email']).exists():
                user = User.objects.get(email=_.signup['email'])
                print(json.dumps({
                    'username': user.username, 'email': user.email 
                }, indent=4))


def import_non_l2():
    import re, requests, json
    from random import randint
    users = requests.get('https://theyellowtherapist.com/data/clients').json()['data']
    non_l2_users = [user for user in users if not user['l2']]
    found = saved = 0
    for u in non_l2_users:
        user = ditto(u)
        if not User.objects.filter(email=user.email).exists():
            if not User.objects.filter(**{
                    'first_name': 'Default',
                    'last_name': 'User',
                    'username': user.email.split('@')[0],
                    'email': user.email,
                }).exists():
                if user.email.split('@')[0] in ('tanvir', 'info'):
                    User(**{
                    'first_name': 'Default',
                    'last_name': 'User',
                    'username': user.email.split('@')[0]+'_',
                    'email': user.email,
                }).save()
      
            

     