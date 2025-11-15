from xxfilter import xfilter_multiple_files
#2 columns
xfilter_multiple_files(
    input_folder= r'.\execfiltsort',
    output_folder='./sortexecfilt', 
    keywords=['M'] ,
    filtered_filename='sortexecfilt.xlsx',
    unfiltered_filename='other.xlsx',
    email_column='E',  # Optional: specify  column , no duplicate
    role_columns=['i', 'E', 'y']  # Optional: specify role columns,  duplicate included
)