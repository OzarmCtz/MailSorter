import colorama
from colorama import Fore
import os
import re
import shutil
from collections import defaultdict

# Initialiser Colorama
colorama.init()

graf = r"""
  __  __       _ _    _____            _            
 |  \/  |     (_) |  / ____|          | |           
 | \  / | __ _ _| | | (___   ___  _ __| |_ ___ _ __ 
 | |\/| |/ _` | | |  \___ \ / _ \| '__| __/ _ \ '__|
 | |  | | (_| | | |  ____) | (_) | |  | ||  __/ |   
 |_|  |_|\__,_|_|_| |_____/ \___/|_|   \__\___|_|   
"""


print(Fore.LIGHTYELLOW_EX + graf + "\n")
print("[+] Version 2.0  \n")



def extract_domain(email):
    match = re.search(r"@([\w.]+)", email)
    if match:
        return match.group(1)
    return None


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def clean_email_file(file_path):
    temp_file = "temp.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        valid_emails = []

        for line in lines:
            emails_in_line = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line)
            valid_emails.extend(emails_in_line)

        with open(temp_file, "w", encoding="utf-8") as file:
            file.write("\n".join(valid_emails))
        os.replace(temp_file, file_path)
        print(Fore.GREEN + "The file has been cleaned successfully." + Fore.RESET)
        return True
    except Exception as e:
        print(Fore.RED + f"An error occurred while cleaning the file: {e}" + Fore.RESET)
        return False

    
def display_folder_line_counts(folder_path):
    file_info = defaultdict(int)

    for entry in os.scandir(folder_path):
        if entry.is_file():
            try:
                with open(entry.path, "r") as file_obj:
                    lines = file_obj.readlines()
                line_count = len(lines)
                file_info[entry.name] = line_count
            except Exception as e:
                print(Fore.RED + f"Error occurred while reading the file {entry.name}: {e}" + Fore.RESET)

    # Sort files by line count (from largest to smallest)
    sorted_file_info = sorted(file_info.items(), key=lambda x: x[1], reverse=True)

    # Display files and line counts
    for file, line_count in sorted_file_info:
        filename = os.path.splitext(file)[0]  # Remove the file extension
        print(Fore.MAGENTA + f" [*]  {filename}: [{line_count}] mail founded." + Fore.RESET)
        
        
def remove_empty_lines_in_random_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
        with open(file_path, "w") as file:
            file.write("\n".join(lines))
    except Exception as e:
        print(Fore.RED + f"Error occurred while removing empty lines: {e}" + Fore.RESET)


def process_email_list(file_path, result_folder, maxi):
    emails_by_domain = defaultdict(list)
    random_emails = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                email = line.strip()

                if not validate_email(email):
                    print(f"\033[91m [-] {email} Invalid! [incorrect]\033[0m")
                    continue

                domain = extract_domain(email)
                if domain:
                    emails_by_domain[domain].append(email)
                else:
                    random_emails.append(email)

        # Create result folder
        os.makedirs(result_folder, exist_ok=True)

        for domain, emails in emails_by_domain.items():
            if len(emails) >= int(maxi):
                domain_file_path = os.path.join(result_folder, f"{domain}.txt")
                with open(domain_file_path, "a") as domain_file:
                    domain_file.write("\n".join(emails) + "\n")

        random_file_path = os.path.join(result_folder, "random.txt")
        with open(random_file_path, "a") as random_file:
            random_file.write("\n".join(random_emails) + "\n")

        # Remove empty lines in random file
        remove_empty_lines_in_random_file(random_file_path)

        # Display the results
        display_folder_line_counts(result_folder)

        total_lines = sum(1 for _ in open(file_path))
        result_lines = sum(1 for _ in open(random_file_path))
        random_lines = total_lines - result_lines


        input(Fore.RED + "\n\n [x] Press to exit ..." + Fore.RESET)

    except Exception as e:
        print(Fore.RED + f"Une erreur s'est produite lors du traitement des e-mails : {e}" + Fore.RESET)
        return



file_path = input(Fore.LIGHTYELLOW_EX + "Enter the file path: " + Fore.RESET)
while not os.path.isfile(file_path):
    print(Fore.RED + "The specified file does not exist. Please try again." + Fore.RESET)
    file_path = input(Fore.LIGHTYELLOW_EX + "Enter the mail list path: " + Fore.RESET)

result_folder = input(Fore.LIGHTYELLOW_EX + "Enter the name of the result folder: " + Fore.RESET)
while os.path.exists(result_folder):
    choice = input(
        Fore.RED + "The folder name already exists. Are you sure you want to overwrite it? (y/n): " + Fore.RESET)
    if choice == "y":
        shutil.rmtree(result_folder)
        break
    elif choice == "n":
        result_folder = input(Fore.LIGHTYELLOW_EX + "Enter a new folder name: " + Fore.RESET)
    else:
        print(Fore.RED + "I didn't understand. Please choose between 'y' and 'n'." + Fore.RESET)

maxi = input(Fore.LIGHTYELLOW_EX + "Enter the minimum number of emails required to create a domain file: " + Fore.RESET)
while not maxi.isdigit():
    print(Fore.RED + "Please enter a valid number." + Fore.RESET)
    maxi = input(Fore.LIGHTYELLOW_EX + "Enter the minimum number of emails required to create a domain file: " + Fore.RESET)

# Clean the file before displaying and sorting the emails
if clean_email_file(file_path):
    process_email_list(file_path, result_folder, maxi)
else:
    print(Fore.RED + "Unable to continue the script due to an error during file cleaning." + Fore.RESET)
