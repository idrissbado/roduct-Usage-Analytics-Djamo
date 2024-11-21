import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# 1. Connect to the database
def connect_to_db(db_host, db_user, db_password, db_name):
    """
    Establishes a connection to the SQL database.
    """
    try:
        engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")
        connection = engine.connect()
        print("Database connected successfully!")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# 2. Extract data from the database (Replace with actual table and columns)
def extract_data(connection):
    """
    Extracts feature usage data from the database.
    Assumes a table named 'user_activity' with columns: 'user_id', 'feature', 'session_id', 'timestamp'.
    """
    query = """
    SELECT user_id, feature, session_id, timestamp
    FROM user_activity
    WHERE timestamp BETWEEN '2024-01-01' AND '2024-12-31';  -- Example date range
    """
    try:
        df = pd.read_sql(query, connection)
        print(f"Data extracted successfully! Number of rows: {len(df)}")
        return df
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

# 3. Analyze and visualize the data

def analyze_feature_usage(df):
    """
    Analyze feature usage frequency, engagement rate, and session counts.
    """
    # Feature Usage Frequency
    feature_usage = df.groupby('feature').size().reset_index(name='usage_count')

    # Plotting Feature Usage Frequency
    plt.figure(figsize=(10, 6))
    sns.barplot(x='feature', y='usage_count', data=feature_usage, palette='viridis')
    plt.title('Feature Usage Frequency')
    plt.xlabel('Feature')
    plt.ylabel('Usage Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Feature Engagement Rate (Percentage of users engaging with each feature)
    feature_engagement = df.groupby('feature')['user_id'].nunique().reset_index(name='unique_users')
    feature_engagement['engagement_rate'] = feature_engagement['unique_users'] / df['user_id'].nunique()

    # Plotting Feature Engagement Rate
    plt.figure(figsize=(10, 6))
    sns.barplot(x='feature', y='engagement_rate', data=feature_engagement, palette='coolwarm')
    plt.title('Feature Engagement Rate')
    plt.xlabel('Feature')
    plt.ylabel('Engagement Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Session Count per Feature (How many sessions used each feature)
    session_count = df.groupby('feature')['session_id'].nunique().reset_index(name='session_count')

    # Plotting Session Count per Feature
    plt.figure(figsize=(10, 6))
    sns.barplot(x='feature', y='session_count', data=session_count, palette='plasma')
    plt.title('Session Count per Feature')
    plt.xlabel('Feature')
    plt.ylabel('Session Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 4. Main Execution
def main():
    # Database connection details (you will get these credentials from Djamo's team)
    db_host = 'your_database_host'
    db_user = 'your_database_user'
    db_password = 'your_database_password'
    db_name = 'your_database_name'

    # Connect to the database
    connection = connect_to_db(db_host, db_user, db_password, db_name)

    if connection:
        # Extract data
        df = extract_data(connection)

        if df is not None:
            # Analyze and visualize data
            analyze_feature_usage(df)
        
        # Close the database connection
        connection.close()

# Run the main function
if __name__ == "__main__":
    main()
