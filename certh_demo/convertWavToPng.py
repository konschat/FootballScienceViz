from PIL import Image
import wave, struct, sys, math

# if sys.argv[1][-4:] != '.wav':
#     sys.exit("First argument should be a .wav file")
#
# if sys.argv[2][-4:] != '.png':
#     sys.exit("Second argument should be a .png file")

# yt/mp3/wav convertion via https://audio.online-convert.com/convert-to-wav
path_to_sound = 'C:/Users/konsc/PycharmProjects/FootballScience/certh_demo/input-wav/All Them Witches - Tigers Pit.wav'
name = path_to_sound.split("/")[-1].split(".")[-2]

path_to_save = './output-png/' + name + '.png'

# Wave file needs to be 16 bit mono
waveFile = wave.open(path_to_sound, 'r')

if waveFile.getnchannels() != 1:
    sys.exit("ERROR: The wave file should be single channel (mono)")

if waveFile.getframerate() != 44100:
    sys.exit("ERROR: The samplerate should be 44,100")

imageRgbArray = list()

waveLength = waveFile.getnframes()

# Create the image size (based on the length)
imageSize = math.sqrt(44100)

# Loop through the wave file
for i in range(0, 44100):
    
    # Try to read frame, if not possible fill with 0x0
    try:
        waveData = waveFile.readframes(1)
        data = struct.unpack("<h", waveData) # This loads the wave bit
        convertedData = int(data[0]) + 32768 # This adds 16bit/2 (=32768) to the data
    except:
        convertedData = 0
        pass

    # This converts the number into a hex value.
    convertedDataHex = hex(convertedData)

    # convert the value to a string and strips first two characters 
    hexString = str(convertedDataHex)[2:]

    # Check how much the string should be prefixed to get the color hex length (= 6 char)
    count = 6 - len(hexString)

    # Prefix with a zero
    while (count > 0):
        hexString = "0" + hexString 
        count -= 1
    
    # Convert into RGB value
    rgbData = tuple(int(hexString[i:i + 6 // 3], 16) for i in range(0, 6, 6 // 3)) # Convert to RGB data
    
    # Add the RGB value to the image array
    imageRgbArray.append(rgbData)

# Create new image
im = Image.new('RGB', (int(imageSize), int(imageSize)))

# Add image data
im.putdata(imageRgbArray)

# Save image
im.save(path_to_save)