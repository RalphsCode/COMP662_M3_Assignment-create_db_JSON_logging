# !/usr/bin/env python3

# Assignment 3 - SQL Statements
# Author: Ralph Godkin

'''
General Comments: This application creates a database MOVIE.DB, reads the movie data from MOVIE_DATA.JSON,
                inserts the JSON data into the db, creates a MOVIE.LOG file to record the log entries,
                and finally prints out certain details as required by the assignment. '''

# Imports
import logging
import json
import sqlite3

# Configure the logging module
logging.basicConfig(filename="movie.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
        
    # Open the JSON file containing the movie data
    with open('movie_data.json', 'r') as file:
        # Load the data from the JSON file
        movie_data = json.load(file)

    # Connect to the database (creates a new database if it doesn't exist)
    conn = sqlite3.connect('movie.db')
    
    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # Update log
    logging.debug('Successfully: (1)loaded JSON file  (2)connected to database  (3)created cursor')  


    # Create the 2 tables
    create_table_1 = '''
        CREATE TABLE IF NOT EXISTS movies_info_1 (
            show_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL
        );
        '''
    cursor.execute(create_table_1)

    create_table_2 = '''
           CREATE TABLE IF NOT EXISTS movies_info_2 (
            show_id TEXT PRIMARY KEY,
            director TEXT NOT NULL,
            release_year TEXT,
            description TEXT NOT NULL,
            FOREIGN KEY (show_id) REFERENCES movies_info_1(show_id)
        );
        '''
    cursor.execute(create_table_2)

    # Update log
    logging.info('Successfully created 2 tables in the database')

    # Insert data into movies_info_1 table
    insert_data_table_1 = '''
        INSERT INTO movies_info_1 (show_id, title, genre)
        VALUES (?, ?, ?)
        '''

    # Pull the values from the movie_data dictionary
    cursor.execute(insert_data_table_1, (
        movie_data['movie_1']['show_id'],
        movie_data['movie_1']['title'],
        movie_data['movie_1']['genre']
        ))
    cursor.execute(insert_data_table_1, (
        movie_data['movie_2']['show_id'],
        movie_data['movie_2']['title'],
        movie_data['movie_2']['genre']
        ))
    cursor.execute(insert_data_table_1, (
        movie_data['movie_3']['show_id'],
        movie_data['movie_3']['title'],
        movie_data['movie_3']['genre']
        ))


    # Insert data into movies_info_2 table
    insert_data_table_2 = '''
        INSERT INTO movies_info_2 (show_id, director, release_year, description)
        VALUES (?, ?, ?, ?)
        ''' 
    # Pull the values from the movie_data dictionary
    cursor.execute(insert_data_table_2, (
        movie_data['movie_1']['show_id'], 
        movie_data['movie_1']['director'], 
        movie_data['movie_1']['release_year'], 
        movie_data['movie_1']['description']
        ))
    cursor.execute(insert_data_table_2, (
        movie_data['movie_2']['show_id'], 
        movie_data['movie_2']['director'], 
        movie_data['movie_2']['release_year'], 
        movie_data['movie_2']['description']
        ))
    cursor.execute(insert_data_table_2, (
        movie_data['movie_3']['show_id'], 
        movie_data['movie_3']['director'], 
        movie_data['movie_3']['release_year'], 
        movie_data['movie_3']['description']
        ))
        
    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

    # Update log
    logging.debug('Successfully loaded the data to the tables, and closed connection to the database')

    #==================================================================================================
    #####  PRINTING OUTPUT  ########

    # Open a new database connection
    conn = sqlite3.connect('movie.db')

    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # INNER JOIN the 2 movie tables
    join_the_tables = '''
        SELECT movies_info_1.*, movies_info_2.* 
        FROM movies_info_1
        INNER JOIN movies_info_2 
        ON movies_info_1.show_id = movies_info_2.show_id
        '''
    cursor.execute(join_the_tables)

    # Fetch all the result rows
    movie_rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Print the movie info from the database
    print("\nGodkin Assignment: 3 - MOVIE DATABASE\n")
    print('P_KEY\tMOVIE TITLE\tGENRE\tP_KEY\tDIRECTOR\tYEAR\tDESCRIPTION\n')
    for row in movie_rows:
        print(row)

    # Update log
    logging.debug('Successfully reopened the db, completed INNER JOIN, printed results, and closed connection')

    # Print last 3 entries in log file (movie.log)

    # Open the log file
    log_file_path = 'movie.log'
    with open(log_file_path, 'r') as file:
        # Read all the lines of the file
        lines = file.readlines()

    # Get the last 3 entries
    last_three_entries = lines[-3:]

    # Print the last 3 lines
    print('\n\n==> Last 3 entries in log file (movie.log):\n')

    for line in last_three_entries:
        print(line)


    # Print completion statement
    print('\n\t APPLICATION COMPLETED SUCCESFULLY.\n')

if __name__ == "__main__":
    main()