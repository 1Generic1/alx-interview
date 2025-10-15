import pandas as pd
import os
import glob

def xfilter_multiple_files(input_folder, output_folder, keywords, filtered_filename, unfiltered_filename, email_column=None, remove_duplicates=True):
    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Find all Excel and CSV files in the input folder
        excel_files = glob.glob(os.path.join(input_folder, "*.xlsx")) + glob.glob(os.path.join(input_folder, "*.xls"))
        csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
        all_files = excel_files + csv_files

        if not all_files:
            print(f"❌ No Excel or CSV files found in '{input_folder}'")
            return
        
        print(f"📁 Found {len(all_files)} files to process:")
        for file in all_files:
            print(f"   - {os.path.basename(file)}")

        # Initialize combined DataFrames
        all_filtered_dfs = []
        all_unfiltered_dfs = []
        processed_files = 0
        current_email_column = None  # Initialize here to avoid reference errors

        # Process each file
        for file_path in all_files:
            file_name = os.path.basename(file_path)
            print(f"\n🔍 Processing: {file_name}")

            try:
                # Read file
                if file_path.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                    file_type = "Excel"
                else:
                    df = pd.read_csv(file_path)
                    file_type = "CSV"
                
                print(f"   📖 Read {file_type} file: {len(df)} rows")
                print(f"   📋 Columns: {list(df.columns)}")

                # Auto-detect email column if not specified
                current_email_column = email_column
                if current_email_column is None:
                    email_columns = [col for col in df.columns if 'email' in col.lower()]
                    if email_columns:
                        current_email_column = email_columns[0]
                        print(f"   🔍 Auto-detected email column: '{current_email_column}'")
                    else:
                        print(f"   ❌ Available columns: {df.columns.tolist()}")
                        print(f"   ⚠️  Skipping file - no email column found")
                        continue
                else:
                    # Verify specified column exists
                    if current_email_column not in df.columns:
                        print(f"   ❌ Column '{current_email_column}' not found. Available: {list(df.columns)}")
                        print(f"   ⚠️  Skipping file")
                        continue
                
                # Filter data
                mask = df[current_email_column].str.contains('|'.join(keywords), na=False)
                filtered_df = df[mask].copy()  # FIX: Use .copy() to avoid warning
                unfiltered_df = df[~mask].copy()  # FIX: Use .copy() to avoid warning

                # Add source file info to track where data came from
                filtered_df.loc[:, 'source_file'] = file_name  # FIX: Use .loc to avoid warning
                unfiltered_df.loc[:, 'source_file'] = file_name  # FIX: Use .loc to avoid warning

                # Add to combined lists
                all_filtered_dfs.append(filtered_df)
                all_unfiltered_dfs.append(unfiltered_df)
                processed_files += 1

                print(f"   ✅ Filtered: {len(filtered_df)} rows | Unfiltered: {len(unfiltered_df)} rows")
                
            except Exception as e:
                print(f"   ❌ Error processing {file_name}: {e}")
                continue

        # Check if we processed any data
        if not all_filtered_dfs:
            print(f"\n❌ No data was processed from any files")
            return
        
        # Combine all results into TWO DataFrames
        combined_filtered = pd.concat(all_filtered_dfs, ignore_index=True)
        combined_unfiltered = pd.concat(all_unfiltered_dfs, ignore_index=True)

        # Remove duplicates if requested
        if remove_duplicates and current_email_column:
            initial_filtered_count = len(combined_filtered)
            initial_unfiltered_count = len(combined_unfiltered)
            
            # PRINT INITIAL COUNTS
            print(f"\n📊 INITIAL DATA ANALYSIS:")
            
            # Count empty/missing emails BEFORE processing
            empty_filtered = combined_filtered[combined_filtered[current_email_column].isna() | (combined_filtered[current_email_column] == '')]
            empty_unfiltered = combined_unfiltered[combined_unfiltered[current_email_column].isna() | (combined_unfiltered[current_email_column] == '')]
            valid_filtered = combined_filtered[combined_filtered[current_email_column].notna() & (combined_filtered[current_email_column] != '')]
            valid_unfiltered = combined_unfiltered[combined_unfiltered[current_email_column].notna() & (combined_unfiltered[current_email_column] != '')]
            
            print(f"   - Filtered: {len(valid_filtered)} valid emails, {len(empty_filtered)} empty/missing emails")
            print(f"   - Unfiltered: {len(valid_unfiltered)} valid emails, {len(empty_unfiltered)} empty/missing emails")
            
            # PRINT DUPLICATE EMAILS FOUND
            print(f"\n🔍 DUPLICATE EMAILS FOUND:")
            
            # Find duplicates in filtered data (only valid emails)
            filtered_duplicates = valid_filtered[valid_filtered.duplicated(subset=[current_email_column], keep=False)]
            if len(filtered_duplicates) > 0:
                print(f"📧 FILTERED duplicates ({len(filtered_duplicates[current_email_column].unique())} unique duplicate emails):")
                for email in filtered_duplicates[current_email_column].unique():
                    duplicate_rows = filtered_duplicates[filtered_duplicates[current_email_column] == email]
                    sources = duplicate_rows['source_file'].unique().tolist()
                    print(f"   - {email} (found {len(duplicate_rows)} times in: {', '.join(sources)})")
            
            # Find duplicates in unfiltered data (only valid emails)
            unfiltered_duplicates = valid_unfiltered[valid_unfiltered.duplicated(subset=[current_email_column], keep=False)]
            if len(unfiltered_duplicates) > 0:
                print(f"📧 UNFILTERED duplicates ({len(unfiltered_duplicates[current_email_column].unique())} unique duplicate emails):")
                for email in unfiltered_duplicates[current_email_column].unique():
                    duplicate_rows = unfiltered_duplicates[unfiltered_duplicates[current_email_column] == email]
                    sources = duplicate_rows['source_file'].unique().tolist()
                    print(f"   - {email} (found {len(duplicate_rows)} times in: {', '.join(sources)})")
            
            # 🔥 REMOVE EMPTY EMAILS + DEDUPLICATE VALID EMAILS
            print(f"\n🔄 PROCESSING DATA:")
            
            # Remove duplicates ONLY from valid emails
            valid_filtered_deduplicated = valid_filtered.drop_duplicates(subset=[current_email_column], keep='first')
            valid_unfiltered_deduplicated = valid_unfiltered.drop_duplicates(subset=[current_email_column], keep='first')
            
            # USE ONLY DEDUPLICATED VALID EMAILS (REMOVE EMPTY EMAILS)
            combined_filtered = valid_filtered_deduplicated
            combined_unfiltered = valid_unfiltered_deduplicated
            
            # COUNT EVERYTHING PROPERLY
            valid_filtered_duplicates_removed = len(valid_filtered) - len(valid_filtered_deduplicated)
            valid_unfiltered_duplicates_removed = len(valid_unfiltered) - len(valid_unfiltered_deduplicated)
            empty_filtered_removed = len(empty_filtered)
            empty_unfiltered_removed = len(empty_unfiltered)
            
            total_filtered_removed = valid_filtered_duplicates_removed + empty_filtered_removed
            total_unfiltered_removed = valid_unfiltered_duplicates_removed + empty_unfiltered_removed
            
            print(f"   - Valid email duplicates removed: {valid_filtered_duplicates_removed} filtered, {valid_unfiltered_duplicates_removed} unfiltered")
            print(f"   - Empty emails removed: {empty_filtered_removed} filtered, {empty_unfiltered_removed} unfiltered")
            print(f"   - Total rows removed: {total_filtered_removed} filtered, {total_unfiltered_removed} unfiltered")
            
            # VERIFICATION - should match initial - removed = final
            verified_filtered = (initial_filtered_count - total_filtered_removed) == len(combined_filtered)
            verified_unfiltered = (initial_unfiltered_count - total_unfiltered_removed) == len(combined_unfiltered)
            
            print(f"\n✅ VERIFICATION:")
            print(f"   - Filtered: {initial_filtered_count} - {total_filtered_removed} = {len(combined_filtered)} {'✓' if verified_filtered else '✗'}")
            print(f"   - Unfiltered: {initial_unfiltered_count} - {total_unfiltered_removed} = {len(combined_unfiltered)} {'✓' if verified_unfiltered else '✗'}")
            
            print(f"\n🗑️  FINAL REMOVAL SUMMARY:")
            if total_filtered_removed > 0:
                print(f"   - Filtered: Removed {total_filtered_removed} total rows")
                if valid_filtered_duplicates_removed > 0:
                    print(f"     • {valid_filtered_duplicates_removed} duplicate valid emails")
                if empty_filtered_removed > 0:
                    print(f"     • {empty_filtered_removed} empty/missing emails")
            else:
                print(f"   - Filtered: No rows removed")
                
            if total_unfiltered_removed > 0:
                print(f"   - Unfiltered: Removed {total_unfiltered_removed} total rows")
                if valid_unfiltered_duplicates_removed > 0:
                    print(f"     • {valid_unfiltered_duplicates_removed} duplicate valid emails")
                if empty_unfiltered_removed > 0:
                    print(f"     • {empty_unfiltered_removed} empty/missing emails")
            else:
                print(f"   - Unfiltered: No rows removed")

        # Use your custom filenames
        filtered_output = os.path.join(output_folder, filtered_filename)
        unfiltered_output = os.path.join(output_folder, unfiltered_filename)

        # Save the TWO combined files with YOUR names
        if filtered_output.endswith(('.xlsx', '.xls')):
            combined_filtered.to_excel(filtered_output, index=False)
        else:
            combined_filtered.to_csv(filtered_output, index=False)
        
        if unfiltered_output.endswith(('.xlsx', '.xls')):
            combined_unfiltered.to_excel(unfiltered_output, index=False)
        else:
            combined_unfiltered.to_csv(unfiltered_output, index=False)

        # Print final results
        print(f"\n🎉 PROCESSING COMPLETE")
        print(f"📁 Input folder: {input_folder}")
        print(f"📁 Output folder: {output_folder}")
        print(f"📊 Files successfully processed: {processed_files}/{len(all_files)}")
        print(f"✅ FILTERED: {len(combined_filtered):,} unique valid email rows")
        print(f"   📄 Saved as: {filtered_filename}")
        print(f"🚫 UNFILTERED: {len(combined_unfiltered):,} unique valid email rows")
        print(f"   📄 Saved as: {unfiltered_filename}")
        print(f"🔍 Keywords used: {keywords}")

        # Show sample of what was filtered
        if len(combined_filtered) > 0:
            print(f"\n📨 SAMPLE OF FILTERED DATA:")
            sample = combined_filtered.head(3)
            for _, row in sample.iterrows():
                email = row[current_email_column]
                source = row['source_file']
                print(f"   - {email} | From: {source}")
        
    except Exception as e:
        print(f"❌ Error: {e}")