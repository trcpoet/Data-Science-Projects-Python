#Import libraries 

import pandas as pd   
import streamlit as st 
import altair as alt  #Graph library 
from PIL import Image #for displaying logo


#PAGE TITLE 

image = Image.open('dna-logo.jpg') #Show dna logo

st.image(image, use_container_width = True) #Display image to column width 

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")


#INPUT TEXT BOX

#st.sidebar.header("Enter DNA sequence")
st.header("Enter DNA Sequence")

sequence_input = ">DNA Query\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCG\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCG\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCG\n"

#sequence = st.sidebar.text_area("Sequence input", squence_input, height = 250)
sequence = st.text_area("Sequence input", sequence_input, height = 250)
sequence = sequence.splitlines() #Splits lines into lists; sequence ln 1 = DNA Query Name, ln 2 = DNA Sequence
sequence = sequence[1:] #Skips the sequence name (first line)
sequence = ''.join(sequence) #Concatenates list to string 
st.write("""
***
""")

# Prints the input DNA sequence 
st.header('INPUT (DNA Query)')
sequence 

# DNA nucleotide count 
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d = dict([
            ('A', seq.count('A')),
            ('T', seq.count('T')),
            ('G', seq.count('G')),
            ('C', seq.count('C')),
            ])
    return d

X = DNA_nucleotide_count(sequence)

# X_label = list(X)
# X_values = list(X.values())

X

## 2. Print text
st.subheader('2. Print text')
st.write('There are  ' + str(X['A']) + ' adenine (A)')
st.write('There are  ' + str(X['T']) + ' thymine (T)')
st.write('There are  ' + str(X['G']) + ' guanine (G)')
st.write('There are  ' + str(X['C']) + ' cytosine (C)')

### 3. Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X, orient = 'index') #Creates dataframe from dictionary function
df = df.rename({0: 'count'}, axis = 'columns') 
# Because column becomes default at 0'
# When you convert a dictionary like {'A': 10, 'C': 5} with orient='index', 
# pandas creates a DataFrame where your dictionary keys become the index, 
# and the values go into a default column with no name.
# Since no column name was given, pandas names it 0 by default — the first unnamed column
df.reset_index(inplace=True)
# By default, 'A', 'C', 'G', 'T' are the index of the DataFrame.
# reset_index() turns the index into a regular column, so we can treat it like normal data.
# But pandas names it 'index', so we rename it to 'nucleotide'.
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair 
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x = 'nucleotide',
    y = 'count'
)
p = p.properties(
    width = alt.Step(80) #controls width of bar.
)
st.write(p)