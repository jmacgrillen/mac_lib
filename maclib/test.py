from pathlib import Path
import mac_settings as settings
import mac_logger
import logging

def main():
    
    user_home_directory = Path.home()
    m_logger = mac_logger.configure_logger(
        log_file_uri=f"{user_home_directory}/log.txt",
        logging_level=logging.DEBUG)
    msettings = settings.MacSettings(
        settings_file_path=f"{user_home_directory}/settings.yaml",
        default_settings_path="./default_settings.yaml")

    msettings['uhd-server']['log_level']


if __name__ == "__main__":
    main()
