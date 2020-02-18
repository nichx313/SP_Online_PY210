#!/usr/bin/env python3

"""PY210_SP - mailroom part 4 unit tests
author: Nick Miller"""

import os
import mailroom_pt4 as mail
from pathlib import Path

donor_db = {
    "Jeff Staple": [20, 20],
    "Takashi Murakami": [10.50],
    "Virgil Abloh": [300, 40.33, 5.35],
    "Jan Chipchase": [1001.23, 400.87, 102]
}

test_db = {
    "Donor One": [10, 10],
    "Donor Two": [0],
    "Donor Three": [10, 25.50]
}


def test_letter_prep():
    expected = ['jeff', 40.0]
    assert mail.letter_prep("jeff staple", donor_db) == expected
    expected2 = ['donor', 35.5]
    assert mail.letter_prep("donor three", test_db) == expected2


def test_letter_format():
    assert mail.letter_format("bob", 10) == ('\n'.join(['', 'Dearest bob,', '',
                             'Thank you for your generous support!',
                             'We appreciate your donation(s), which total $10.00 to date!', '',
                             'Sincerest regards,',
                             '',
                             'The Foundation']))


def test_thanks_all():
    mail.thanks_all(test_db)
    assert os.path.isfile("janchipchase.txt") is True
    assert os.path.isfile("jeffstaple.txt") is True
    assert os.path.isfile("takashimurakami.txt") is True


def test_save_file():
    mail.save_file("test.txt", "blah, blah")
    assert os.path.isfile("test.txt") is True
    expected = "blah, blah"
    assert Path('test.txt').read_text() == expected


def test_list_check():
    expected = "jeff staple"
    assert mail.list_check("jeff staple", donor_db) == expected
    expected2 = "not"
    assert mail.list_check("donor four", test_db) == expected2


def test_input_prep():
    test_str = "  HeLLo, HoW aRe YoU?  "
    expected = "hello, how are you?"
    assert mail.input_prep(test_str)


def test_input_check():
    expected = "list"
    assert mail.input_check("list") == expected
    expected2 = "y"
    assert mail.input_check("  Y") == expected2


def test_db_update():
    expected = None
    assert mail.db_update("donor four", 10, test_db) == expected


def test_report_sort_key():
    expected = 1
    assert mail.report_sort_key([0, 1]) == expected


def test_quit_prog():
    expected = "exit menu"
    assert mail.quit_prog() == expected
