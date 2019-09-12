#!/usr/bin/env bash
clear
banner(){
    clear
    echo """




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
         """
}


banner
# check for if this script is running as root or not.
if [[ `id -u` -ne 0 ]]
  then echo "Please run setup as root."
  exit 1
fi


packages=('apache2' 'python3')

for i in ${packages[@]}; do
    echo "Checking: ${i}"
    dpkg -s ${i} &> /dev/null

    if [[ $? -eq 0 ]]; then
        echo "${i} is already installed!"
    else
        echo "${i} is NOT installed!"
        echo "Installing ${i}..."
        apt -y install ${i}
        if [[ $? -ne 0 ]]; then
            echo "Error while installing package ${i}"
        fi
    fi
done
