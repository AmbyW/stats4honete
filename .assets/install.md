#### Install Python

* ###### Ubuntu and derivates

```bash
$ sudo apt install build-essential python3 python3-dev python3-pip python3-wheel python3-setuptools python3-virtualenv python3-virtualenvwrapper libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info git redis
```

* ###### Windows
Install Python3 [Python3 64bit](https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe) o [Python3 32bit](https://www.python.org/ftp/python/3.8.7/python-3.8.7.exe)
if didn't do it using the installer you should [set Python path in environment PATH OS variable](https://datatofish.com/add-python-to-windows-path/)


#### Download repository and move inside

* ###### manually from browser using the link
    [Download Hon Stats](https://github.com/AmbyW/stats4honete/archive/refs/heads/main.zip)

* ###### or using bash with a downloader
    wget https://github.com/AmbyW/stats4honete/archive/refs/heads/main.zip

* ###### or clone it using Git
    git clone https://github.com/AmbyW/stats4honete.git

if repository was downloaded and not cloned with Git you need to uncompress the zip file to continue
other wise only need to move inside project folder

```bash
    cd stats4honete/
```


#### Create and activate python virtual environment

* ###### Ubuntu and derivates
```bash
$ virtualenv hon_stats -p python3
$ source hon_stats/bin/activate
```

* ###### Windows
```bash
$ virtualenv hon_stats -p python3
$ hon_stats/bin/activate.bat
```

#### Install requirements
```bash
$ pip3 install -r ./requeriments.txt
```

#### Set configuration values

Check 'envs/example_env' file tu create a valid environment file for configuration values system needs to works as expected.

* ###### Ubuntu

```bash
$ sudo cp envs/local/example_env /etc/environment.d/candy_app.conf
```

* ###### windows

Set manually the values as windows environment variables as explain [here](https://answers.microsoft.com/es-es/windows/forum/windows_10-other_settings/windows-10-variables-de-entorno-windows-10-version/703ea5fa-1db4-46da-8ff7-6261140bf58b)
