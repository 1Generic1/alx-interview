import pandas as pd
import os

def xfilter(input_file, output_file_filtered, output_file_unfiltered, keywords, email_column=None):
    """
    Args:
        input_file: Path to input CSV or Excel file
        output_file_filtered: Path for filtered results (with keywords)
        output_file_unfiltered: Path for remaining results (without keywords)  
        keywords: List of strings to filter 
        email_column: Optional specific column name containing emails
    """
    try:
        # Read file
        if input_file.endswith(('.xlsx', '.xls')):  # Fixed: added dots
            df = pd.read_excel(input_file)
            print(f"📖 Read Excel file: {len(df)} rows")
        elif input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
            print(f"📖 Read CSV file: {len(df)} rows")
        else:
            raise ValueError("Unsupported file format. Please use .xlsx, .xls, or .csv")  # Fixed: raise error instead of just printing

        print(f"📋 Columns found: {list(df.columns)}")

        # Auto-detect email column if not specified
        if email_column is None:
            email_columns = [col for col in df.columns if 'email' in col.lower()]
            if email_columns:
                email_column = email_columns[0]
                print(f"🔍 Auto-detected email column: '{email_column}'")
            else:
                print("❌ Available columns:", df.columns.tolist())
                raise ValueError("No email column found. Please specify email_column parameter.")
        else:
            # Verify specified column exists
            if email_column not in df.columns:
                raise ValueError(f"Column '{email_column}' not found in file. Available columns: {list(df.columns)}")
        
        # Filter data
        print(f"🔎 Filtering for keywords: {keywords}")
        mask = df[email_column].str.contains('|'.join(keywords), na=False)
        filtered_df = df[mask]
        unfiltered_df = df[~mask]

        # Save files - Fixed: index=False to avoid extra row numbers column
        for data, file_path in [(filtered_df, output_file_filtered), (unfiltered_df, output_file_unfiltered)]:
            if file_path.endswith(('.xlsx', '.xls')):
                data.to_excel(file_path, index=False)  # Changed to index=False
            else:
                data.to_csv(file_path, index=False)    # Changed to index=False

        # Print comprehensive results
        print(f"\n✅ PROCESSING COMPLETE")
        print(f"📁 Input file: {input_file}")
        print(f"📊 Total rows processed: {len(df):,}")
        print(f"✅ Filtered rows (with keywords): {len(filtered_df):,} → {output_file_filtered}")
        print(f"🚫 Unfiltered rows (without keywords): {len(unfiltered_df):,} → {output_file_unfiltered}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Usage example
if __name__ == "__main__":
    xfilter(
    input_file='Agricultural-Contractors-Huntsville-AL-Companies.xlsx',
    output_file_filtered='Tcontacts_agriculture.xlsx', 
    output_file_unfiltered='FILES1_WITHOUT_supportinfoagriculture.xlsx',
    keywords=['support@', 'info@', 'help@']
)