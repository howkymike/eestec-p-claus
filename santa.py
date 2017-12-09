from random import randint
import argparse as ap
import csv
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

def list_without(li, i):
    li_copy = list(li)
    if i in li:
        li_copy.remove(i)

    return li_copy


def gender():
    


def deliver_gift(row):
    # Create the container (outer) email message
    msg = EmailMessage()
    msg['Subject'] = 'EESTECowy Mikołaj'
    msg['From'] = 'mikolaj@eestec.xxx.pl'
    msg['To'] = row[2]

    yolo = make_msgid()
    msg.add_alternative("<html><head></head><body>"
                        "Cześć!<br/><br/>" + \
                        "W tym roku będziesz mikołajem dla: <b>" + row[3] + " " + row[4] + "</b>." + \
                        "<br/><br/>" + \
                        "Możesz inspirować się Jej/Jego wishlistą: <br/>" + row[6] + \
                        "<br/><br/>" + \
                        "<img src=\"cid:{yolo}\" \>"
                        "</body></html>".format(yolo=yolo[1:-1]), subtype='html')
    if row[3][-1] == "a":
        print("cebula")
    with open("mikolaj.jpg", 'rb') as img:
        msg.get_payload()[0].add_related(img.read(), 'image', 'jpg', cid=yolo)

    # Send the email via our own SMTP server
    s = smtplib.SMTP('mail3.mydevil.net', 587)
    s.login('prawilny.mikolaj@eestec.pl', '9vS4FjIetp9QUJQQ379W')
    s.send_message(msg)
    s.quit()

    with open('delivered_asbestos', 'a') as f:
        f.write('Email about gift send to ' + row[2] + "\n")
    f.close()


def miki_algo(n):
    people = [i for i in range(n)]
    gift_waiters = list(people)
    relations = []

    if n > 1:
        for i in range(n):
            people_prim = list_without(gift_waiters, people[i])

            if len(people_prim) != 0:
                r = randint(0, len(people_prim) - 1)
                relations.append([people[i], people_prim[r]])
                gift_waiters = list_without(gift_waiters, people_prim[r])
            else:
                r = randint(0, len(relations) - 1)
                relations.append([people[i], relations[r][1]])
                relations[r][1] = people[i]

    return relations


def gen_output(fn, delim, quotechar, header):
    header_arr, people, gift_waiters, n = read_csv(fn, delim=delim, quotechar=quotechar, header=header)
    mapping = miki_algo(n)
    output_arr = []

    for i, j in mapping:
        output_arr.append(people[i] + gift_waiters[j])

    for row in output_arr:
        deliver_gift(row)


def read_csv(fn, delim=',', quotechar='"', header=True):
    people = []
    gift_waiters = []
    header_arr = []
    n = 0

    with open(fn, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delim, quotechar=quotechar)

        for i, row in enumerate(spamreader):
            if len(row) < 2:
                raise Exception('Za mało kolumn')

            if header and i == 0:
                header_arr = row
            else:
                n += 1
                people.append(row[:3])
                gift_waiters.append(row)

        return header_arr, people, gift_waiters, n


def write_csv(output, fn, delim=',', quotechar='"'):

    with open(fn, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=delim,
                                quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)

        for row in output:
            spamwriter.writerow(row)


if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Program "miki" przyjmuje plik csv z imionami i nazwiskami osób,'
                                           ' i na jego podstawie generuje drugi plik csv'
                                           ' wraz z przyporządkowanymi mikołajami.\n'
                                           'Pamiętaj proszę o poprawnym formatowaniu pliku csv. '
                                           'Plik wynikowy ma takie same ustawienia jak plik wejściowy.\n\n'
                                           'Domyślne ustawienia:\n'
                                           '\t- symbol separatora kolumn: ,\n'
                                           '\t- symbol separatora tekstu: "\n'
                                           '\t- plik zawiera nagłówek: tak\n'
                                           '\t- nazwa pliku wynikowego: miki.csv\n'
                                           'Wszystkie powyższe ustawienia można zmienić.\n\n'
                                           '\tPrzykładowe wywołanie: miki.py osoby.csv -o osoby-miki.csv',
                               formatter_class=ap.RawTextHelpFormatter)

    parser.add_argument("filename", help="Filename")
    # parser.add_argument("-o", "--output", default='miki.csv', type=str, help="Nazwa pliku wynikowego")
    parser.add_argument("-d", "--delimeter", default=',', type=str, help="Separator")
    parser.add_argument("-q", "--quotechar", default='"', type=str, help="Symbol cudzysłowia")
    parser.add_argument('-n', '--noheader', help='Plik csv nie zawiera nagłówka', action='store_true')

    args = parser.parse_args()

    gen_output(args.filename, args.delimeter, args.quotechar, not args.noheader)
