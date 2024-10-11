![Screenshot 2024-10-11 075901](https://github.com/user-attachments/assets/4d92a107-3413-4d18-a3bd-4999400b4dd7)

# MailSorter

A Python script to sort and filter email addresses by domain from a provided email list file. This tool is designed to clean up email data and categorize it for better organization and management.

## Features

- Validates email addresses using regex.
- Extracts domains from valid email addresses.
- Cleans input files by removing invalid email addresses.
- Sorts valid emails by domain into separate text files.
- Stores any invalid or unclassified emails in a "random.txt" file.
- Displays a count of emails processed and sorted.

## Requirements

Before running the script, ensure you have Python installed on your machine. You can check your Python installation by running:

```bash
python --version
```

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OzarmCtz/MailSorter.git
   cd email_sorter
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare a text file containing the email addresses you want to sort, with one email address per line.

2. Run the script:

   ```bash
   python mail_sorter.py
   ```

3. Follow the prompts to input:
   - The path to your email list file.
   - The name of the result folder where sorted files will be stored.
   - The minimum number of emails required to create a domain-specific file.

## Example

```plaintext
Enter the file path: path/to/your/emails.txt
Enter the name of the result folder: sorted_emails
Enter the minimum number of emails required to create a domain file: 5
```

## Notes

- The script will clean the email list by removing any invalid addresses before sorting.
- The output will include separate files for each domain containing the respective emails, along with a `random.txt` file for unclassified emails.
- In case of any errors during execution, appropriate error messages will be displayed.
