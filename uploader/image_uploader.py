import argparse
import sys
from utils import connect_db, create_table, insert_image, get_png_files, encode_image

def main(args):
    """
    Main function that takes command-line arguments and uploads .png images to the PostgreSQL table.

    Args:
        args: Command-line arguments.
    """
    directory = args.directory

    # Get the list of .png files
    png_files = get_png_files(directory)

    if not png_files:
        print(f"No .png files found in the directory {directory}")
        return

    # Connect to the database
    try:
        connection = connect_db(args.database, args.user, args.password, args.host, args.port)
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return

    # Create the table
    create_table(connection)

    # Upload each image to the database
    for file in png_files:
        try:
            image_data = encode_image(file)
            insert_image(connection, image_data, file)
            print(f"Uploaded {file} to the database.")
        except Exception as e:
            print(f"Failed to upload {file}: {e}")

    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload .png images to a PostgreSQL table.")
    parser.add_argument("directory", help="The directory containing the .png images.")
    parser.add_argument("database", help="The name of the PostgreSQL database.")
    parser.add_argument("user", help="The PostgreSQL user.")
    parser.add_argument("password", help="The password for the PostgreSQL user.")
    parser.add_argument("host", help="The host of the PostgreSQL database.")
    parser.add_argument("port", help="The port to connect to the PostgreSQL database.")
    args = parser.parse_args()

    main(args)
