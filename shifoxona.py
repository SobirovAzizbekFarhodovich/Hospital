import os
import time
import json
from datetime import datetime


def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)



doctors_db = load_json("doctors.json")
users_db = load_json("users.json")
admin_db = load_json("admin.json")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


YASHIL = '\033[32m'
QIZIL = '\033[31m'
SARIQ = '\033[33m'
KOK = '\033[34m'
RESET = '\033[0m'

def print_color(text, color=RESET):
    print(f"{color}{text}{RESET}")


def wait(seconds):
    time.sleep(seconds)






def admin_panel():
    while True:
        clear()
        print_color("--- ADMIN PANEL ---", SARIQ)
        print("1. Doktorlarni ko‘rish")
        print("2. Doktor qo‘shish")
        print("3. Doktor o‘chirish")
        print("4. Foydalanuvchilar ro‘yxati")
        print("5. Foydalanuvchini boshqarish")
        print("0. Chiqish")

        choice = input("\nTanlov: ")

    
        if choice == "1":
            clear()
            print_color("--- DOKTORLAR RO‘YXATI ---", KOK)
            if not doctors_db:
                print("Hozircha shifokorlar yo‘q.")
            else:
                for k, d in doctors_db.items():
                    print(f"ID: {k} | {d['name']} | {d['type']}")
            input("\nQaytish uchun Enter...")

        elif choice == "2":
            clear()
            print_color("--- YANGI DOKTOR QO‘SHISH ---", KOK)
            doc_id = input("Doktor ID (login): ")
            if doc_id in doctors_db:
                print_color("Bu ID allaqachon mavjud!", QIZIL)
                wait(1.5)
                continue

            name = input("Ism-familiya: ")
            password = input("Parol: ")
            type_ = input("Mutaxassislik: ")

            doctors_db[doc_id] = {
                'name': name,
                'password': password,
                'type': type_,
                'bemorlar': []
            }

            save_json("doctors.json", doctors_db)
            print_color("Doktor muvaffaqiyatli qo‘shildi!", YASHIL)
            wait(1.5)

        elif choice == "3":
            clear()
            print_color("--- DOKTOR O‘CHIRISH ---", KOK)
            doc_id = input("O‘chirmoqchi bo‘lgan doktor ID: ")
            if doc_id not in doctors_db:
                print_color("Bunday ID mavjud emas!", QIZIL)
            else:
                del doctors_db[doc_id]
                save_json("doctors.json", doctors_db)
                print_color("Doktor o‘chirildi!", YASHIL)
            wait(1.5)



        elif choice == "4":
            clear()
            print_color("--- FOYDALANUVCHILAR RO‘YXATI ---", KOK)

            if not users_db:
                print("Bazada foydalanuvchi yo‘q.")
            else:
                for phone, u in users_db.items():
                    status = "BLOKLANGAN" if u.get("blocked") else "Faol"
                    print(f"{phone} | {u['name']} | {status}")

            input("\nQaytish uchun Enter...")

        elif choice == "5":
            clear()
            print_color("--- FOYDALANUVCHI BOSHQARISH ---", KOK)
            phone = input("Foydalanuvchi telefon raqami: ")

            if phone not in users_db:
                print_color("Bunday foydalanuvchi mavjud emas!", QIZIL)
                wait(1.5)
                continue

            usr = users_db[phone]

            while True:
                clear()
                print_color(f"{usr['name']} ({phone})", SARIQ)
                print("1. Kartasini ko‘rish")
                print("2. Bloklash")
                print("3. Blokdan chiqarish")
                print("0. Chiqish")

                c = input("\nTanlov: ")

                if c == "1":
                    clear()
                    print_color("--- BEMOR KARTASI ---", KOK)

                    if not usr.get("history"):
                        print("Hali hech qaysi shifokorga murojaat qilmagan.")
                    else:
                        for i, h in enumerate(usr['history'], 1):
                            print(f"{i}. Shifokor: {h['doctor']} ({h['type']}) | Sana: {h['time']}")

                    input("\nOrqaga qaytish uchun Enter...")

                elif c == "2":
                    usr["blocked"] = True
                    save_json("users.json", users_db)
                    print_color("Foydalanuvchi bloklandi!", YASHIL)
                    wait(1)

                elif c == "3":
                    usr["blocked"] = False
                    save_json("users.json", users_db)
                    print_color("Foydalanuvchi blokdan chiqarildi!", YASHIL)
                    wait(1)

                elif c == "0":
                    break

                else:
                    print_color("Xato tanlov!", QIZIL)
                    wait(1)


        elif choice == "0":
            break

        else:
            print_color("Noto‘g‘ri tanlov!", QIZIL)
            wait(1)






def doctor_panel(doc_username):
    current_doc = doctors_db[doc_username]

    while True:
        clear()
        print_color(f"--- SHIFOKOR PANELI: {current_doc['name']} ---", SARIQ)
        print(f"Mutaxassislik: {current_doc['type']}")
        print("--------------------------------")
        print("1. Bemorlar ro‘yxati")
        print("2. Qabulni boshlash")
        print("0. Chiqish")

        choice = input("\nTanlov: ")

        if choice == "1":
            clear()
            print_color("--- BEMORLAR ---", KOK)
            if not current_doc['bemorlar']:
                print("Navbatda bemor yo‘q.")
            else:
                for i, p in enumerate(current_doc['bemorlar'], 1):
                    print(f"{i}. {p['name']} | Tel: {p['phone']} | Vaqt: {p['time']}")
            input("\nOrqaga qaytish uchun Enter...")

        elif choice == "2":
            if not current_doc['bemorlar']:
                print_color("Bemor yo‘q!", QIZIL)
                wait(1.5)
            else:
                patient = current_doc['bemorlar'][0]
                print(f"{patient['name']} ko‘rikka kiryapti...")
                wait(2)
                current_doc['bemorlar'].pop(0)
                save_json("doctors.json", doctors_db)
                print_color("Ko‘rik tugadi!", YASHIL)
                wait(1.5)

        elif choice == "0":
            break

        else:
            print_color("Noto‘g‘ri tanlov!", QIZIL)
            wait(1)






