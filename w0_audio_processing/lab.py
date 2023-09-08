"""
6.101 Lab 0: Katie Chen 
Audio Processing
"""

import wave
import struct

# No additional imports allowed!


def backwards(sound):
    """
    Returns a new sound containing the samples of the original in reverse
    order, without modifying the input sound.

    Args:
        sound: a dictionary representing the original mono sound

    Returns:
        A new mono sound dictionary with the samples in reversed order
    """
    # list.reverse() reverses the original list and returns none
    # [::-1] returns a reversed new list and leaves the original untouched
    reversed_samples = sound["samples"][::-1]
    reversed_sound = {"rate": sound["rate"], "samples": reversed_samples}
    return reversed_sound


def mix(sound1, sound2, p):
    """
    Mix two sounds with the same sampling rate together.

    Parameters:

        * Mixing parameter p (float 0 <= p <= 1):
            take p times the samples in the first sound
            and 1-p times the samples in the second sound,
            and add them together to produce a new sound.

    Returns:

        * A new mixed sound, if the sampling rates of two sounds are the same
        * None, if the sampling rates are different
    """

    # mix 2 good sounds
    if (
        "rate" in sound1.keys()
        and "rate" in sound2.keys()
        and sound1["rate"] == sound2["rate"]
    ) is False:
        return None

    if len(sound1["samples"]) <= len(sound2["samples"]):
        shorter_sound = len(sound1["samples"])
    else:
        shorter_sound = len(sound2["samples"])

    mix_sound = []
    index = 0
    while index <= shorter_sound:
        mix_sound.append(
            p * sound1["samples"][index] + sound2["samples"][index] * (1 - p)
        )  # add sounds
        index += 1
        if index == shorter_sound:  # end
            break

    return {"rate": sound1["rate"], "samples": mix_sound}  # return new sound


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new signal consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    sample_delay = round(delay * sound["rate"])
    # final_sample_length = (len(sound["samples"]) * (num_echoes + 1)) - sample_delay * num_echoes
    final_sample_length = len(sound["samples"]) + num_echoes * sample_delay
    all_echo_samples = []
    # populate each copy to be of the same length (final sample length) - but this modifies original copy
    copy_of_original = sound["samples"][:]
    copy_of_original.extend([0] * (final_sample_length - len(sound["samples"])))

    all_echo_samples.append(copy_of_original)

    for copy_num in range(1, num_echoes+1): 
        new_copy = []
        # insert 0 before copy
        offset = [0] * sample_delay * copy_num
        new_copy = offset + new_copy
        for sample in sound["samples"]: 
            new_copy.append(sample * scale ** copy_num)
        new_copy.extend([0] * (final_sample_length - len(new_copy)))
        all_echo_samples.append(new_copy)

    result = all_echo_samples[0]
    # Iterate through the remaining sublists and add corresponding elements
    for sublist in all_echo_samples[1:]:
        result = [a + b for a, b in zip(result, sublist)]
    # print(result)
    return {"rate": sound["rate"], "samples": result}


def pan(sound):
    """
    Adjust the volume in the left and right channels separately,
    so that the left channel starts out at full volume and ends at 0 volume (and vice versa for the right channel).

    Parameters: sound 

    Return: 
    New sound file
    """
    new_right = []
    new_left = []
    N = len(sound['left'])

    for i, sample in enumerate(sound['right']):
        multiplier = 1 / (N - 1)
        new_right.append(sample *  (multiplier * i))
    for i, sample in enumerate(sound['left']): 
        new_left.append(sample * (1 - multiplier * i))
    # print(new_right)
    # print(new_left)
    return {
        'rate': sound['rate'], 
        'left': new_left,
        'right': new_right
    }


def remove_vocals(sound):
    mono_sample = []

    for i in range(len(sound['left'])):
        mono_sample.append(sound['left'][i] - sound['right'][i])
    return { 'rate': sound['rate'], 'samples': mono_sample}


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Load a file and return a sound dictionary.

    Args:
        filename: string ending in '.wav' representing the sound file
        stereo: bool, by default sound is loaded as mono, if True sound will
            have left and right stereo channels.

    Returns:
        A dictionary representing that sound.
    """
    sound_file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = sound_file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    left = []
    right = []
    for i in range(count):
        frame = sound_file.readframes(1)
        if chan == 2:
            left.append(struct.unpack("<h", frame[:2])[0])
            right.append(struct.unpack("<h", frame[2:])[0])
        else:
            datum = struct.unpack("<h", frame)[0]
            left.append(datum)
            right.append(datum)

    if stereo:
        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = [(ls + rs) / 2 for ls, rs in zip(left, right)]
        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Save sound to filename location in a WAV format.

    Args:
        sound: a mono or stereo sound dictionary
        filename: a string ending in .WAV representing the file location to
            save the sound in
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l_val, r_val in zip(sound["left"], sound["right"]):
            l_val = int(max(-1, min(1, l_val)) * (2**15 - 1))
            r_val = int(max(-1, min(1, r_val)) * (2**15 - 1))
            out.append(l_val)
            out.append(r_val)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav("sounds/hello.wav")