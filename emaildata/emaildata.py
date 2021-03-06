# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:42:02 2017
@author: Wenlong Liu 
wliu14@ncsu.edu
"""
import yagmail
import glob
import time
import os
import json

from smtplib import SMTPAuthenticationError


def _configuration(filename):
    """
    Load configuration parameters from existing json file.
    :param filename: the json file to store parameters.
    :return: A dictionary with all the parameters.
    """
    with open(filename) as configuration:
        data = json.load(configuration)
    return data


def _get_filename(Path, FileType):
    """
    Obtain the specify files in the target folder.
    :param:
    -Path: such as 'F:\\'
    -FileType: file type, such as: .par
    :return:
    A list that contains all the names of targeted files in specific paths.
    """
    files = list()
    for filename in glob.glob(os.path.join(Path, '*' + FileType)):
        files.append(filename)
    return files


def send_email(username, to, subject, body, attachments):
    """
    Wrapper of yagmail to send out emails.
    """
    # for the first time user, a popup will be shown to ask for password.
    yag = yagmail.SMTP(username)
    # Check the types of attachments.
    if attachments:
        contents = [body]
    elif isinstance(attachments,list):
        contents = [body] + attachments
    else:
        raise TypeError("Attachments should be list or None.")

    yag.send(to=to, subject=subject, contents=[body] + attachments)


if __name__ == '__main__':
    # load configurations from json.
    config = _configuration('configuration.json')

    username = config['SendAddress']
    to = config['ReceiveAddress']
    subject = config['Subject']
    body = config['Content']
    interval = config['Interval']
    attachment = config['Attachments']

    while True:
        attachments = list()
        try:
            for item in attachment:
                attachments += _get_filename(attachment[item]['Path'],
                                             attachment[item]['FileType'])

            send_email(username=username, to=to, subject=subject, body=body,
                       attachments=attachments)

            print('Send one email.\n')

        except SMTPAuthenticationError:
            print('Invalid password, please try it again!\n')
            try:
                send_email(username, to, subject=subject, body=body,
                           attachments=attachments)
                print('Send one email.\n')

            except SMTPAuthenticationError:
                print("Invalid email or password again!")
                print("Please close program, login via web browser and try it again .\n")
                break

        except TypeError as e:
            print(e)

        except:
            print('Bad connection, try it again.\n')

        finally:
            time.sleep(interval)
