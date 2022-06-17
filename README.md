## Instructions

1. Install requirements 
   ```
   pip install -r requirements.txt
   ```
   
2. Run app 
   ```
   python main.py
   ```

3. The output of pipeline will be saved in `data` folder, 
with sub-folders for each run in format: `YEAR-MONTH-DATE-HOUR-MINUTE`. Each sub-folder contains following:   
   * metadata: metadata in `.csv` format per language
   * wavs: actual `.wav` format audio files in corresponding folders per language
   * vads: output in `.csv` format of voice activity detector per language
   * lang_clas: output in `.csv` format of language classifier per language