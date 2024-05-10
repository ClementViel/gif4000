
# import required module
from pydub import AudioSegment
from pydub.playback import play
 
def playSound(path):
    # for playing mp3 file
    song = AudioSegment.from_mp3(path)
    print('playing sound using  pydub')
    play(song)



