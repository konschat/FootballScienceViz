from PIL import Image
import wave, struct, sys, soundfile as Sndfile, numpy as np, math
import numpy as np
# import calc
# from IPython.display import Audio

##
# Collect input
##
path_to_sound = 'C:/Users/konsc/PycharmProjects/FootballScience/certh_demo/output-png/3.png'
name = path_to_sound.split("/")[-1].split(".")[-2]

path_to_save = './output-wav/' + name + '.wav'

# def sound_waveform(framerate=44100):
#     t = np.linspace(0, 5, framerate * 5)
#     data = np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 224 * t)
#
#     # Indicate the calc module if we are inside colaboratory
#     calc.setColaboratory(True)
#
#     # Show waveform
#     calc.plot11(t, data, "Sound Waveform", "Time (s)", "Value")
#
#     # We can zoom the start of the waveform
#     calc.plot11(t[0:10000], data[0:10000], "Sound Waveform (Detail)", "Time (s)", "Value")
#     # Generate a player for mono sound
#     final_audio = Audio(data, rate=framerate, autoplay=True)
#     return final_audio, framerate

# Open image
with Image.open(path_to_sound) as pngFile:

    # Load image
    pngAllPixels = pngFile.load()

    # Set the counters that create the image
    countX = 0
    countY = 0
    count = pngFile.size[0] * pngFile.size[1]

    # Create the array which will contain all the bits
    bitArray = list()

    # Loop through the individual pixels
    while count > 0:
        
        # Set the location of the pixel that should be loaded
        singlePixel = pngAllPixels[countX, countY]

        # Get RGB vals and convert them to hex
        singlePixelToHexString = '%02x%02x%02x' % (singlePixel[0], singlePixel[1], singlePixel[2])

        # Break if end of file (0x0)
        if singlePixelToHexString == "000000":
            break # break because audio is < 44100 bit 

        # Convert hex string into actual hex
        singlePixelToHex = hex(int("0x" + singlePixelToHexString.lstrip("0"), 16) + int("0x0", 16))
        # This adds 16bit/2 (=32768) to the data and converts hex into a bit
        singleBit = int(singlePixelToHex, 16) - 32768

        # Append the single bit to the array
        bitArray.append(singleBit)

        # Run through the image and set x and y vals (goes to next row when ready)
        if countX == (pngFile.size[0] - 1):
            countX = 0
            countY += 1
        else:
            countX += 1
        count -= 1

    # Convert the array into a Numpy array
    bitArrayNp = np.array(bitArray, dtype=np.int16)
    print(bitArrayNp)

    # Sound wave soundwave
    # sound_wave, framerate = sound_waveform()

    # Output the file
    Sndfile.write(path_to_save, bitArrayNp, 44100, 'PCM_16')


