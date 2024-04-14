import paramiko
import subprocess
import argparse
import os
import win32gui
import win32con
import easygui


# Подключение к удаленному компьютеру
def connect_to_remote(host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=22, username=username, password=password)
    return client

# Деинсталляция Windows
def uninstall_windows(client):
    # Команда для деинсталляции Windows с использованием wimlib
    uninstall_command = 'wimlib-imagex apply /path/to/windows.wim 1 /dev/sdx --skip-ntfs --no-check'

    stdin, stdout, stderr = client.exec_command(uninstall_command)

    # Печать вывода команды
    print(stdout.read().decode())

    # Проверка наличия ошибок
    if stderr.channel.recv_exit_status() != 0:
        print('Произошла ошибка при деинсталляции Windows.')
    else:
        print('Windows успешно деинсталлирован.')

# Создание ISO файла с операционной системой и дополнительными пакетами
def create_iso(os_files, additional_packages, output_iso):
    os_files_str = " ".join(os_files)
    additional_packages_str = " ".join(additional_packages)

    create_iso_command = f"mkisofs -o {output_iso} {os_files_str} {additional_packages_str}"

    subprocess.run(create_iso_command, shell=True)

# Установка готового ISO образа на чистый диск
def install_iso_image(iso_image, disk_path):
    install_iso_command = f"dd if={iso_image} of={disk_path} bs=4M status=progress"

    subprocess.run(install_iso_command, shell=True)

def main():
    remote_host = easygui.enterbox("Введите IP-адрес удаленного хоста:")
    remote_username = easygui.enterbox("Введите имя пользователя удаленного хоста:")
    remote_password = easygui.passwordbox("Введите пароль удаленного хоста:")
    installation_type = easygui.choicebox("Выберите тип АРМ:", choices=['server', 'client'])
    server_config = easygui.choicebox("Выберите пакет доп ПО:", choices=['1', '2'])

    # Подключение к удаленному компьютеру
    ssh_client = connect_to_remote(remote_host, remote_username, remote_password)

    if ssh_client:
        # Деинсталляция Windows
        uninstall_windows(ssh_client)

        # Установка ISO образа на чистый диск
        iso_path = '/path/to/iso/image.iso'
        disk_path = '/dev/sdx'
        install_iso_image(iso_path, disk_path)

        # Установка дополнительных пакетов в зависимости от типа установки
        additional_packages = []
        if installation_type == 'server':
            additional_packages.append('server_package1')
            additional_packages.append('server_package2')
            if server_config:
                additional_packages.append(server_config)
        elif installation_type == 'client':
            additional_packages.append('client_package1')
            additional_packages.append('client_package2')

        # Установка дополнительных пакетов
        for package in additional_packages:
            install_additional_package(ssh_client, package)

        ssh_client.close()

if __name__ == '__main__':
    main()
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)

