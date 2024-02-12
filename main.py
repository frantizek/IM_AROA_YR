"""Imports needed to complete the script tasks."""
import os, errno, re, csv, requests
from bs4 import BeautifulSoup
from rich.progress import track
import my_file_validation
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
import itertools


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def export_to_pdf(data):
    c = canvas.Canvas("IM_AROA_YR.pdf", pagesize=(landscape(letter)))
    w, h = landscape(letter)
    max_rows_per_page = 27
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15

    xlist = [x + x_offset for x in [0, 110, 260, 490, 680]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]

    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()

    c.save()

def simple_validation(my_file) -> None:
    if (my_file_validation.file_exist(my_file) and
            my_file_validation.file_size(my_file) and
            my_file_validation.file_lines(my_file) and
            my_file_validation.file_format(my_file)):
        print("    - Validacion completada, continuando el procesamiento.")
    else:
        print("    - Falla en la validacion del archivo, revisa los ERRORES y/o ADVERTENCIAS.")


def silentremove(filename) -> None:
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred


def read_file(filename) -> list:
    """Open the file in read mode, returns the lines."""
    with open(filename, "r", encoding="utf-8") as this_file:
        lines = this_file.readlines()
    return lines


def search_telegram_user(user_name, dict_of_users):
    """Using the dictionary, return the link with the user."""
    if user_name in dict_of_users.keys():
        return dict_of_users[user_name].replace('@', '')
    else:
        return " "


def main():
    """Let's create the files with the guild members."""
    # Initializing the users dictionary
    d_users = {}
    swgoh_gg = True

    print("Recuerda: para procesar la informacion actualizada del gremio,")
    print("necesitamos sincronizar la pagina en https://swgoh.gg/")
    while swgoh_gg:
        _ = input("Presiona ENTER para continuar, una vez que hayas sincronizado la info del gremio.")
        swgoh_gg = False

    print("\n\nIniciando el proceso de generar los archivos con la informacion actualizada del gremio... ")

    # Since I do want to use a clean version it would be better 
    # if we delete the previous versions
    silentremove("gremio_aroa.csv")
    silentremove("IM_AROA_YR.md")
    silentremove("IM_AROA_YR.pdf")

    print("    - Se eliminaron las versiones anteriores de los archivos")

    if os.path.exists("IM_AROA_YR.txt"):
        filename = "IM_AROA_YR.txt"
        simple_validation(filename)
        lines = read_file(filename)
        print("    - Iniciando el proceso para las {} entradas en el archivo...\n\n\n".format(str(len(lines))))

        for _ in track(range(len(lines)), description='[cyan]    Combinando la informacion desde swgoh.gg y nuestro archivo de usuarios...\n'):

            for line in lines:
                user_data = line.strip().split(" ", 1)
                d_users[user_data[1].lower()] = user_data[0].lower()

            csv_header = ['Codigo de aliado', 'Usuario en SWGOH', 'Usuario en Telegram']
            data = [('Codigo de aliado', 'Usuario en SWGOH', 'Usuario en Telegram')]

            with open('gremio_aroa.csv', 'w', encoding="UTF8", newline='') as this_file:
                writer = csv.writer(this_file, delimiter=',')

                # write the header
                writer.writerow(csv_header)

                # This is the current url used at swgoh.gg for the guild
                # The page is usually refreshed so we will used to extract the guild members
                im_aroa_yr_url = "https://swgoh.gg/g/pTtJHHuYQcSMinxQXXZJgA/"

                page = requests.get(im_aroa_yr_url, timeout=10, verify=True)

                soup = BeautifulSoup(page.content, "html.parser")

                table = soup.find('table')

                acode_l = []
                uswgoh_l = []
                telegram_l = []
                message_me_l = []
                

                headers = [header.text for header in table.find_all('th')]
                results = [{headers[i]: cell for i, cell in enumerate(row.find_all('td'))}
                        for row in table.find_all('tr')]

                for result in results:
                    if "Name" in result.keys():
                        tag_converted_to_str = str(result['Name'])
                        username_swgoh = re.search(r'<div><strong>(.*?)</strong></div>',
                                                tag_converted_to_str).group(1)
                        allycode_swgoh = re.search(r'<a href="/p/(.*?)/">', tag_converted_to_str).group(1)
                        telegram = search_telegram_user(username_swgoh.lower(), d_users)

                        acode_l.append(allycode_swgoh)
                        uswgoh_l.append(username_swgoh)
                        telegram_l.append(telegram)
                        message_me_l.append(f"https://t.me/{telegram}")

                        # write the data
                        writer.writerow([allycode_swgoh, username_swgoh, telegram])
                        data.append((allycode_swgoh, username_swgoh, telegram))

            # close the file
            this_file.close()

            f = open("IM_AROA_YR.md", "w", encoding="utf-8")
            f.writelines(["# Imperio Mandaloriano Aroa'yr\n"])
            f.writelines(["\n| Codigo de aliado | Usuario en SWGOH | Enlace Perfil SWGOH | Usuario en Telegram | Mensaje Telegram |\n"])
            f.writelines(["|--- | ----:|:----|----:|:----|\n"])
            for guild_users in range(0, len(acode_l)):
                f.writelines([f"| {acode_l[guild_users]} |{uswgoh_l[guild_users]} | <a href=\"https://swgoh.gg/p/{acode_l[guild_users]}/\"><img src=\"images/icons8-swgoh-64.png\" alt=\"Perfil en swgoh.gg\" width=\"24\" height=\"24\" /></a> | {telegram_l[guild_users]} | <a href=\"{message_me_l[guild_users]}\"><img src=\"images/icons8-telegram-48.png\" alt=\"Mensaje por Telegram.\" width=\"24\" height=\"24\"  /></a> |\n"])
            f.writelines(["|  |  |  |   | |\n"])
            f.writelines(["\n\n\n\n"])

            f.writelines(["""

\n<div style="text-align: center;">
<a href=\"https://docs.google.com/spreadsheets/d/13gRpR_noZBz46L-uh9_pLAOHhXcOBPxBaGk6sxn92mc/edit?usp=sharing"><img src=\"images/Google_Sheets_2020_Logo.png\" alt=\"Usuarios\" height=\"24\" /></a>
<a href=\"https://docs.google.com/spreadsheets/d/13gRpR_noZBz46L-uh9_pLAOHhXcOBPxBaGk6sxn92mc/edit?usp=sharing">Enlace al archivo compartido en linea con los usuarios.</a>
</div>
                        """])

            f.close()

        export_to_pdf(data)

        print("\n\nHa terminado el proceso de generar los archivos.")
        print("¡SOMOS AROA'YR! \n\n")
    else:
        print("Error: el archivo que contiene los usuarios no existe o no puede leerse.")
        return 1



if __name__ == "__main__":
    main()
