import pandas as pd
import os
import glob

def xfilter_multiple_files(input_folder, output_folder, keywords, filtered_filename, unfiltered_filename, email_column=None, role_columns=None):
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
        current_email_column = None

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

                # Auto-detect role columns if not specified
                current_role_columns = role_columns
                if current_role_columns is None:
                    # Look for common role-related column names
                    role_keywords = ['role', 'position', 'title', 'job', 'department']
                    current_role_columns = [col for col in df.columns if any(word in col.lower() for word in role_keywords)]
                    if current_role_columns:
                        print(f"   🔍 Auto-detected role columns: {current_role_columns}")
                    else:
                        print(f"   ⚠️  No role columns auto-detected, will only filter by email")
                        current_role_columns = []
                else:
                    # Verify specified role columns exist
                    missing_role_columns = [col for col in current_role_columns if col not in df.columns]
                    if missing_role_columns:
                        print(f"   ⚠️  Some role columns not found: {missing_role_columns}")
                        current_role_columns = [col for col in current_role_columns if col in df.columns]
                
                # FILTERING LOGIC: Search in BOTH email and role columns
                print(f"   🔎 Filtering for keywords: {keywords}")
                
                # Create mask for email column filtering - BULLETPROOF
                try:
                    email_mask = df[current_email_column].apply(
                        lambda x: str(x) if pd.notna(x) else ''
                    ).str.contains('|'.join(keywords), na=False)
                except Exception as e:
                    print(f"   ❌ Email filtering error: {e}")
                    continue

                # Create mask for role columns filtering (keep ALL duplicates for roles) - BULLETPROOF
                role_mask = pd.Series([False] * len(df))
                if current_role_columns:
                    for role_col in current_role_columns:
                        try:
                            # Use the same bulletproof method for role columns
                            role_col_mask = df[role_col].apply(
                                lambda x: str(x) if pd.notna(x) else ''
                            ).str.contains('|'.join(keywords), na=False, case=False)
                            role_mask = role_mask | role_col_mask
                        except Exception as e:
                            print(f"   ⚠️  Role column '{role_col}' filtering error: {e}")
                            continue
                
                # COMBINE MASKS: Keep records that match either email OR role criteria
                combined_mask = email_mask | role_mask
                
                # Split data based on combined mask
                filtered_df = df[combined_mask].copy()
                unfiltered_df = df[~combined_mask].copy()

                # Add source file info (FIXED: safe for empty DataFrames)
                if len(filtered_df) > 0:
                    filtered_df = filtered_df.copy()
                    filtered_df['source_file'] = file_name
                if len(unfiltered_df) > 0:
                    unfiltered_df = unfiltered_df.copy()
                    unfiltered_df['source_file'] = file_name

                # Add to combined lists (only if they have data)
                if len(filtered_df) > 0:
                    all_filtered_dfs.append(filtered_df)
                if len(unfiltered_df) > 0:
                    all_unfiltered_dfs.append(unfiltered_df)
                    
                processed_files += 1

                print(f"   ✅ Filtered: {len(filtered_df)} rows | Unfiltered: {len(unfiltered_df)} rows")
                
                # Show what was found in roles vs emails
                if len(filtered_df) > 0:
                    # Reset index to avoid reindexing warnings
                    temp_filtered = filtered_df.reset_index(drop=True)
                    temp_email_mask = email_mask[combined_mask].reset_index(drop=True)
                    temp_role_mask = role_mask[combined_mask].reset_index(drop=True)
    
                    email_matches = len(temp_filtered[temp_email_mask])
                    role_matches = len(temp_filtered[temp_role_mask])
                    both_matches = len(temp_filtered[temp_email_mask & temp_role_mask])
                    
                    print(f"   📊 Match breakdown:")
                    print(f"     • Email matches: {email_matches}")
                    print(f"     • Role matches: {role_matches}")
                    if both_matches > 0:
                        print(f"     • Both email & role matches: {both_matches}")
                
            except Exception as e:
                print(f"   ❌ Error processing {file_name}: {e}")
                continue

        # Check if we processed any data
        if not all_filtered_dfs:
            print(f"\n❌ No data was processed from any files")
            return
        
        # Combine all results
        combined_filtered = pd.concat(all_filtered_dfs, ignore_index=True)
        combined_unfiltered = pd.concat(all_unfiltered_dfs, ignore_index=True)

        # REMOVE DUPLICATES ONLY FOR EMAILS, KEEP ALL ROLE DUPLICATES
        print(f"\n🔄 PROCESSING DUPLICATES:")
        print(f"   📧 Removing duplicate emails only")
        print(f"   👥 Keeping ALL role-based duplicates")
        
        initial_filtered_count = len(combined_filtered)
        initial_unfiltered_count = len(combined_unfiltered)
        
        # Remove duplicates based on email column only
        if current_email_column and current_email_column in combined_filtered.columns:
            # Count duplicates before removal
            email_duplicates = combined_filtered[combined_filtered.duplicated(subset=[current_email_column], keep=False)]
            unique_duplicate_emails = email_duplicates[current_email_column].nunique()
            
            print(f"   📧 Found {unique_duplicate_emails} unique duplicate emails in filtered data")
            
            # Remove email duplicates but keep first occurrence
            combined_filtered = combined_filtered.drop_duplicates(subset=[current_email_column], keep='first')
            
            print(f"   ✅ Removed {initial_filtered_count - len(combined_filtered)} duplicate email rows from filtered data")
        
        if current_email_column and current_email_column in combined_unfiltered.columns:
            # Remove duplicates from unfiltered data as well
            combined_unfiltered = combined_unfiltered.drop_duplicates(subset=[current_email_column], keep='first')
            
            print(f"   ✅ Removed {initial_unfiltered_count - len(combined_unfiltered)} duplicate email rows from unfiltered data")

        # Use your custom filenames
        filtered_output = os.path.join(output_folder, filtered_filename)
        unfiltered_output = os.path.join(output_folder, unfiltered_filename)

        # Save the files
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
        print(f"✅ FILTERED: {len(combined_filtered):,} rows (email duplicates removed)")
        print(f"   📄 Saved as: {filtered_filename}")
        print(f"🚫 UNFILTERED: {len(combined_unfiltered):,} rows (email duplicates removed)")
        print(f"   📄 Saved as: {unfiltered_filename}")
        print(f"🔍 Keywords used: {keywords}")

        # Show detailed sample of what was filtered
        if len(combined_filtered) > 0:
            print(f"\n📨 SAMPLE OF FILTERED DATA:")
            sample = combined_filtered.head(5)
            for _, row in sample.iterrows():
                email = row[current_email_column] if current_email_column in row else 'N/A'
                source = row['source_file']
                
                # Show which role columns had matches
                role_matches_info = []
                if current_role_columns:
                    for role_col in current_role_columns:
                        if role_col in row and pd.notna(row[role_col]):
                            role_value = str(row[role_col])
                            if any(keyword.lower() in role_value.lower() for keyword in keywords):
                                role_matches_info.append(f"{role_col}: {role_value}")
                
                role_info = " | " + ", ".join(role_matches_info) if role_matches_info else ""
                print(f"   - {email} | From: {source}{role_info}")
        
    except Exception as e:
        print(f"❌ Error: {e}")