def show_user_card(phone):
    clear()
    if phone not in users_db:
        print_color("Foydalanuvchi topilmadi!", QIZIL)
        input("\nOrqaga qaytish uchun Enter...")
        return

    usr = users_db[phone]
    print_color(f"--- {usr.get('name','No-name')}NING TIBBIY KARTASI ---", KOK)

    if not usr.get("history"):
        print("Siz hali hech qaysi shifokorga murojaat qilmagansiz.")
        input("\nOrqaga qaytish uchun Enter...")
        return

    for i, h in enumerate(usr["history"], 1):
        print(f"{i}. Shifokor: {h['doctor']} | Mutaxassislik: {h['type']} | Sana: {h['time']}")

    input("\nOrqaga qaytish uchun Enter...")




def user_panel(phone):
    current_user = users_db[phone]

    while True:
        clear()
        print_color(f"--- FOYDALANUVCHI PANELI: {current_user['name']} ---", SARIQ)
        print("1. Ma'lumotlarim")
        print("2. Shifokor qabuliga yozilish")
        print("3. Mening kartam")
        print("0. Chiqish")

        choice = input("\nTanlov: ")

        if choice == "1":
            clear()
            print_color("--- MA'LUMOTLAR ---", KOK)
            print(f"Ism: {current_user['name']}")
            print(f"Yosh: {current_user['age']}")
            print(f"Telefon: {phone}")
            input("\nOrqaga qaytish uchun Enter...")

        elif choice == "2":
            clear()
            print_color("--- SHIFOKORLAR ---", KOK)

            for idd, d in doctors_db.items():
                print(f"ID: {idd} | {d['name']} | {d['type']}")

            print("\n0. Orqaga")

            doc_choice = input("\nShifokor ID: ")

            if doc_choice == "0":
                continue

            if doc_choice not in doctors_db:
                print_color("Bunday shifokor yo‘q!", QIZIL)
                wait(1.5)
                continue

            doc = doctors_db[doc_choice]

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            doc['bemorlar'].append({
                'name': current_user['name'],
                'phone': phone,
                'time': timestamp
            })

           
            if "history" not in current_user:
                current_user["history"] = []

            current_user["history"].append({
                'doctor': doc['name'],
                'type': doc['type'],
                'time': timestamp
            })

            save_json("doctors.json", doctors_db)
            save_json("users.json", users_db)

            print_color(f"{doc['name']} qabuliga yozildingiz!", YASHIL)
            wait(2)

        elif choice == "3":
            show_user_card(phone)

        elif choice == "0":
            break

        else:
            print_color("Noto'g'ri tanlov!", QIZIL)
            wait(1)





def login(user_type):
    clear()

    if user_type == "admin":
        print_color("--- ADMIN KIRISH ---", SARIQ)
        u = input("Login: ")
        p = input("Parol: ")

        if u == admin_db.get('username') and p == admin_db.get('password'):
            admin_panel()
        else:
            print_color("Login yoki parol noto‘g‘ri!", QIZIL)
            wait(1.5)


    elif user_type == "doctor":
        print_color("--- SHIFOKOR KIRISH ---", SARIQ)
        username = input("Login: ")
        password = input("Parol: ")

        if username in doctors_db and doctors_db[username]['password'] == password:
            doctor_panel(username)
        else:
            print_color("Login yoki parol noto‘g‘ri!", QIZIL)
            wait(1.5)


    elif user_type == "user":
        print_color("--- FOYDALANUVCHI ---", SARIQ)
        phone = input("Telefon (+998...): ")

        if phone not in users_db:
            print_color("Ro‘yxatdan o‘tish:", KOK)
            name = input("Ism-familiya: ")
            age = input("Yosh: ")
            password = input("Parol: ")

            users_db[phone] = {
                'name': name,
                'age': age,
                'password': password,
                'blocked': False,
                'history': []
            }

            save_json("users.json", users_db)
            print_color("Ro‘yxatdan o‘tildi!", YASHIL)
            wait(1.5)
            user_panel(phone)

        else:
            if users_db[phone].get("blocked"):
                print_color("Profilingiz bloklangan!", QIZIL)
                wait(2)
                return

            password = input("Parol: ")

            if password == users_db[phone]["password"]:
                user_panel(phone)
            else:
                print_color("Parol noto‘g‘ri!", QIZIL)
                wait(2)


while True:
    clear()
    print_color("=== SHIFOXONA TIZIMI ===", KOK)
    print("1. Admin sifatida kirish")
    print("2. Shifokor sifatida kirish")
    print("3. Foydalanuvchi sifatida kirish")
    print("0. Chiqish")

    c = input("\nTanlov: ")

    if c == "1":
        login("admin")
    elif c == "2":
        login("doctor")
    elif c == "3":
        login("user")
    elif c == "0":
        print_color("Dastur to‘xtatildi.", YASHIL)
        break
    else:
        print_color("Noto‘g‘ri tanlov!", QIZIL)
        wait(1)
