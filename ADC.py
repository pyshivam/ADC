#!/usr/bin/env python3
import os
import shutil


def check_for_root():
    if os.getuid() != 0:
        print("Need root access to run this file. Exiting :(")
        exit(1)
    else:
        os.system("clear")


def banner():
    print("""

        
                                                                                   
                                                                                   
                       AAA               DDDDDDDDDDDDD                CCCCCCCCCCCCC
                      A:::A              D::::::::::::DDD          CCC::::::::::::C
                     A:::::A             D:::::::::::::::DD      CC:::::::::::::::C
                    A:::::::A            DDD:::::DDDDD:::::D    C:::::CCCCCCCC::::C
                   A:::::::::A             D:::::D    D:::::D  C:::::C       CCCCCC
                  A:::::A:::::A            D:::::D     D:::::DC:::::C              
                 A:::::A A:::::A           D:::::D     D:::::DC:::::C              
                A:::::A   A:::::A          D:::::D     D:::::DC:::::C              
               A:::::A     A:::::A         D:::::D     D:::::DC:::::C              
              A:::::AAAAAAAAA:::::A        D:::::D     D:::::DC:::::C              
             A:::::::::::::::::::::A       D:::::D     D:::::DC:::::C              
            A:::::AAAAAAAAAAAAA:::::A      D:::::D    D:::::D  C:::::C       CCCCCC
           A:::::A             A:::::A   DDD:::::DDDDD:::::D    C:::::CCCCCCCC::::C
          A:::::A               A:::::A  D:::::::::::::::DD      CC:::::::::::::::C
         A:::::A                 A:::::A D::::::::::::DDD          CCC::::::::::::C
        AAAAAAA                   AAAAAAADDDDDDDDDDDDD                CCCCCCCCCCCCC
                                                                                   
                                                                                   
                                                                           
                                                                                                                               
                                                                           

                                                                Apache Domain Creator v1.0

    Coded by: pyshivam
""")


public_folder = "public_html"


def make_file_structure(server_name, server_admin):
    # Changing Directory to '/var/www'
    os.chdir('/var/www/')

    # Making folder for our website or project.
    try:
        os.mkdir(server_name)
    except FileExistsError:
        print("File already exists.")
        dis = input("Do you want to overwrite?(Y/n): ")
        if dis.lower() == 'yes' or dis.lower() == 'y':
            shutil.rmtree(server_name)
            os.mkdir(server_name)

    # Changing directory to flask app.
    os.chdir(server_name)

    # Making file structure.
    os.mkdir(public_folder)
    give_permissions(server_name)
    make_config(server_name, server_admin)


def give_permissions(server_name):
    """
    Now we have the directory structure for our files, but they are owned by our root user.
    If we want our regular user to be able to modify files in our web directories.


    :param server_name:
    :return: boolean
    """

    user = os.system("chown -R $USER:$USER /var/www/{0}/public_html".format(server_name))

    # We should also modify our permissions a little bit to ensure that read access is permitted to
    # the general web directory and  all of the files and folders it contains so that pages can be served correctly
    root = os.system("chmod -R 755 /var/www")

    if user == 0 and root == 0:
        return True
    else:
        return False


def create_webpage(server_name):

    """
    Create Web page to show information

    :param server_name:
    :return: html template
    """

    return """<html>
      <head>
        <title>Welcome to {0}!</title>
      </head>
      <body>
        <h1>Success!  The {0} virtual host is working!</h1>
      </body>
    </html>
            """.format(server_name)


def make_config(server_name, server_admin):
    # Changing Directory to '/var/www/'+app_name
    os.chdir('/var/www/' + server_name + "/" + public_folder)

    # Main program of your project logic goes here
    with open('index.html', 'w+') as index:
        print(create_webpage(server_name), file=index)

    config = """
<VirtualHost *:80>
            ServerName {server_name}
            ServerAdmin {server_admin}
            DocumentRoot /var/www/{server_name}/public_html
            ErrorLog {apache_dir}/error.log
            LogLevel warn
            CustomLog {apache_log_dir}/access.log combined
</VirtualHost>
""".format(server_name=server_name, server_admin=server_admin,
           apache_dir="${APACHE_LOG_DIR}", apache_log_dir="${APACHE_LOG_DIR}")

    #  Successfully virtual host created.
    with open("/etc/apache2/sites-available/{server_name}.conf".format(server_name=server_name), 'w+') as conf:
        print(config, file=conf)

    #  Virtual host enabled.
    if os.system("a2ensite {server_name}".format(server_name=server_name)) == 0:
        print("Successfully virtual host created, virtual host enabled.")
    else:
        print("Error occurred")
        exit(1)

    if restart_apache() == 0:
        print("Server restarted successfully.")


def restart_apache():
    return os.system("systemctl reload apache2")


def disable_domain(server_name):
    return os.system("a2dissite {server_name}".format(server_name=server_name))


def remove_domain(server_name):
    pass


def main():
    print("Enter fully qualified domain name. \nE.g: example.com or subdomain.example.com")
    server_name = input("Enter domain name: ")
    print("Enter server admin email address. \nE.g: admin@example.com")
    server_admin = input("Enter email: ")
    make_file_structure(server_name, server_admin)


if __name__ == '__main__':
    check_for_root()
    banner()
    pwd = os.getcwd()
    main()
