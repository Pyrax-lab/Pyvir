




                                            

#________________________________________________________________________                                
# |[] Pyvir                                                         [F] |'|
# |---------------------------------------------------------------------|'|
# |12.Pyvir:> cmd.exe                                                   | |
# |12.localhost:/Asc> ed shell01.asc                                    | |
# |                                                                     | |
# |                                                                     |_|
# |_____________________________________________________________________|/|
                                   

from colorama import Fore, Style, init

# Инициализация для Windows
init()

logo = f"""
{Fore.GREEN} 
@@@@@@@   @@@ @@@  @@@  @@@  @@@  @@@@@@@   
@@@@@@@@  @@@ @@@  @@@  @@@  @@@  @@@@@@@@  
@@!  @@@  @@! !@@  @@!  @@@  @@!  @@!  @@@  
!@!  @!@  !@! @!!  !@!  @!@  !@!  !@!  @!@  
@!@@!@!    !@!@!   @!@  !@!  !!@  @!@!!@!   
!!@!!!      @!!!   !@!  !!!  !!!  !!@!@!    
!!:         !!:    :!:  !!:  !!:  !!: :!!   
:!:         :!:     ::!!:!   :!:  :!:  !:!  
::          ::      ::::     ::  ::   :::  
:           :        :      :     :   : :            

{Style.RESET_ALL}
"""

menu = f"""
{Fore.CYAN}Pyvir (v0.1)  - 2025
            \nGitHub: https://github.com/Pyrax-lab/Pyvir\n\nUsing malware, including viruses\nand other malicious software, should\nonly be done on your personal computer\nand solely for educational purposes.
{Style.RESET_ALL}
"""

# Печать баннера и меню
print(logo)
print(menu)
a= input()
