# supplier2opens.py

**Created by**: Aiden Olsen

supplier2opens is a python script that allows the automatic conversion from
different supplier lists/carts to the OPEnS shopping list format saving lost of time.

The program takes in a csv or excel spreadsheet containing the necessary information
required for the OPEnS shopping list. The script then organized the data correctly
and copies the formatted contents to you clipboard to be easily pasted into the OPEnS
shopping list.

Currently the following suppliers lists/carts are supported:

- [Digi-Key](https://www.digikey.com/) Lists
- [Mouser](https://www.mouser.com/) Shopping Carts

## 🎥 Demo:

This following demo walks you through how to process a digikey list.

<img src="./examples/demo.gif" width=600>

## ⚙️  Installation Instructions:

```bash
git clone https://github.com/OPEnSLab-OSU/supplier2opens
cd supplier2opens
python3 -m venv venv
source venv/bin/activate # see table below to for other os/shells
pip install -r requirements.txt
```

| **Platform** |   **Shell**  | **Command to activate virtual environment** |
|:------------:|:------------:|:-------------------------------------------:|
| POSIX        | _bash/zsh_   | $ source <venv>/bin/activate                |
|              | _fish_       | $ source <venv>/bin/activate.fish           |
|              | _csh/tcsh_   | $ source <venv>/bin/activate.csh            |
|              | _PowerShell_ | $ <venv>/bin/Activate.ps1                   |
| Windows      | _cmd.exe_    | C:\> <venv>\Scripts\activate.bat            |
|              | _PowerShell_ | PS C:\> <venv>\Scripts\Activate.ps1         |

## ⚡️ Usage:

### Digi-Key list conversion:

Digi-Key allows you to to create lists of components and is a really handy
was to organize components for PCBs. Follow the instructions below to export
the file required for the script.

1. Open your digikey list `Account & Lists > Lists` and select the desired list
2. Download the csv by clicking `Download` and changing the export format to `CSV`
3. Run the following command: `python supplier2opens.py <path-to-csv>`

### Mouser shopping cart conversion:

Mouser allows users to export shopping cart contents, however it is formatted
differently than the OPEnS shopping list. Follow the steps below to export the
excel sheet required for processing.

1. Open your cart `Cart > View Cart`
2. Export the cart to excel `Export > To Excel`
3. Run the following command: `python supplier2opens.py <path-to-xls>`
