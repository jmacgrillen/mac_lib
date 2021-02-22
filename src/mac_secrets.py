#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_secrets.py
    Desscription:
        The Mac Library password manager.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

from pbkdf2 import PBKDF2
from Cryptodome.Cipher import AES
import random
import string
import os
import base64
import pickle
import logging
import mac_lib.mac_file_management as file_m
from src.wadwalker_directories import e_screen_settings_directory


class CESecretsException(Exception):
    """
    Secrets file issue.
    """
    pass


class CESecrets(object):
    """
    Safe password storage.
    """
    mac_logger: logging.Logger = logging.getLogger("mac_logger")
    seed_file_name: str = "{0}/seed.p".format(
        e_screen_settings_directory)
    seed_length: int = 24
    seed: str = None
    kp_file_name: str = "{0}/kfileConfigVerify.p".format(
        e_screen_settings_directory)
    sdb_file_name: str = '{0}/sdbfileNsxConfigVerify'.format(
        e_screen_settings_directory)
    passphrase_size: int = 72
    key_size: int = 32
    block_size: int = 16
    iv_size: int = 16
    salt_size: int = 8
    __instance = None

    def __init__(self):
        """
        Initialise the crypto routines.
        """
        # Load or create the seed file.
        if file_m.does_exist(os_path=self.seed_file_name):
            self.mac_logger.debug("Getting crypto seed.")
            with open(file=self.seed_file_name,
                      mode='r') as seed_file:
                self.seed = seed_file.read()
        else:
            self._create_seed_file()
        # Load or create the kp file.
        if file_m.does_exist(os_path=self.kp_file_name):
            self.mac_logger.debug("Opening kp file")
            with open(file=self.kp_file_name,
                      mode='r') as kp_file:
                self.kp = kp_file.read()
            if len(self.kp) == 0:
                self.mac_logger.error("kp file contained no data.")
                raise CESecretsException()
        else:
            self._initialise_kp_file()
            # If the kp has to be regenerated, then the old data
            # in the SDB file can no longer be used and should be
            # removed
            if file_m.does_exist(os_path=self.sdb_file_name):
                self.mac_logger.info("SDB file is not usable. Deleting it.")
                if not file_m.delete_file(os_path=self.sdb_file_name):
                    err_msg = "Unable to delete the SDB file {0}".format(
                        self.sdb_file_name)
                    self.mac_logger.error(err_msg)
        # Decode the kp value from base64
        print(self.kp)
        self.kp = base64.b64decode(self.kp)

        # Load or create SDB_FILE:
        self.mac_logger.debug("Loading SDB file.")
        if file_m.does_exist(os_path=self.sdb_file_name):
            with open(file=self.sdb_file_name,
                      mode='rb') as sdb_file:
                self.sdb = pickle.load(sdb_file)
                if self.sdb == {}:
                    self.mac_logger.error("SDB file was empty.")
                    # raise CESecretsException()
        else:
            self._initialise_sdb_file()

    def __new__(cls, *args, **kwargs):
        """
        This class is following the Singleton pattern, a class that
        is a single instance that persists across all modules no matter
        how many times the program calls for a new instance.
        """
        if not cls.__instance:
            cls.__instance = super(CESecrets, cls).__new__(
                                cls, *args, **kwargs)
        return cls.__instance

    def _initialise_kp_file(self):
        """
        Create a new kp file.
        """
        self.mac_logger.debug("kp file does not exist. Creating it.")
        with open(file=self.kp_file_name,
                  mode='wb') as kp_file:
            self.kp = os.urandom(self.passphrase_size)
            kp_file.write(base64.b64encode(self.kp))

    def _initialise_sdb_file(self):
        """
        Creata a new secrets database
        """
        self.mac_logger.debug("SDB file does not exist. Creating it.")
        self.sdb = {}
        with open(file=self.sdb_file_name,
                  mode='wb') as sdb_file:
            pickle.dump(self.sdb, sdb_file)

    def _create_seed_file(self):
        """
        Create a file to hold the crypto seed.
        """
        self.mac_logger.debug("Creating a new seed file.")
        self.seed = "{0}".join(
            random.choice(seq=string.ascii_lowercase) for
            _ in range(self.seed_length))
        with open(file=self.seed_file_name,
                  mode='w') as seed_file:
            seed_file.write(self.seed)

    def getSaltForPasswordKey(self, pass_key: str):
        """
        Salt is generated as the hash of the key with it's own
        salt acting like a seed value
        """
        return PBKDF2(pass_key, self.seed).read(self.salt_szie)

    def encrypt(self, pass_key: str, pass_value: str):
        """
        Pad p, then encrypt it with a new, randomly initialised cipher.
        Will not preserve trailing whitespace in plaintext!
        """
        # Initialise Cipher Randomly
        initVector = os.urandom(self.iv_size)
        salt = self.getSaltForPasswordKey(pass_key)
        # Prepare cipher key that will be used to encrypt and decrypt
        k = PBKDF2(self.kp, salt).read(self.key_size)
        # Create cipher that will be used to encrypt the data
        cipher = AES.new(k, AES.MODE_CBC, initVector)
        # Pad and encrypt
        self.sdb[pass_key] = initVector + cipher.encrypt(pass_value + ' '*(
            self.block_size - (len(pass_value) % self.block_size)))
        with open(file=self.sdb_file_name,
                  mode='wb') as f:
            pickle.dump(self.sdb, f)

    def decrypt(self, pass_key: str):
        """
        Reconstruct the cipher object and decrypt. Will not preserve
        trailing whitespace in the retrieved value!
        """
        self.sdb[pass_key]
        salt = self.getSaltForPasswordKey(pass_key)
        # Recreate an identical cipher key:
        key = PBKDF2(self.kp, salt).read(self.key_size)
        # Get initVector (salt) that was concatenated into the encrypted Data
        # stored in the SDB_FILE
        initVector = self.sdb[pass_key][:self.iv_size]
        # Get only the data you want to decrypt
        encryptedData = self.sdb[pass_key][self.iv_size:]
        # Recreate cipher
        cipher = AES.new(key, AES.MODE_CBC, initVector)
        # Decrypt and depad
        return cipher.decrypt(encryptedData).rstrip(' ')
