#!/usr/bin/python
import sys
try:
    import argparse
except ImportError:
    sys.exit('Silahkan install `python-argparse` atau gunakan python >= 2.7 untuk menjalankan script ini')
import os, re, urllib2, json
ver = '1.0.4'
prog_desc = "Simple Kominfo Trust / Internet Positif db fetcher written in Python"
base_url = 'http://trustpositif.kominfo.go.id/files/downloads/index.php'
path_lists = 'path.json'
dl_dir = 'RAW_DATA'
clean_data = 'DATA'
cnf_dir = 'conf'

def halo() :
    print "\n" + "-+-"*23 + "\n\tPython Kominfo Trust / Intetnet Positif Fetcher " + str(ver)
    print "\t" + prog_desc
    print "\tby ditatompel <svcadm@ditatompel.com> <christian.dita@wds.co.id>"
    print "-+-"*23+"\n"

def clean_domain(government):
    validate_ip = re.compile("^(\*\.)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    for censorship in government.keys():
        dir_location = dl_dir + '/' + censorship + '/'
        if os.path.isdir(dir_location):
            for filename in os.listdir(dir_location):
                lines_seen = set()
                if not os.path.exists(os.path.dirname(clean_data + '/' + censorship + '/')):
                    os.makedirs(os.path.dirname(clean_data + '/' + censorship + '/'))
                outfile = open(clean_data + '/' + censorship + '/' + filename, "wb")
                outfile.write('')
                for line in open(dir_location + filename, "rb"):
                    # added .replace(' ', "\n") because kominfo source data contain 2 domains in 1 line -_-"
                    line = line.strip().replace("\r", '').replace(' ', "\n")
                    # discard invalid domain like shesafreak. , ladyboynancy. or invalid wildcard ip addr like *.200.10.104.174
                    if line.endswith('.\n') or validate_ip.match(line):
                        print 'Domain / alamat IP tidak valid ditemukan : ' + line
                    else:
                        if line not in lines_seen:
                            outfile.write(line + "\n")
                            lines_seen.add(line)
                        else:
                            print 'Data kembar ditemukan : ' + line
                outfile.close()
        else:
            print 'Direktori ' + dir_location + ' tidak ditemukan'

def fetch_data(government):
    for censorship in government.keys():
        fetch_link = urllib2.urlopen(base_url + "?dir=" + government[censorship])
        raw_html = fetch_link.read()
        links = re.findall('href=".*dlf/unknown', raw_html)
        for link in links:
            link = re.findall('\?dir.*" class=', link)
            link = link[0].replace('" class=', '')
            print "Mengunduh " + base_url + link
            stream = urllib2.urlopen(base_url + link)
            domain_data = stream.read()
            files = link.split('=')
            save_to = dl_dir + '/' + censorship + '/' + files[2] + '.txt'
            if not os.path.exists(os.path.dirname(save_to)):
                os.makedirs(os.path.dirname(save_to))
            with open(save_to, "wb") as db:
                db.write(domain_data)

def generate_named(government, ns, email, domain):
    if not os.path.exists(os.path.dirname(cnf_dir + '/')):
        os.makedirs(os.path.dirname(cnf_dir + '/'))
    head = """
$TTL 86400      ; 1 day
@   IN      SOA %s. %s. (
                                2017040503 ; serial
                                3600       ; refresh (1 hour)
                                120        ; retry (2 minute)
                                604800     ; expire (1 week)
                                86400      ; minimum (1 day)
                                )
        IN      NS      %s.
""" % (ns, email, ns)
    print 'Memproses pembuatan config BIND...'
    # found *.{ipaddr} on blacklist. definitely not valid
    ipaddr_regex = re.compile("^(\*\.)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    for censorship in government.keys():
        dir_location = clean_data + '/' + censorship + '/'
        if os.path.isdir(dir_location):
            for filename in os.listdir(dir_location):
                if filename == 'domains.txt':
                    outfile = open(cnf_dir + '/' + censorship + '_named.conf', "wb")
                    outfile.write(head)
                    for line in open(dir_location + filename, "rb"):
                        record = line.replace("\r",'').replace("\n", '')
                        # blocking the entry ip address is not wise sir!
                        # remove if condition below if you want to include the ip addresses!
                        # don't forget to fix indentation if you remove if condition below!
                        if not ipaddr_regex.match(record):
                            outfile.write(record + " IN CNAME " + domain + ".\n")
                    outfile.close()
        else:
            print 'Direktori ' + dir_location + ' tidak ditemukan'

if __name__ == "__main__":
    if not os.path.isfile(path_lists):
        sys.exit('file ' + path_lists + ' tidak ditemukan. Kunjungi https://github.com/ditatompel/Katanya-Internet-Positif')
    nameserver = 'localhost.local'
    email = 'administrator.localhost.local'
    dest_domain = 'internetbaik.wds.co.id'

    opts = argparse.ArgumentParser(
        description=prog_desc,
        epilog="Contoh: python ./" + sys.argv[0] + " -cfg -n ns.domain.com -e admin.domain.com -d blokir.domain.com")
    opts.add_argument("-f", "--fetch", dest="fetch", action="store_true", help="Ambil data blacklist dari trustpositif.kominfo.go.id")
    opts.add_argument("-c", "--clean", dest="clean", action="store_true", help="Bersihkan duplikasi data dari trustpositif.kominfo.go.id")
    opts.add_argument("-g", "--generate", dest="generate", action="store_true", help="Buat file zone file untuk BIND (BIND zone file generator)")
    group = opts.add_argument_group('Opsi tambahan untuk BIND zone file generator')
    group.add_argument("-n", "--nameserver", dest="nameserver", help="Nameserver option, default : " + nameserver)
    group.add_argument("-e", "--email", dest="email", help="Email option, default : " + email)
    group.add_argument("-d", "--domain", dest="domain", help="CNAME domain tujuan. Default " + dest_domain)
    options = opts.parse_args()

    show_help = True
    with open(path_lists) as source:
        government = json.load(source)
    if options.fetch:
        fetch_data(government)
        show_help = False
    if options.clean:
        clean_domain(government)
        show_help = False
    if options.generate:
        if options.nameserver:
            nameserver = options.nameserver
        if options.email:
            email = options.email
        if options.domain:
            dest_domain = options.domain
        generate_named(government, nameserver, email, dest_domain)
        show_help = False
    if show_help:
        halo()
        opts.print_help()
