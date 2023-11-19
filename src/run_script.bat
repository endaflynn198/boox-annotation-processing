SET input_dir="C:\Users\Username\Google Drive\Books\Exported Boox Annotations"
SET output_dir="C:\Users\Username\Obsidian Vault\Books\Boox Annotations"
cls

python boox_annotation_processing.py %input_dir% %output_dir%

@echo off
REM Example without using arguments specified through %1 and %2 variables
REM python boox_annotation_processing.py "C:\Users\Username\Google Drive\Books\Exported Boox Annotations"  "./output_files/"

