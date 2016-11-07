#!/bin/bash

# Get the MIDI path/file name
mid=$(zenity --file-selection)
if [ $? = 1 ];
then exit
fi

# Get save path/file name
wav=$(zenity --file-selection --save --confirm-overwrite)
if [ $? = 1 ];
then exit
fi

# see if current user has write permissions by creating an empty file
> $wav
# if so, do the conversion and show progress bar
if [ $?  -eq 0 ]; then
timidity "$mid" -Ow -o "$wav" | zenity --progress --pulsate --auto-close --text "Converting..."

# Tell us the conversion is done
zenity --info --text "Conversion complete!"

# if not, get root password, run command as root
else
# Get the users password
passwd=$(zenity --password)

# Do the conversion and show a progress bar
echo $passwd|sudo -S timidity "$mid" -Ow -o "$wav" | zenity --progress --pulsate --auto-close --text "Converting..."
if [ $? = 1 ];
then exit
fi

# Tell us the conversion is done
zenity --info --text "Conversion complete!"
fi
MIDI_converter.sh.zip566 bytes
« PreviousNext »View All Steps
profile pic

We have a be nice comment policy.
Please be positive and constructive.

