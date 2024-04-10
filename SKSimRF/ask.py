import numpy as np
import matplotlib.pyplot as plt

# params
SAMPLING_RATE = 1000
BIT_RATE = 10
AMP_0 = 0
AMP_1 = 1
ASK_FREQ = 10

def GenerateCarrierWave(amplitude, freq, duration, sampling_rate):
    t = np.arange(0, duration, 1 / sampling_rate)
    return amplitude * np.sin(2 * np.pi * freq * t)

def ComputeASK(data, bit_rate, amp_0, amp_1, freq, sampling_rate):
    ask_output = []

    for byte in data:
        for i in range(8):
            bit = (byte >> (7 - i)) & 0x01

            if bit == 0:
                signal = GenerateCarrierWave(amp_0, freq, 1 / bit_rate, sampling_rate)
            else:
                signal = GenerateCarrierWave(amp_1, freq, 1 / bit_rate, sampling_rate)
            
            ask_output.extend(signal)

    return np.array(ask_output)

def main():
    input_data = input("DATA> ")

    # get digital data
    ascii_data = [ord(char) for char in input_data]
    digital_signal = np.repeat([int(x) for char in input_data for x in bin(ord(char))[2:].zfill(8)], SAMPLING_RATE * BIT_RATE // 8)

    # generate carrier wave
    duration = len(input_data) * 8 / BIT_RATE
    t = np.linspace(0, duration, int(duration * SAMPLING_RATE))
    carrier_wave = GenerateCarrierWave(AMP_1, ASK_FREQ, duration, SAMPLING_RATE)

    # get ASK
    ask_output = ComputeASK(ascii_data, BIT_RATE, AMP_0, AMP_1, ASK_FREQ, SAMPLING_RATE)

    # Display
    plt.subplot(3, 1, 1)
    plt.plot(np.linspace(0, duration, len(digital_signal)), digital_signal, 'r')
    plt.title('High Low Signal of the Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(t, carrier_wave, "b")
    plt.title("Carrier Wave")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)    

    plt.subplot(3, 1, 3)
    plt.plot(t, ask_output, "g")
    plt.title("ASK Output")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)    

    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    main()


