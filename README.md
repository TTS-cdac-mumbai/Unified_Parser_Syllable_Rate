
# Find Syllabe rate 

1. Install following python modules : 
    ```bash
    pip install pydub syllables
    ```

2. Make the folder with language name and put the .txt and folder containing the wav files.
   
3. Change the following variable in <em>syl_rate.py</em> script
    ```python
    language = "language_folder_name"
    text_path = "yourtext.txt"
    wav_path = "path_of_wav_folder"
    traverse_from = "wav" # text
    ```
4. And then run 
    ```python
    python syl_rate.py
    ```
    
5. Output file will be generated in <em>language_folder/path_of_wav_folder.csv</em>
   Mean, Median and Variance will be displayed in terminal.