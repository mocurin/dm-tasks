# Dark matter tasks

Консольное приложение для проверки открытых портов в подсети. Если указаны 443 и 80, то происходит попытка получить информацию о слушаюшем сервере.

Использование:
```bash
python3.8 portscan.py [-h] [-w WORKERS] [-c CHUNKSIZE] [-t TIMEOUT] [-r] [-d] range ports [ports ...]
```

Например:
```bash
python3.8 portscan.py -w 4 192.168.1.0/24 443 80 21 22 25
```

Пример вывода:
```bash
192.168.1.1 80 OPEN
192.168.1.1 443 OPEN
```

Help message:
```bash
Investigate network for open ports

positional arguments:
  range                 IP-addresses range
  ports                 List of ports

optional arguments:
  -h, --help            show this help message and exit
  -w WORKERS, --workers WORKERS
                        Number of workers to use
  -c CHUNKSIZE, --chunksize CHUNKSIZE
                        Chunk size to use within process pool`s imap
  -t TIMEOUT, --timeout TIMEOUT
                        Socket timeout
  -r, --request         Try to request server info. Has no effect ifneither 80 or 443 are used as `ports` arguments
  -d, --debug           Do not suppress stack trace
```
