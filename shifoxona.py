import os
import time

# Shifokorlar bazasi
doctors_db = {
    'abubakr': {
        'name': 'Dr. Alijonov Abubakr',
        'password': 'admin',
        'type': 'Pediatr (Bolalar shifokori)',
        'bemorlar': []
    },
    'nodir': {
        'name': 'Dr. Nodir',
        'password': '1111',
        'type': 'Stomatolog (Tish shifokori)',
        'bemorlar': []
    },
    'azim': {
        'name': 'Dr. Azim',
        'password': '2222',
        'type': 'Xirurg (Jarroh)',
        'bemorlar': []
    }
}

# Foydalanuvchilar bazasi
users_db = {
    '+998901234567': {
        'name': "Abdumalik To'ychiyev",
        'age': 18,
        'password': '123'
    }
}



def clear():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

YASHIL = '\033[32m'
QIZIL = '\033[31m'
SARIQ = '\033[33m'
KOK = '\033[34m'
RESET = '\033[0m'
def print_color(text, color=RESET):
    print(f"{color}{text}{RESET}")

def wait(seconds):
    time.sleep(seconds)



def doctor_panel(doc_username):
    current_doc = doctors_db[doc_username] 
    
    while True:
        clear()
        print_color(f"--- SHIFOKOR PANELI: {current_doc['name']} ---", SARIQ)
        print(f"Mutaxasislik: {current_doc['type']}")
        print("--------------------------------")
        print("1. Bemorlarim ro'yxati")
        print("2. Qabulni boshlash (Ko'rik)")
        print("0. Chiqish")
        
        choice = input("\nTanlovni kiriting: ")
        
        if choice == '1':
            print_color("\n--- NAVBATDAGI BEMORLAR ---", KOK)
            if not current_doc['bemorlar']:
                print("Hozircha bemorlar yo'q.")
            else:
                for i, patient in enumerate(current_doc['bemorlar'], 1):
                    print(f"{i}. {patient['name']} (Tel: {patient['phone']})")
            
            input("\nDavom etish uchun Enterni bosing...")

        elif choice == '2':
            if not current_doc['bemorlar']:
                print_color("\nKo'rik o'tkazish uchun bemorlar yo'q!", QIZIL)
            else:
                patient = current_doc['bemorlar'][0]
                print(f"\nBemor qabul qilinmoqda: {patient['name']}...")
                wait(2)
                print_color("Ko'rik muvaffaqiyatli yakunlandi!", YASHIL)

                current_doc['bemorlar'].pop(0)
            
            input("\nDavom etish uchun Enterni bosing...")

        elif choice == '0':
            print("\nTizimdan chiqilmoqda...")
            wait(1)
            break
        else:
            print_color("Noto'g'ri tanlov!", QIZIL)
            wait(1)

def user_panel(phone):
    current_user = users_db[phone]
    
    while True:
        clear()
        print_color(f"--- FOYDALANUVCHI PANELI: {current_user['name']} ---", SARIQ)
        print("1. Mening ma'lumotlarim")
        print("2. Shifokor qabuliga yozilish")
        print("0. Chiqish")
        
        choice = input("\nTanlovni kiriting: ")
        
        if choice == '1':
            print_color("\n--- SHAXSIY MA'LUMOTLAR ---", KOK)
            print(f"Ism-familiya: {current_user['name']}")
            print(f"Yosh: {current_user['age']}")
            print(f"Telefon: {phone}")
            input("\nQaytish uchun Enterni bosing...")
            
        elif choice == '2':
            clear()
            print_color("--- MAVJUD SHIFOKORLAR ---", KOK)
            
            for idd, data in doctors_db.items():
                print(f"ID: {idd} | Ism: {data['name']} |", end=' ')
                print_color(data['type'], SARIQ)
            
            print("\n0. Orqaga qaytish")
            
            doc_choice = input("\nQabuliga yozilmoqchi bo'lgan Shifokor ID sini yozing: ")
            
            if doc_choice == '0':
                continue
            
            if doc_choice in doctors_db:
                selected_doc = doctors_db[doc_choice]
                
                new_appointment = {
                    'name': current_user['name'],
                    'phone': phone
                }
                selected_doc['bemorlar'].append(new_appointment)
                
                print_color(f"\n{selected_doc['name']} qabuliga muvaffaqiyatli yozildingiz!", YASHIL)
                wait(2)
            else:
                print_color("Bunday ID li shifokor topilmadi!", QIZIL)
                wait(1)
                
        elif choice == '0':
            print("\nTizimdan chiqilmoqda...")
            wait(1)
            break



def login(user_type):
    clear()
    
    if user_type == 'doctor':
        print_color("--- SHIFOKOR SIFATIDA KIRISH ---", SARIQ)
        print('Orqaga qaytish uchun: 0')
        username = input("Login: ")
        if username == '0': return
        password = input("Parol: ")
        
        if username in doctors_db and doctors_db[username]['password'] == password:
            print_color("Kirish muvaffaqiyatli!", YASHIL)
            wait(1)
            doctor_panel(username)
        else:
            print_color("Login yoki parol xato!", QIZIL)
            wait(1.5)

    elif user_type == 'user':
        print_color("--- FOYDALANUVCHI SIFATIDA KIRISH / RO'YXATDAN O'TISH ---", SARIQ)
        phone = input("Telefon raqamingiz (+998901234567): ")
        if phone == '0': return
        

        if phone not in users_db:
            print_color("\nRaqam bazada topilmadi. Ro'yxatdan o'tish:", KOK)
            name = input("Ism-familiyangizni kiriting: ")
            age = input("Yoshingizni kiriting: ")
            new_password = input("Yangi parol o'ylab toping: ")
            
            users_db[phone] = {
                'name': name,
                'age': age,
                'password': new_password
            }
            print_color("Ro'yxatdan o'tish muvaffaqiyatli!", YASHIL)
            print("Tizimga kirilmoqda...")
            wait(1.5)
            user_panel(phone)
            

        else:
            password = input("Parolingizni kiriting: ")
            if users_db[phone]['password'] == password:
                print_color("Xush kelibsiz!", YASHIL)
                wait(1)
                user_panel(phone)
            else:
                print_color("Parol noto'g'ri!", QIZIL)
                wait(2)


while True:
    clear()
    print_color("=== SHIFOXONA TIZIMI ===", KOK)
    print("1. Shifokor sifatida kirish")
    print("2. Foydalanuvchi sifatida kirish")
    print("0. Dasturdan chiqish")
    
    main_choice = input("\nTanlovni kiriting: ")
    
    if main_choice == '1':
        login('doctor')
    elif main_choice == '2':
        login('user')
    elif main_choice == '0':
        print_color("Dastur yakunlandi!", YASHIL)
        break
    else:
        print_color("Noto'g'ri tanlov!", QIZIL)
        wait(1)