# Scaffhold

A quick way to start brand new [web2py](http://web2py.com/) projects.

## Instructions

1. Change directory to your web2py `applications` directory path.

2. Run the [scaffhold.sh](scaffhold.sh) bash script to create the project.
    Script parameters:
    - `-t` `--tag`: Specify a commit tag (*optional*);
        default value: "R-2.18.5" (Script version v1.0 10/04/2020)
    - `-n` `--name`: Specify a name for your brand new web2py project  (*optional*);
        default value: "scaffhold"
    - `-r` `--repo`: Specify the url of a blanc remote git repository ready to be initialized (*optional*);

3. Overwrite the `appconfig.ini` file with the template you'll find under your
`private` directory and compile it according to your needs following the inner
documentation.

1. Change directory to your web2py root directory path.

4. Run the script `setupdb.py` you'll find under the path `extra/script/` eventually
inside the prepared python virtualenv to create the needed configured databases:

    - **WARNING** At the moment only **PostgreSQL** and **SQLite** driver are
    supported.

    ```
    (pyenv) user@mypc:web2py$ python ./web2py.py -S <scaffhold app name> -R applications/<scaffhold app name>/extra/scrits/setupdb.py -A -h
    ```

    Refer to the script documentation you can read running it with the `-h` or `--help` option.
