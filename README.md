# Loggin to xlsx new files in directories like backup journal
Log all new files that match the extensions in specified folders and subfolders

## Requirements
WatchDog, openpyxl, pandas libraries are required
```python
    pip install watchdog openpyxl pandas
```
## Describe
source_path.txt (in the same folder with "censor_file_type.py")

    List of directories. Don't intersect directories

file_types.txt (in the same folder with "censor_file_type.py")
    
    List of filetypes, that logging
    
## Attention
Folders should be exists
Result add to xlsx file backup_journal.xlsx
