import os
import base64
import psycopg2
from PIL import Image
from typing import List

def connect_db(database: str, user: str, password: str, host: str, port: int) -> psycopg2.extensions.connection:
    """
    Connect to the PostgreSQL database.

    Args:
        database: The name of the database.
        user: The database user.
        password: The password for the database user.
        host: The database host.
        port: The port to connect to the database.

    Returns:
        A connection object.
    """
    try:
        connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        return connection
    except psycopg2.Error as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        raise

def create_table(connection: psycopg2.extensions.connection):
    """
    Create a table for storing image data and file paths in the database.

    Args:
        connection: A connection object for the database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS images (id SERIAL PRIMARY KEY, image_data BYTEA, file_path TEXT);")
        connection.commit()
        cursor.close()
    except psycopg2.Error as error:
        print(f"Error while creating table: {error}")
        raise

def insert_image(connection: psycopg2.extensions.connection, image_data: bytes, file_path: str):
    """
    Insert an image and its file path into the database.

    Args:
        connection: A connection object for the database.
        image_data: The image data as bytes.
        file_path: The file path of the image.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO images (image_data, file_path) VALUES (%s, %s);", (image_data, file_path))
        connection.commit()
        cursor.close()
    except psycopg2.Error as error:
        print(f"Error while inserting image: {error}")
        raise

def get_png_files(directory: str) -> List[str]:
    """
    Get a list of .png file paths from a directory.

    Args:
        directory: The directory to search for .png files.

    Returns:
        A list of .png file paths.
    """
    png_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith('.png')]
    return png_files

def encode_image(image_path: str) -> bytes:
    """
    Encode an image as bytes using Base64.

    Args:
        image_path: The file path of the image.

    Returns:
        The encoded image data as bytes.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
            return encoded_image
    except IOError as error:
        print(f"Error while reading image: {error}")
        raise

