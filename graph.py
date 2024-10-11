from flask import Flask, render_template, send_from_directory
import pandas as pd
from pyvis.network import Network
from sqlalchemy import create_engine
import os

# PostgreSQL connection details
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'airflow'

# Create PostgreSQL connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Define output directory for graphs
output_base_dir = 'assets/graph'
folders = [
    'causes_female', 'causes_male', 'causes_reccu',
    'treats_female', 'treats_male', 'treats_reccu',
    'prevents_female', 'prevents_male', 'prevents_reccu',
    'diagnoses_female', 'diagnoses_male', 'diagnoses_reccu'
]

# Ensure graph output directories exist
for folder in folders:
    output_dir = os.path.join(output_base_dir, folder)
    os.makedirs(output_dir, exist_ok=True)

cancer_types = ['Female Breast Cancer', 'Male Breast Cancer', 'Recurrent Breast Cancer']
tables = ['causes_table', 'treats_table', 'prevents_table', 'diagnoses_table']

def generate_graphs(table):
    try:
        with engine.connect() as connection:
            df = pd.read_sql_table(table, connection)
    except Exception as e:
        print(f"Error reading from table {table}: {e}")
        return

    categories = df['Category'].unique()
    for category in categories:
        df_category = df[df['Category'] == category]
        
        # Determine the output directory based on the table name and category
        output_dir = os.path.join(output_base_dir, f"{table[:-6]}_{category.lower()}")  # Assuming table names end with "_table"
        
        # Create a new Network graph
        net = Network(notebook=True)

        for _, row in df_category.iterrows():
            net.add_node(row['SUBJECT_NAME'], title=row['SUBJECT_NAME'], size=15, color='lightblue')
            net.add_node(row['OBJECT_NAME'], title=row['OBJECT_NAME'], size=15, color='lightgreen')
            net.add_edge(
                row['SUBJECT_NAME'], 
                row['OBJECT_NAME'], 
                color='gray'
            )

        file_path = os.path.join(output_dir, f'{category}.html')
        net.save_graph(file_path)  # Save the graph as an HTML file

def generate_all_graphs():
    for table in tables:
        generate_graphs(table)

if __name__ == "__main__":
    generate_all_graphs()