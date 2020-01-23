#!/usr/bin/env python3

"""PY210_SP - mailroom part 2 - no dict switch, yet
author: Nick Miller"""

import sys

# new example database

donor_db = {
    "Jeff Staple": [20, 20],
    "Takashi Murakami": [10.50],
    "Virgil Abloh": [300, 40.33, 5.35],
    "Jan Chipchase": [1001.23, 400.87, 102]
}


def letter_prep(ver, db):
    """
    takes user input (name)
    :param ver: name (sanitized before being passed)
    :param db: a dict of donors and their donations
    :return: a list of their full name, first name, all donations, and a total
    """
    namer = ver.split(" ")
    firster = namer[0]
    monies = db[ver.title()]
    toters = sum(monies)
    toters = float(f"{toters:.2f}")
    return [namer, firster, monies, toters]


def letter_format(firster, toters):
    """
    takes in first name and totals and returns formatted Thank You message
    :param firster: first name, sanitized before passing
    :param toters: sum of donations, sanitized before passing
    :return: formatted, faux-personalized Thank You message
    """
    letter = ('\n'.join(['', 'Dearest {first_name},', '', 'Thank you for your generous support!',
                             'We appreciate your donation(s), which total ${donats:.2f} to date!', '',
                             'Sincerest regards,',
                             '',
                             'The Foundation'])).format(first_name=firster, donats=toters)
    return letter


def one_thanks(db=donor_db):
    """
    this whole thing needs re-tooled to work with the new dict-based db
    :param db: dictionary-based database of donors(key) and their donations(values)
    :return: thanks for a donation
    """
    thanks_c = str(input("Enter a name or type 'list': "))
    thanks_c = thanks_c.lower()
    if thanks_c.strip() == "list":
        for item in donor_db:
            print(item)
    elif thanks_c.strip().lower() == "q":
        return
    elif thanks_c.title() not in donor_db.keys():
        add_q = str(input("That name is not in the list, would you like to add it? (y/n): "))
        add_q = add_q.lower()
        if add_q.strip() == "q":
            return
        if add_q.strip() == "n":
            return
        if add_q.strip() == "y":
            print("Adding", thanks_c.title(), "to the donor list.")
            add_y = input("Please enter their donation amount: ")
            if add_y.lower().strip() == "q":
                return
            else:
                while True:
                    try:
                        add_y = float(add_y)
                        break
                    except ValueError:
                        print("Sorry, that is not a valid amount. ")
                add_y_f = f"{add_y:.2f}"
                thanks_c = thanks_c.title()
                print("Adding " + thanks_c + "'s donation of $" + add_y_f, "to their db entry")
                add_y_l = [add_y]
                donor_db[thanks_c] = add_y_l
                firster = letter_prep(thanks_c, donor_db)[1]
                toters = letter_prep(thanks_c, donor_db)[3]
                letter = letter_format(firster, toters)
                print("Here is your Thank You:")
                print(letter)
    elif thanks_c.title() in donor_db.keys():
        in_list = str(input("That name is in the list, would you like to add a new donation to it? (y/n): "))
        while in_list != "y" and in_list != "n" and in_list != "q":
            in_list = input("Please enter y or n: ").lower()
        if in_list == "q":
            return
        if in_list == "n":
            next_q = str(input("Do you still want to send a Thank You? (y/n): "))
            while next_q != "y" and next_q != "n" and next_q != "q":
                next_q = input("Please enter y or n: ").lower()
            if next_q == "n":
                pass
            if next_q == "q":
                return
            elif next_q == "y":
                firster = letter_prep(thanks_c, donor_db)[1]
                toters = letter_prep(thanks_c, donor_db)[3]
                letter = letter_format(firster, toters)
                print(letter)
        elif in_list == "y":
            donats = donor_db[thanks_c.title()]
            while True:
                try:
                    add_donats = input("Add a donation amount: ")
                    if add_donats.strip().lower() == "q":
                        return
                    else:
                        add_donats = float(add_donats)
                        donats.append(add_donats)
                        break
                except ValueError:
                    print("Sorry, that is not a valid amount. ")
        firster = letter_prep(thanks_c, donor_db)[1]
        toters = letter_prep(thanks_c, donor_db)[3]
        letter = letter_format(firster, toters)
        print("Here is your Thank You:")
        print(letter)


def thanks_all(db=donor_db):
    """
    given a donor db, write thank-you files for each donor
    :param db: dictionary-based database of donors(key) and their donations(values)
    :return: a text file thank you for each donor
    """
    for donor in donor_db:
        firster = letter_prep(donor, donor_db)[1]
        toters = letter_prep(donor, donor_db)[3]
        letter_text = letter_format(firster, toters)
        file_name = donor.lower().replace(" ", "") + ".txt"
        letter_text = letter_format(firster, toters)
        save_file(file_name, letter_text)
    print("Individual Thank You files for each donor have been created in the same directory\n"
          "in which this programs lives/runs.")


def save_file(file_name, letter_text):
    """
    borrowed from a totally diff assignment, needs re-tooled to save files for donation thank-yous
    :param file_name: name for file to be written
    :param letter_text: formatted text to be written to file
    :return: text file with Thank You letter
    """
    f = open(file_name, "w+")
    f.write(letter_text)
    f.close()


def report_sort_key(item):
    """
    defines a sorting key for database, stolen for part 1, might need fixed for proper dict sorting
    :param item: an index-able thing
    :return: returns index item 1 as the key to sort by
    """
    return item[1]


def report(db=donor_db):
    """
    this functions takes in a donor database and returns a formatted report
    :param db: input database, a dict of donor: donations
    :return: formatted report, based on db data; sum of donations, total num of donations, average donation/name
    """
    report_don = []
    for key in db:
        name = key
        donations = db[name]
        totes = sum(donations)
        nums = len(donations)
        aves = totes / nums
        report_don.append((name, totes, nums, aves))

    report_don.sort(key=report_sort_key, reverse=True)

    key = ["name", "total given", "num gifts", "average gift"]
    separator = "|"

    print(f"{key[0]:<18}",
          f"{separator:^3}",
          f"{key[1]:^18}",
          f"{separator:^3}",
          f"{key[2]:^10}",
          f"{separator:^3}",
          f"{key[3]:>15}")
    print("-" * 76)
    for row in report_don:
        print("{:<18s}   {:>15.2f}   {:12d}   {:>20.2f}".format(*row))


def quit_prog():
    """
    used to trigger program quit
    :return: ends program
    """
    print("Quitting - See you next time.")
    sys.exit()


def main():
    """
    Main menu function
    :return: navigates into menu option functions; q exits back to this menu
    """
    while True:
        print("""
        Menu of Options
        1) Send a 'Thank You' to a single donor
        2) Send 'Thank You' letters to all donors
        3) Create a Report
        4) Exit Program
        """)
        usrchoice = str(input("Which option would you like to perform? [1 to 4]: "))
        print()

        if usrchoice.strip() == '1':
            one_thanks()

        elif usrchoice.strip() == '2':
            thanks_all()

        elif usrchoice.strip() == '3':
            report()

        elif usrchoice.strip() == '4':
            quit_prog()

        elif usrchoice.strip() == 'q':
            quit_prog()

        else:
            print("sorry, that's not a valid option")


main()