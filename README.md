# Internet Positif Kominfo
[![Website](https://img.shields.io/website-up-down-green-red/http/trustpositif.kominfo.go.id.svg)](http://trustpositif.kominfo.go.id)
[![license](https://img.shields.io/github/license/ditatompel/Katanya-Internet-Positif.svg)]()

## Pendahuluan
    Anda sangat diundang untuk berpartisipasi dalam pengembangan terhadap basis
    data TRUST+™ Positif yang saat ini telah ada.
    - trustpositif.kominfo.go.id

Trust+ membagi data domain menjadi beberapa kategori :
* database
    * blacklist
        * kajian
        * pengaduan
    * whitelist
* db_porn

Dari list diatas, pada sisi `database/blacklist` terdapat kategori `pengaduan`
yang *mungkin* berasal dari pengaduan masyarakat. kategori pengaduan tersebut
berisi sejumlah file, antara lain :
* domains
* domain.b4.asterisk
* domain.old
* domain.save.[0-9]+
* dst.. (Mungkin ada yang bisa bantu **memperkenalkan** yang namanya *Revision
    Control System* atau *Version Control System* ;p)

Kemudian masih pada sisi `database/blacklist` terdapat kategori lain, yaitu
`kajian` yang banyak `ditafsirkan` sebagai hasil kajian oleh tim Trust+ dari
kategori `pengaduan` masyarakat.

Selanjuatnya ada lagi yang namanya `db_porn` yang **pastinya** merupakan list
domain-domain yang berbau pornografi.

Dan terakhir `database/whitelist` yang saat ini isinya (kosong ?)

### Banyaknya Duplikasi Data
Dari data blacklist `kajian` sendiri pun masih terdapat beberapa domain yang
double, misalnya domain sextubebdsm.com terdapat pada file
`database/blacklist/kajian/domains` line 1225 dan line 1229
##### Linux | GNU
`sort <FILE> | uniq -cd | sort -nr`
##### OSX | BSD
`sort <FILE> | uniq -c | grep -v '^ *1 ' | sort -nr`

### Domain tidak valid
Banyak domain yang terdapat pada list diatas yang tidak lagi valid. Misalnya
domain sudah habis, http service tidak dapat diakses, atau format domain yang
tidak valid.

Misalnya :
##### Tidak memiliki TLD
domain `shesafreak.` atau `ladyboynancy.` tidak memiliki TLD.
##### 2 buah domain pada 1 line
`db_porn/domains` line 900.
##### Wildcard alamat IP
Pemblokiran alamat IP mengunakan asterisk seperti `*.200.10.104.174` menjadikan alamat IP tidak valid.

Jika asal melakukan convert menggunakan cli. Misalnya :

`$ awk '{print $1" IN CNAME blokir.domain.com."}' domains >> /var/named/trust-positif.db`

Akan menjadi :

    [record zone lainnya]
    shesafreak. IN CNAME blokir.domain.com.
    ladyboynancy. IN CNAME blokir.domain.com.
    krucil.net adultjoy.net IN CNAME blokir.domain.com.
    [record zone lainnya]
Hal tersebut dapat menyebabkan service DNS **tidak dapat berjalan**.

Sebaiknya domain yang sudah tidak valid dihilangkan dari list sehingga lebih
efektif dan efisien.

### Kurang Bijak
Pemblokiran berbasis alamat IP menurut author tidaklah bijak.

## Penggunaan
`$ python ./internetpositif.py`

    optional arguments:
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

Contoh :

    $ python ./internetpositif.py -f -c

atau

    $ python ./internetpositif.py -cfg -n ns.domain.com -e admin.domain.com -d blokir.domain.com

### Struktur File
    ./RAW_DATA/ (data asli yang didapat dari trustpositif.kominfo.go.id )
    ./DATA/ (hasil list domain yang telah dibersihkan dari folder ./RAW_DATA/)
    ./conf/ (hasil convert named zone yang didapat dari folder ./DATA/)

## Berkontribusi
Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk informasi lebih detail mengenai
cara berkontribusi pada repositori ini.
