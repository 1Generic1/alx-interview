from xfilter_multiple import xfilter_multiple_files
#1 column
# filter
xfilter_multiple_files(
    input_folder= r'.\execfiltsort',
    output_folder='./sortexecfilt',
    keywords=['M'],
    filtered_filename='execsort.xlsx',
    unfiltered_filename='other.xlsx',
    email_column='email_service'
)

# Example 2: Process different keywords
# xfilter_multiple_files(
#     input_folder= r'./datafile',
#     output_folder='./results',
#     keywords=['i@', 'i@'],
#     filtered_filename='i.xlsx',
#     unfiltered_filename='i.xlsx'
# )

# Example 3: Process with specific email column
# xfilter_multiple_files(
#     input_folder='./datafile',
#     output_folder='./results',
#     keywords=['i@', 'i'],
#     filtered_filename='i.xlsx',
#     unfiltered_filename='i.xlsx',
#     email_column='i'  # Specific column name
# )
