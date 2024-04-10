import numpy as np
import matplotlib.pyplot as plt

# params
SAMPLING_RATE = 1000
BIT_RATE = 10
PHASE_0 = 0
PHASE_1 = 180
PSK_FREQ = 10

def GenerateCarrierWave(phase_shift, freq, duration, sampling_rate):
    t = np.arange(0, duration, 1 / sampling_rate)
    return np.sin(2 * np.pi * freq * t + phase_shift)

def ComputePSK(data, bit_rate, phase_0, phase_1, freq, sampling_rate):
    psk_output = []

    for byte in data:
        for i in range(8):
            bit = (byte >> (7 - i)) & 0x01

            if bit == 0:
                signal = GenerateCarrierWave(phase_0, freq, 1 / bit_rate, sampling_rate)
            else:
                signal = GenerateCarrierWave(phase_1, freq, 1 / bit_rate, sampling_rate)
            
            psk_output.extend(signal)

    return np.array(psk_output)

def main():
    input_data = input("DATA> ")

    # get digital data
    ascii_data = [ord(char) for char in input_data]
    digital_signal = np.repeat([int(x) for char in input_data for x in bin(ord(char))[2:].zfill(8)], SAMPLING_RATE * BIT_RATE // 8)

    # generate carrier wave
    duration = len(input_data) * 8 / BIT_RATE
    t = np.linspace(0, duration, int(duration * SAMPLING_RATE))
    carrier_wave = GenerateCarrierWave(PHASE_0, PSK_FREQ, duration, SAMPLING_RATE)

    # get PSK
    psk_output = ComputePSK(ascii_data, BIT_RATE, PHASE_0, PHASE_1, PSK_FREQ, SAMPLING_RATE)

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
    plt.plot(t, psk_output, "g")
    plt.title("PSK Output")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)    

    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    main()


