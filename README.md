# SequenceExperiment

This is experiment source for sequence learning of common lab!

# Run code

1. Run this command in terminal

python ./main.py

2. Input participant name in terminal.

3. Input 'r' key after the program is loaded.
4. Input 's' key to start program.

The previous two steps are purpose of synchronizing mri signal. In the skku, mri sends 's' signal when the brain is captured.

5. After a run which means the unit of experiment consisting of multiple trials, "+" sign will be shown continually.
6. If you want to start new run, go to step 3.
   
If you want to stop the program while the program is running, input 'p' command.

# Output

Experiment stimulus and response is stored in experiment directory within following directory. 

Directory path:
  [working_dir]/experiment/[detail experiment name]/[participant_name]

The stimulus file name is stimulus_[participant_name]_r[run_number].csv and response file name is esponser_[participant_name]_r[run_number].csv

The columns of stimulus are Step, Event_Type, Stimulus, display_seconds, start_seconds.

Step denotes the number of visual stimulus
Event_Type denotes visual stimulus type
Stimulus denotes visual information
display_seconds denotes how much a stimulus lasts
start_seconds denotes the timing of showing visual stimulus

# Dependency

I checked this source in mac (version: 12.6.8)

- python: version 3.8.11
- psychopy: version 2021.2.3

## Psychopy

https://psychopy.org

I recommend to install psychopy in conda environment. (version 2021.2.3)



