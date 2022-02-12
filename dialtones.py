import scipy.io.wavfile as wv
import sys
import numpy as np
import matplotlib.pyplot as plt

def report_progress(current, total):
    sys.stdout.write('\rProgress: {:.2%}'.format(float(current)/total))
    if current==total:
       sys.stdout.write('\n')
    sys.stdout.flush()

def dft(N, offset, end): # Creates a DFT matrix

    i, j = np.meshgrid(np.arange(N), np.arange(offset,end))
    omega = np.exp( - 2 * np.pi * 1J / N )
    W = np.power( omega, i * j ) / np.sqrt(N)
    return W

def fourier_analysis(sound, offset, end):

    N = len(sound)
    x =  dft(N, offset, end) # create Matrix for DFT
    fourier_coeff = np.absolute(x @ sound)[:N // 2] # calculate Fourier coefficents
    peak = sorted(fourier_coeff.argsort()[-2:][::-1] + offset ) # look for two highest peaks in the coefficents
    first_one = possibilities[np.argmin([abs(peak[0]-pos) for pos in possibilities  ]   )] 
    second_one = possibilities[np.argmin([abs(peak[1]-pos) for pos in possibilities  ]   )]
    fin = sorted([first_one, second_one]) # Now we found the most likely frequencies

    return fourier_coeff, peak, telefone[rows[fin[0]] + cols[fin[1]]]

def find_numbers(sampling_data, rate, offset, end):
    # Some plotting adjustments
    plt.rcParams.update({'font.size': 8})
    fig, axs = plt.subplots(2,3, figsize=(15, 6), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace = .5, wspace=.001)

    axs = axs.ravel()
    code = "" # Number that is dialed
    n = len(data) // rate

    for i in range(n):
        report_progress(i,n-1)
        coeff, peak, item = fourier_analysis(sampling_data[i*rate: (i+1)*rate], offset, end)
        axs[i].plot(np.arange(offset, end),coeff) # Plot
        axs[i].set_title("Number " +  str(i+1) + "\n Peaks at " + str(peak[0]) + " and " + str(peak[1]) + " so this is a " + item)
        code += item

    print("\n The called number is "+ code)
    plt.show()
    return
  
# This is how we look at the telephone
telefone = {   "11": "1", "12": "2", "13": "3",
            "21": "4","22": "5","23": "6",
            "31": "7","32": "8","33": "9",
            "41": "*","42": "0","43": "#" }

rows = { 697: "1", 770: "2", 852: "3", 941: "4" }
cols ={ 1209: "1", 1336: "2", 1477: "3"}

possibilities = [ 697, 770, 852, 941, 1209, 1336, 1477] # We need that to reduce noise

rate, data = wv.read("dialtones.wav") # open file

offset = 650 # lower bound for frequencies
end = 1500 # upper bound for frequencies

find_numbers(data, rate, offset, end)