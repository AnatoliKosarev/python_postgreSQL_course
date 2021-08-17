from database import add_entry, get_entry, create_table, search_for_entry

message = """Please select one of the following options:
1. Add new entry for today.
2. View entries.
3. Search for entry by date.
4. Exit.

Your selection: """

welcome_message = """Welcome to the programming diary.
-------------------------------"""


def prompt_new_entry():
    user_entry_content = input("Please enter what have you learned today: ")
    user_entry_date = input("Please enter entry date: ")
    add_entry(user_entry_content, user_entry_date)


def view_entries(entries):
    if (row := entries.fetchone()) is None:
        print("No entries found.")
    else:
        print(f"{row['date']}\n{row['content']}\n")  # print fetched row first, because it's not in entries anymore
        for entry in entries:
            print(f"{entry['date']}\n{entry['content']}\n")


def prompt_search_by_date():
    user_search_date = input("Please enter entry date: ")
    view_entries(search_for_entry(user_search_date))


print(welcome_message)
create_table()

while (user_selection := input(message)) != "4":
    if user_selection == "1":
        prompt_new_entry()
    elif user_selection == "2":
        view_entries(get_entry())
    elif user_selection == "3":
        prompt_search_by_date()
    else:
        print("Invalid option, please try again!")