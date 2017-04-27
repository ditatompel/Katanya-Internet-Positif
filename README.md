# Katanya Internet Positif
[![license](https://img.shields.io/github/license/ditatompel/Katanya-Internet-Positif.svg)](LICENSE)
[![Website](https://img.shields.io/website-up-down-green-red/http/trustpositif.kominfo.go.id.svg)](http://trustpositif.kominfo.go.id)

`Katanya Internet Positif` adalah script sederhana untuk mengambil data blacklist dari trustpositif.kominfo.go.id, melakukan filterisasi kembali untuk duplikasi domain atau alamat wildcard IP yang tidak valid, dan melakukan convert untuk konfigurasi BIND DNS zone blacklist. Untuk informasi lebih lanjut, baca [halaman Wiki](https://github.com/ditatompel/Katanya-Internet-Positif/wiki).

## Petunjuk Penggunaan
Script ini dapat dijalankan menggunakan Python 2.7 atau lebih.

Untuk yang masih menggunakan Python 2.6, masih dapat menjalankan script ini
dengan menginstall `python-argparse` sebagai module tambahan.

### 1st run / update RAW_DATA
Untuk yang **pertama kali menjalankan script ini** (atau ingin melakukan update RAW_DATA), gunakan opsi `-f` atau `--fetch` untuk
mengambil RAW_DATA dari trustpositif.kominfo.go.id

    $ python ./internetpositif.py --fetch

### Bersihkan duplikasi Data / list alamat IP yang tidak valid
Untuk membersihkan duplikasi data, menghapus alamat IP yang tidak valid, gunakan opsi `-c` atau `--clean`

    $ python ./internetpositif.py -c

### BIND zone file generator
Untuk membuat konfigurasi BIND blacklist zone, gunakan opsi `-g` atau `--generate` dengan opsi tambahan `-n` / `--nameserver`, `-e` / `--email`, `-d` / `--domain`

Misalnya :

    $ python ./internetpositif.py --generate -n ns.domain.com -e admin.domain.com -d blokir.domain.com
akan menghasilkan file :

    $TTL 86400      ; 1 day
    @   IN      SOA ns.domain.com. admin.domain.com. (
                                    2017040503 ; serial
                                    3600       ; refresh (1 hour)
                                    120        ; retry (2 minute)
                                    604800     ; expire (1 week)
                                    86400      ; minimum (1 day)
                                    )
            IN      NS      ns.domain.com.
    domain.yang.diblokir.com IN CNAME blokir.domain.com.
    domain.lainnya.yang.diblokir.net IN CNAME blokir.domain.com.
    [dan seterusnya]

### Jalankan semua dalam 1 baris
    $ python ./internetpositif.py -cfg -n=ns.domain.com --email=admin.domain.com -d blokir.domain.com

### Default value
Opsi tertentu memiliki default value, seperti :
* `-n` / `--nameserver` = `localhost.local`
* `-e` / `--email` = `administrator.localhost.local`
* `-d` / `--domain` = `internetbaik.wds.co.id`

Informasi lebih lanjut

    $ python ./internetpositif.py

    -h, --help            show this help message and exit
    -f, --fetch           Ambil data blacklist dari trustpositif.kominfo.go.id
    -c, --clean           Bersihkan duplikasi data dari
                        trustpositif.kominfo.go.id
    -g, --generate        Buat file zone file untuk BIND (BIND zone file
                        generator)

    Opsi tambahan untuk BIND zone file generator:
    -n NAMESERVER, --nameserver NAMESERVER
                        Nameserver option, default : localhost.local
    -e EMAIL, --email EMAIL
                        Email option, default : administrator.localhost.local
    -d DOMAIN, --domain DOMAIN
                        CNAME domain tujuan. Default internetbaik.wds.co.id


## Struktur File
Script akan membuat folder tertentu sesuai dengan opsi perintah yang diberikan.

| Perintah | Alias | Folder | Keterangan |
|---|---|---|---|
| -f | --fetch | ./RAW_DATA/ | data asli yang didapat dari trustpositif.kominfo.go.id |
| -c | --clean | ./DATA/ | hasil list domain yang telah dibersihkan dari folder ./RAW_DATA/ |
| -g | --generate | ./conf/ | hasil convert named zone yang didapat dari folder ./DATA/ |

## Berkontribusi
Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk informasi lebih detail mengenai
cara berkontribusi pada repositori ini.

## Lisensi
[MIT License](LICENSE)
