# Image Index Parser

County Image Parser

###Running with Docker
Create image and run.

```
$ docker build . -t image-parser
$ docker run -i -t --net=host --name=image-parser-cont -v ${pwd}/config:application/config image-parser
```


### Requirements

| Module | Recomended Version |
| ------ | ------ |
| Python | 3.6.9 (> 3.0) |
| virtualenv |  |


#### config.ini content
```
[DB]
server = 127.0.0.1
username = SA 
password = Mg.13579 
# This makes column unique. You may need to use it once. True,1 -> true values. False,0 -> false values
prevent_duplicate = 0 

[SOURCE]
name = collin
```
> You should fill correct DB information here.

#### Source contents
```
[TABLE]
name = Seminar.dbo.Tarrant

[FILE_SERVER]
host = tcftp.tarrantcounty.com
username = cceai
password = Pr0gre$$
# If True or 1, then it uses SFTP, else it uses FTP
use_ssl = True
# This is the root path. We can make it empty. In that case, ftp server default path will be used.
# Empty is working. If you want to set it anyway, this is the example usage: folder = /Home/cceai/
folder = 
parse_file = assumed_names.txt
```


### Running

```
$ pip3 install virtualenv
$ python3 -m virtualenv venv
$ pip3 install -r requirements.txt
$ cd src
$ python3 app.py
```
After the creation of run environment, config.ini should be checked for connection information.
```
$ python parser.py
```

#### requirements.txt

```
configparser==3.7.4
numpy==1.19.4
pandas==1.1.5
pymssql==2.1.5
pysftp==0.2.9
```

> These are the libraries needed.

#### Assumptions
- All table contents are same. Only change is the table name.
- Collin is not reachable from development. Hence it is assumed that it connects to correct folder and the only xml in zip is what we need. 

#### Comments
- Bexar is taking too long to download file.
- Bexar file structure is too complicated and badly organized.


**Author:** *Mehmet Gençol*